# Browser and interface QA — 2026-10-22

**Result:** the final local browser suite passed 66 of 66 checks. All 57 automated axe scans reported zero WCAG 2.0/2.1 A/AA violations. This validates the public interface and offline planning controls; it does not constitute an experimental study or production deployment verification.

## Executed matrix

Chromium 156.0.8078.4, using Playwright 1.64.1 and axe-core 4.14.0, exercised these widths with a 900-pixel viewport height: **360, 390, 768, 1024, and 1440 pixels**.

| Surface | Routes | Executed coverage |
|---|---|---|
| Garden | Home, philosophy, experiment, laboratory, field notes, archive, toolkit, 404 document | All eight routes at all five widths; main landmark and heading, HTTP response, horizontal overflow, axe scan, and screenshots |
| Icarus parent site | Home, responsible AI/security, 404 | All three routes at all five widths; Garden/repository links on home, expected HTTP status, horizontal overflow, axe scan, and screenshots |
| Additional lab states | Allocation at 360 pixels; trace comparison at desktop width | Layout and axe scans, beyond the default conditions pane |

The parent 404 route correctly returns HTTP 404. That intentional document response is distinguished from unexpected asset failures. No unhandled JavaScript errors, unexpected console/HTTP errors, or third-party network requests occurred in the final suite.

## Functional checks executed

- Keyboard skip link, visible focus, Enter activation, and Space activation of all four orbital fragments.
- All **20 combinations** of four primary conditions and five phases. Baseline disables memory in every arm; withdrawal and transfer remove the original ambient file. Memory-enabled histories remain explicitly distinguished from the original file.
- The separate four-way exploratory inspector: no document, neutral text, persona instructions, and ambient philosophy.
- Allocation repeatability using an identical Unicode seed, changed-seed divergence, four-arm balance in every block, and 16/48/96 trajectory selections.
- Downloaded demonstration JSON checked for its educational/non-executable status, zero inference calls, false empirical-data flag, seed, count, and balanced assignments. Editing inputs disables stale export; whitespace-only input produces a validation message.
- All five trace phases, explicit zero-output states, same-condition comparison warning, and laboratory deep-link persistence after reload.
- Reduced-motion preference, disabled smooth scrolling, and absence of active animations.
- JavaScript disabled: accessible explanatory notice, all three laboratory sections visible, static source material available, and ordinary navigation preserved.
- Failed corpus-preview request: explicit unavailable state and a usable direct source link.

The browser’s educational FNV/xorshift allocation was tested as a teaching instrument. It is intentionally different from the research toolkit’s SHA-256 allocator and is not treated as an executable research configuration.

## Visual review and corrections

Screenshots were captured for every matrix entry. Representative screenshots were visually inspected across all five widths, including the Garden home, pale Laboratory, source-corpus page, experimental sequence, field notes, toolkit, and parent research listing. The inspection checked text rendering, hierarchy, responsive reflow, clipping, contrast, and separation between the artistic and analytical modes.

The initial rendered pass found a header link whose redundant accessible name omitted its visible tagline. Removing that attribute fixed the axe finding across all eight pages. A desktop heading size was adjusted after visual inspection to preserve the intended two-line composition. The affected pages were rebuilt and the complete matrix rerun successfully.

The minimal QA host initially lacked fonts and fontconfig; Chromium rendered invisible text and exited. Local, ignored test dependencies were supplied before the valid run. No conclusions are drawn from that invalid initial rendering. The website itself uses system font stacks and requires no font CDN.

Historical prototype links were subsequently changed to explicit HTML downloads, preserving the originals while avoiding a broken inline-script experience under the current strict Content Security Policy. A focused follow-up passed at all five widths: zero violations in five additional axe scans, no horizontal overflow, and both historical HTML links triggered actual browser downloads with the expected filenames. Targeted parent-listing screenshots were also captured at all five widths. The follow-up evidence is `.qa/archive-followup.json`. A small spacing issue in the parent listing was then corrected by its owner. A focused 390/1440-pixel follow-up measured a 12-pixel gap between the links, found no horizontal overflow, and passed two further full-homepage axe scans. Updated listing screenshots were visually inspected; evidence is `.qa/parent-spacing-followup.json`.

## Reproduction and evidence

Run `npm ci`, install a compatible Playwright Chromium browser and its operating-system dependencies, and run `npm run check`. Run `npm run qa:browser`; it starts an isolated Garden preview automatically and cleans it up on completion or exit. The default suite is independent of the parent repository. `npm run qa:browser -- --smoke` verifies automatic startup and Laboratory rendering without repeating the full matrix.

`GARDEN_QA_URL` reuses a separately started Garden preview. The parent suite runs only when `PARENT_QA_URL` is explicitly supplied; otherwise its skipped status is recorded. The complete 66-check run used Garden port 4178 and parent port 4177. `SKIP_PARENT_QA=1` can explicitly disable an otherwise configured parent suite. The script also recognizes optional ignored local browser, library, and font directories on minimal hosts.

The automatic-preview startup smoke test also passed, with the unconfigured parent suite accurately recorded as skipped in `.qa/browser-smoke.json`.

The local evidence consists of `.qa/browser-results.json`, `.qa/garden/`, and `.qa/parent/`. These generated screenshots and logs are ignored by Git and excluded from public deployment artifacts. The reproducible suite is `scripts/browser-qa.mjs`.

The build, static-link/artifact validation, syntax checks, JavaScript type checking, all **27 research/allocation Python tests**, and **six deployment installer tests** also passed during the final QA build.

## Limits

This was Chromium testing against local static previews. It is not a claim of cross-browser certification, a human screen-reader session, mobile-device hardware testing, production network performance, or public DNS/TLS verification. Automated accessibility checks and keyboard checks do not prove complete accessibility. Real inference, provider-specific state isolation, empirical trace ingestion, and scientific data collection are outside this browser suite and remain separate research milestones.
