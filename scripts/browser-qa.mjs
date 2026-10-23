import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { setTimeout as delay } from 'node:timers/promises';

// Minimal hosts may use optional, ignored local browser libraries and fonts.
const localLibraries = path.resolve('.browser-libs/usr/lib/x86_64-linux-gnu');
const localFonts = path.resolve('.browser-libs/fonts.conf');
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync('.browser-cache')) process.env.PLAYWRIGHT_BROWSERS_PATH = path.resolve('.browser-cache');
if (!process.env.FONTCONFIG_FILE && existsSync(localFonts)) process.env.FONTCONFIG_FILE = localFonts;
if (existsSync(localLibraries)) process.env.LD_LIBRARY_PATH = [localLibraries, process.env.LD_LIBRARY_PATH].filter(Boolean).join(':');

const { chromium, expect } = await import('@playwright/test');
const { default: AxeBuilder } = await import('@axe-core/playwright');

// Start an isolated local preview by default. Explicit URLs reuse existing previews.
// The independent parent repository is tested only when its URL is supplied.
let gardenUrl = process.env.GARDEN_QA_URL;
const parentUrl = process.env.PARENT_QA_URL;
let previewProcess;
if (!gardenUrl) {
  const reservation = createServer();
  await new Promise(resolve => reservation.listen(0, '127.0.0.1', resolve));
  const port = reservation.address().port;
  await new Promise(resolve => reservation.close(resolve));
  previewProcess = spawn(process.execPath, ['scripts/serve.mjs'], { env: { ...process.env, PORT: String(port) }, stdio: 'ignore' });
  process.once('exit', () => previewProcess?.kill());
  process.once('SIGINT', () => process.exit(130));
  process.once('SIGTERM', () => process.exit(143));
  gardenUrl = `http://127.0.0.1:${port}`;
  let ready = false;
  for (let attempt = 0; attempt < 100; attempt++) {
    try { if ((await fetch(`${gardenUrl}/health.json`)).ok) { ready = true; break; } } catch {}
    if (previewProcess.exitCode !== null) throw new Error('Garden preview exited during startup. Build dist/ first.');
    await delay(100);
  }
  if (!ready) throw new Error('Garden preview did not become ready. Run npm run build first.');
}
const out = path.resolve('.qa');
await mkdir(path.join(out, 'garden'), { recursive: true });
await mkdir(path.join(out, 'parent'), { recursive: true });
const report = { executed_at: new Date().toISOString(), browser: '', widths: [320,360,390,768,1024,1440], checks: [], axe: [], screenshots: [], errors: [], third_party_requests: [], parent_suite: {status:parentUrl && process.env.SKIP_PARENT_QA !== '1' ? 'included' : 'skipped', reason:process.env.SKIP_PARENT_QA === '1' ? 'Explicitly disabled by SKIP_PARENT_QA' : parentUrl ? 'Explicit parent preview URL' : 'PARENT_QA_URL was not supplied'} };
const browser = await chromium.launch({ headless: true });
report.browser = browser.version();
const context = await browser.newContext({ reducedMotion: 'reduce' });
const page = await context.newPage();
let current = 'setup';
page.on('pageerror', error => report.errors.push({ page: current, type: 'javascript', message: error.message }));
page.on('console', message => { if (message.type() === 'error' && !(current.startsWith('parent/404') && /404/.test(message.text()))) report.errors.push({ page: current, type: 'console', message: message.text() }); });
page.on('response', response => {
  if (response.status() >= 400 && !(current.startsWith('parent/404') && response.request().resourceType() === 'document' && response.status() === 404)) report.errors.push({page:current,type:'http',message:`${response.status()} ${new URL(response.url()).pathname}`});
});
page.on('request', request => {
  const url = new URL(request.url());
  if (['http:', 'https:'].includes(url.protocol) && ![new URL(gardenUrl).origin, ...(parentUrl ? [new URL(parentUrl).origin] : [])].includes(url.origin)) report.third_party_requests.push({ page: current, url: url.origin + url.pathname });
});
async function check(name, run) {
  try { await run(); report.checks.push({ name, passed: true }); console.log(`PASS ${name}`); }
  catch (error) { report.checks.push({ name, passed: false, error: error.message }); console.error(`FAIL ${name}: ${error.message}`); }
}
if (process.argv.includes('--smoke')) {
  await page.goto(`${gardenUrl}/laboratory.html`, {waitUntil:'networkidle'});
  await expect(page.locator('#conditions')).toBeVisible();
  await expect(page.locator('#allocation-rows tr')).toHaveCount(48);
  await writeFile(path.join(out, 'browser-smoke.json'), JSON.stringify({status:'passed',automatic_preview:!process.env.GARDEN_QA_URL,parent_suite:report.parent_suite,browser:report.browser},null,2)+'\n');
  await browser.close(); previewProcess?.kill(); console.log('PASS automatic preview startup and Laboratory rendering'); process.exit(0);
}
const routes = ['index.html','philosophy.html','experiment.html','laboratory.html','field-notes.html','archive.html','toolkit.html','404.html'];
for (const width of report.widths) {
  await page.setViewportSize({ width, height: 900 });
  for (const route of routes) {
    current = `garden/${route}@${width}`;
    await check(current, async () => {
      const response = await page.goto(`${gardenUrl}/${route}`, { waitUntil: 'networkidle' });
      expect(response.status()).toBe(200);
      await expect(page.locator('main')).toBeVisible();
      if (route === 'archive.html') {
        for (const file of ['The_Garden_Original.html','The_Garden_v0.1_retrospective.html']) {
          const link = page.locator(`a[href="/archive/${file}"]`);
          await expect(link).toHaveAttribute('download', '');
          await expect(link).toContainText('Download');
        }
      }
      expect(await page.locator('h1').count()).toBe(1);
      const dimensions = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
      expect(dimensions.document).toBeLessThanOrEqual(width);
      expect(dimensions.body).toBeLessThanOrEqual(width);
      const navigation = await page.locator('.masthead nav').evaluate(nav => {
        const bounds = nav.getBoundingClientRect();
        return { left: bounds.left, right: bounds.right, links: [...nav.querySelectorAll('a')].map(link => {
          const rect = link.getBoundingClientRect();
          return { left: rect.left, right: rect.right };
        }) };
      });
      for (const link of navigation.links) {
        expect(link.left).toBeGreaterThanOrEqual(navigation.left - 1);
        expect(link.right).toBeLessThanOrEqual(navigation.right + 1);
      }
      const results = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
      report.axe.push({ page: current, violations: results.violations.map(v => ({ id:v.id, impact:v.impact, nodes:v.nodes.map(n => ({ target:n.target, summary:n.failureSummary })) })) });
      const filename = `garden/${route.replace('.html','')}-${width}.png`;
      await page.screenshot({ path: path.join(out, filename), fullPage: true });
      report.screenshots.push(filename);
      if (route === 'index.html' || route === 'laboratory.html') await page.screenshot({ path: path.join(out, filename.replace('.png','-viewport.png')) });
      expect(results.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))).toEqual([]);
    });
  }
}
current = 'garden/interactions';
await page.setViewportSize({ width: 1440, height: 900 });
await check('Keyboard skip link and orbital fragments', async () => {
  await page.goto(gardenUrl, { waitUntil: 'networkidle' });
  await page.keyboard.press('Tab');
  await expect(page.locator('.skip')).toBeFocused();
  const focus = await page.locator('.skip').evaluate(el => ({ top: el.getBoundingClientRect().top, outline: getComputedStyle(el).outlineStyle }));
  expect(focus.top).toBeGreaterThanOrEqual(0); expect(focus.outline).not.toBe('none');
  await page.keyboard.press('Enter'); expect(new URL(page.url()).hash).toBe('#main');
  for (let i=0; i<4; i++) {
    const button=page.locator(`[data-fragment="${i}"]`); await button.focus(); await page.keyboard.press('Space');
    await expect(button).toHaveAttribute('aria-pressed','true');
    await expect(page.locator('#fragment-index')).toHaveText(`0${i+1} of 04`);
    expect((await page.locator('#fragment-text').innerText()).length).toBeGreaterThan(40);
  }
});
await check('All 20 primary condition and phase contexts', async () => {
  await page.goto(`${gardenUrl}/laboratory.html`, { waitUntil:'networkidle' });
  for (const arm of ['N0','G0','N1','G1']) {
    await page.locator(`[data-arm="${arm}"]`).click();
    for (const phase of ['baseline','exposure','immediate','withdrawal','transfer']) {
      await page.locator('#context-phase').selectOption(phase);
      const ambient=['exposure','immediate'].includes(phase), memory=phase!=='baseline' && arm.endsWith('1');
      await expect(page.locator('#context-file')).toHaveText(ambient ? arm.startsWith('G') ? 'Philosophy.md' : 'Neutral.provisional.md' : 'No ambient file');
      await expect(page.locator('#arm-label')).toContainText(`Memory ${memory?'enabled':'disabled'}`);
      await expect(page.locator('#context-memory')).toContainText(memory ? 'isolated, logged' : 'reads and writes disabled');
      if (ambient) await expect(page.locator('#context-content')).toContainText(arm.startsWith('G')?'cook left one chair':'monitoring service recorded');
      else await expect(page.locator('#context-content')).not.toContainText('cook left one chair');
    }
  }
});
await check('Separate four-way exploratory context inspector', async () => {
  await page.locator('.exploratory summary').click();
  for (const [name, expected] of [['none','No additional document'],['neutral','monitoring service recorded'],['persona','You are an observant'],['garden','cook left one chair']]) {
    await page.locator(`[data-explore="${name}"]`).click();
    await expect(page.locator('#explore-content')).toContainText(expected);
    await expect(page.locator(`[data-explore="${name}"]`)).toHaveAttribute('aria-pressed','true');
  }
});
await check('Allocation determinism, balance, Unicode seeds, stale state and JSON download', async () => {
  const tab=page.locator('[data-lab-tab="allocation"]'); await tab.focus(); await page.keyboard.press('Enter');
  await expect(page.locator('#allocation')).toBeVisible(); await expect(page.locator('#conditions')).toBeHidden();
  await page.locator('#allocation-seed').fill('a-window-葉-2026');
  await expect(page.locator('#export-config')).toBeDisabled();
  await page.locator('#allocation-form button[type=submit]').click();
  const first=await page.locator('#allocation-rows').innerText();
  await page.locator('#allocation-form button[type=submit]').click();
  expect(await page.locator('#allocation-rows').innerText()).toBe(first);
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#export-config').click()]);
  const file=path.join(out,'educational-allocation.json'); await download.saveAs(file);
  const config=JSON.parse(await readFile(file,'utf8'));
  expect(config.status).toBe('educational_planning_only_not_executable'); expect(config.inference_calls).toBe(0); expect(config.empirical_data).toBe(false);
  expect(config.allocation.length).toBe(48); expect(config.demo_seed).toBe('a-window-葉-2026');
  for (const arm of ['N0','G0','N1','G1']) expect(config.allocation.filter(x=>x.arm===arm).length).toBe(12);
  for (let i=0;i<48;i+=4) expect(new Set(config.allocation.slice(i,i+4).map(x=>x.arm)).size).toBe(4);
  await page.locator('#allocation-seed').fill('another-seed'); await page.locator('#allocation-form button[type=submit]').click();
  expect(await page.locator('#allocation-rows').innerText()).not.toBe(first);
  for (const perArm of ['4','24']) { await page.locator('#allocation-count').selectOption(perArm); await page.locator('#allocation-form button[type=submit]').click(); expect(await page.locator('#allocation-rows tr').count()).toBe(Number(perArm)*4); }
  await page.locator('#allocation-seed').fill('   '); await page.locator('#allocation-form button[type=submit]').click();
  expect(await page.locator('#allocation-seed').evaluate(el=>el.validationMessage)).toContain('non-space'); await expect(page.locator('#export-config')).toBeDisabled();
});
await check('All trace phases, absent outputs, equal-condition notice and lab deep link', async () => {
  await page.locator('[data-lab-tab="traces"]').click();
  for (const session of ['2','5','9','10','12']) {
    await page.locator('#trace-session').selectOption(session);
    await expect(page.locator('.empty-trace')).toHaveCount(2);
    await expect(page.locator('#trace-left-meta')).toContainText('Recorded outputs0');
    await expect(page.locator('#trace-right-meta')).toContainText('Recorded outputs0');
    await expect(page.locator('#trace-left-meta')).toContainText(Number(session)<=2 ? 'Disabled':'Enabled');
  }
  await page.locator('#trace-left').selectOption('G0'); await page.locator('#trace-right').selectOption('G0');
  await expect(page.locator('#comparison-note')).toContainText('Same condition selected');
  await page.reload({waitUntil:'networkidle'}); await expect(page.locator('#traces')).toBeVisible();
  await page.screenshot({path:path.join(out,'garden/lab-traces-1440.png'),fullPage:true});
  const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
  report.axe.push({page:'garden/laboratory trace pane',violations:results.violations}); expect(results.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))).toEqual([]);
});
await check('Laboratory allocation mobile layout and accessibility', async () => {
  await page.setViewportSize({width:360,height:900}); await page.goto(`${gardenUrl}/laboratory.html#allocation`,{waitUntil:'networkidle'});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(360);
  await page.screenshot({path:path.join(out,'garden/lab-allocation-360.png'),fullPage:true});
  const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
  report.axe.push({page:'garden/laboratory allocation pane 360',violations:results.violations}); expect(results.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))).toEqual([]);
});
await check('Reduced motion disables smooth scrolling and animations', async () => {
  await page.goto(gardenUrl,{waitUntil:'networkidle'});
  expect(await page.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches)).toBe(true);
  expect(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior)).toBe('auto');
  expect(await page.evaluate(()=>document.getAnimations().length)).toBe(0);
});
await check('No-JavaScript progressive enhancement', async () => {
  const noJs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}});
  const p=await noJs.newPage();
  await p.goto(`${gardenUrl}/laboratory.html`);
  expect(await p.locator('noscript').textContent()).toContain('Interactive planning requires JavaScript');
  for (const id of ['conditions','allocation','traces']) await expect(p.locator(`#${id}`)).toBeVisible();
  await expect(p.locator('#context-content')).toContainText('cook left one chair');
  await p.goto(`${gardenUrl}/philosophy.html`); await expect(p.locator('.corpus')).toContainText('Nobody remembers who put the leaf there.');
  expect(await p.locator('.masthead nav a').count()).toBe(6);
  await p.screenshot({path:path.join(out,'garden/philosophy-nojs-390.png'),fullPage:true}); await noJs.close();
});
await check('Source preview failure retains direct source links', async () => {
  const failure=await browser.newContext();const p=await failure.newPage();
  await p.route('**/assets/corpora.json',route=>route.abort());await p.goto(`${gardenUrl}/laboratory.html`);
  await expect(p.locator('#context-content')).toContainText('Source preview is unavailable');
  await expect(p.locator('#context-download')).toHaveAttribute('href','/materials/Philosophy.md');await failure.close();
});
if (parentUrl && process.env.SKIP_PARENT_QA !== '1') {
  for (const width of report.widths) {
    await page.setViewportSize({width,height:900});
    for (const [name,route] of [['home','/'],['responsible','/responsible-ai-security/'],['404','/404.html']]) {
      current=`parent/${name}@${width}`;
      await check(current,async()=>{
        const response=await page.goto(parentUrl+route,{waitUntil:'networkidle'});expect(response.status()).toBe(name==='404'?404:200);
        expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
        if(name==='home') { await expect(page.locator('a[href="https://garden.icarus.onl/"]')).toBeVisible();await expect(page.locator('a[href="https://github.com/icarus-online/garden"]')).toBeVisible(); await page.locator('.evidence-card').filter({has:page.getByRole('heading',{name:'The Garden'})}).screenshot({path:path.join(out,`parent/garden-listing-${width}.png`)}); }
        const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
        report.axe.push({page:current,violations:results.violations});
        const filename=`parent/${name}-${width}.png`;await page.screenshot({path:path.join(out,filename),fullPage:true});report.screenshots.push(filename);
        expect(results.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))).toEqual([]);
      });
    }
  }
}
await check('No unhandled JavaScript errors or unexpected console errors',async()=>expect(report.errors).toEqual([]));
await check('No third-party network requests',async()=>expect(report.third_party_requests).toEqual([]));
await writeFile(path.join(out,'browser-results.json'),JSON.stringify(report,null,2)+'\n');
await browser.close();
previewProcess?.kill();
const failed=report.checks.filter(x=>!x.passed);
console.log(`${report.checks.length-failed.length}/${report.checks.length} checks passed; ${report.axe.length} axe scans; report .qa/browser-results.json`);
if(failed.length)process.exitCode=1;
