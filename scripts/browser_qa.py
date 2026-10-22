"""Lightweight visual and functional smoke test. Needs Playwright + Chromium.

Navigations are disabled in some research sandboxes. set_content() tests the
self-contained page without making network calls. Resource links are checked
separately by the packaging tool.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from make_allocations import make_allocations

root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
 for label,viewport in [('desktop',{'width':1440,'height':900}),('mobile',{'width':390,'height':844})]:
  page=browser.new_page(viewport=viewport, device_scale_factor=1, accept_downloads=True)
  errors=[]
  page.on('pageerror',lambda error: errors.append(str(error)))
  page.set_content((root/'index.html').read_text(),wait_until='load')
  page.screenshot(path=str(root/'preview'/f'The_Garden_Icarus_{label}_hero.png'),full_page=False)
  page.screenshot(path=str(root/'preview'/f'The_Garden_Icarus_{label}_full.png'),full_page=True)
  layout=page.evaluate('({inner:window.innerWidth,scroll:document.documentElement.scrollWidth,height:document.body.scrollHeight})')
  assert layout['scroll']==layout['inner'],f'Horizontal overflow at {label}: {layout}'
  assert page.locator('button[data-source]').count()==10
  page.locator('button[data-source="9"]').click()
  assert 'sign' in page.locator('#sourceQuote').inner_text().lower()
  page.locator('button[data-condition="3"]').click()
  assert 'G1' in page.locator('#conditionType').inner_text()
  page.locator('button[data-phase="2"]').click()
  assert 'Close the window' in page.locator('#phaseName').inner_text()
  page.locator('button[data-interpret="2"]').click()
  assert 'boundary' in page.locator('#interpretHeadline').inner_text().lower()
  page.locator('#allocCount').select_option('3')
  page.locator('#allocSeed').fill('test-comparison')
  page.locator('#generateAlloc').click()
  assert page.locator('#allocSummary').inner_text().startswith('12 trajectories')
  browser_arms=page.locator('#allocBody tr td:nth-child(3)').all_inner_texts()
  cli_arms=[r['arm'] for r in make_allocations('test-comparison',3)]
  assert browser_arms == cli_arms,(browser_arms,cli_arms)
  with page.expect_download() as event:page.locator('#downloadAlloc').click()
  dl=event.value
  assert dl.suggested_filename=='garden_PRIVATE_allocation_demo.csv'
  assert not errors, errors
  page.locator('#instruments').screenshot(path=str(root/'preview'/f'The_Garden_Icarus_{label}_lab.png'))
  print(f'{label}: visual fit PASS; all interactive controls PASS; JS/Python randomization MATCH; CSV export PASS; JS errors 0')
  page.close()
 browser.close()
