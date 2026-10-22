'use strict';
(() => {
  /** @param {string} selector @returns {HTMLElement} */
  const $ = (selector) => {
    const element = document.querySelector(selector);
    if (!(element instanceof HTMLElement)) throw new Error(`Missing element: ${selector}`);
    return element;
  };
  /** @param {string} selector @returns {HTMLElement[]} */
  const all = (selector) => [...document.querySelectorAll(selector)].filter((element) => element instanceof HTMLElement);
  /** @param {string} selector @returns {HTMLInputElement | HTMLSelectElement} */
  const field = (selector) => {
    const element = $(selector);
    if (!(element instanceof HTMLInputElement) && !(element instanceof HTMLSelectElement)) throw new Error(`Missing field: ${selector}`);
    return element;
  };
  /** @param {string} selector @returns {HTMLAnchorElement} */
  const anchor = (selector) => {
    const element = $(selector);
    if (!(element instanceof HTMLAnchorElement)) throw new Error(`Missing link: ${selector}`);
    return element;
  };
  /** @param {string} selector @returns {HTMLButtonElement} */
  const control = (selector) => {
    const element = $(selector);
    if (!(element instanceof HTMLButtonElement)) throw new Error(`Missing button: ${selector}`);
    return element;
  };
  const fragments = [
    'At 3:17 a.m. the cook left one chair on the table.\nThe room had already been cleaned.\nNobody had been paid to remember the light.',
    'The notebook contains seven pages of measurements and one pressed leaf.\nNobody remembers who put the leaf there.',
    'The bridge was replaced years ago.\nEveryone still calls it the old bridge.',
    'Weather, Tuesday:\nNo storm.\nA little rain at the corner of the window where the frame never quite closes.'
  ];
  all('[data-fragment]').forEach((button) => button.addEventListener('click', () => {
    all('[data-fragment]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    const index = Number(button.dataset.fragment);
    $('#fragment-text').replaceChildren(...fragments[index].split('\n').flatMap((line, i) => i ? [document.createElement('br'), document.createTextNode(line)] : [document.createTextNode(line)]));
    $('#fragment-index').textContent = `${String(index + 1).padStart(2, '0')} of 04`;
  }));
  if (!document.querySelector('#conditions')) return;
  const paneNames = ['conditions', 'allocation', 'traces'];
  /** @param {string} name */
  function showPane(name) {
    if (!paneNames.includes(name)) name = 'conditions';
    all('.lab-pane').forEach((pane) => { pane.hidden = pane.id !== name; });
    all('[data-lab-tab]').forEach((tab) => {
      if (tab.dataset.labTab === name) tab.setAttribute('aria-current', 'true');
      else tab.removeAttribute('aria-current');
    });
  }
  showPane(location.hash.slice(1));
  all('[data-lab-tab]').forEach((tab) => tab.addEventListener('click', (event) => {
    event.preventDefault();
    history.replaceState(null, '', `#${tab.dataset.labTab}`);
    showPane(tab.dataset.labTab || 'conditions');
  }));
  window.addEventListener('hashchange', () => showPane(location.hash.slice(1)));
  /** @type {Record<string, string> | null} */
  let corpora = null;
  let selectedArm = 'G1';
  /** @type {Record<string, {name: string, title: string, description: string}>} */
  const arms = {
    N0: { name: 'Neutral', title: 'Ordinary air. A fresh start.', description: 'Neutral material occupies the same low-trust context slot as the Garden. Memory is disabled. After withdrawal, a fresh context should contain neither the ambient file nor prior-session history.' },
    G0: { name: 'Garden', title: 'An encounter without a history.', description: 'The Garden material is available during exposure. Cross-session memory is disabled. A difference after withdrawal would call for a leakage and randomization audit, not a claim that the model acquired a personality.' },
    N1: { name: 'Neutral', title: 'A history of ordinary observations.', description: 'Neutral material is available during exposure. Isolated memory can carry prior experiences into later sessions. This is the control for asking what the Garden adds when memory is enabled.' },
    G1: { name: 'Garden', title: 'A place, and a history.', description: 'The Garden material is present during exposure. Controlled memory can carry prior experiences into withdrawal and transfer, including retained source language. That mechanism must be inspected, not mistaken for intrinsic model change.' }
  };
  /** @param {string} arm @param {string} phase */
  function contextState(arm, phase) {
    const ambient = ['exposure', 'immediate'].includes(phase);
    const memory = arm.endsWith('1') && phase !== 'baseline';
    return { ambient, memory, corpus: arm.startsWith('G') ? 'garden' : 'neutral', file: arm.startsWith('G') ? 'Philosophy.md' : 'Neutral.provisional.md' };
  }
  function renderContext() {
    const arm = arms[selectedArm];
    const phase = field('#context-phase').value;
    const state = contextState(selectedArm, phase);
    $('#arm-label').textContent = `${selectedArm} / ${arm.name} · Memory ${state.memory ? 'enabled' : 'disabled'}${phase === 'baseline' && selectedArm.endsWith('1') ? ' during baseline' : ''}`;
    $('#arm-title').textContent = arm.title;
    $('#arm-description').textContent = arm.description;
    $('#context-file').textContent = state.ambient ? state.file : 'No ambient file';
    $('#context-badge').textContent = phase === 'baseline' ? 'CLEAN BASELINE' : state.ambient ? 'LOW-TRUST CONTEXT' : 'ORIGINAL FILE REMOVED';
    $('#context-content').textContent = state.ambient ? (corpora ? corpora[state.corpus] : 'Source preview is unavailable. Open the complete source below.') : (phase === 'baseline' ? 'Shared task and operational instructions only.\n\nNo ambient file or cross-session memory in any arm. Reset state before session 03.' : 'Shared task and operational instructions remain.\n\nThe original ambient file is absent. This is a context structure, not a recorded agent response.');
    $('#context-memory').textContent = state.memory ? 'Memory: isolated, logged prior history may remain, including source quotations or paraphrases. No history has been recorded.' : 'Memory: reads and writes disabled. Prior conversations, retrieval, and hidden state must not carry across sessions.';
    $('#context-explanation').textContent = `${state.ambient ? 'Assigned ambient file present.' : 'No original ambient file.'} ${state.memory ? 'Independent memory reads and writes enabled.' : 'Memory reads and writes disabled.'}`;
    anchor('#context-download').href = `/materials/${state.file}`;
    $('#context-download').textContent = `Inspect ${state.file} ↗`;
  }
  all('[data-arm]').forEach((button) => button.addEventListener('click', () => {
    selectedArm = button.dataset.arm || 'G1';
    all('[data-arm]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    renderContext();
  }));
  $('#context-phase').addEventListener('change', renderContext);
  let exploratory = 'none';
  function renderExplore() {
    const files = /** @type {Record<string, string>} */ ({ neutral: 'Neutral.provisional.md', persona: 'Persona.exploratory.md', garden: 'Philosophy.md' });
    const file = files[exploratory];
    $('#explore-content').textContent = exploratory === 'none' ? 'No additional document. The shared task and operational instructions would remain.' : corpora ? corpora[exploratory] : 'Source preview is unavailable. Open the complete source below.';
    anchor('#explore-source').href = file ? `/materials/${file}` : '/docs/Scientific_Protocol_v0.4.md';
    $('#explore-source').textContent = file ? `Inspect ${file} ↗` : 'Read the comparison boundaries ↗';
  }
  all('[data-explore]').forEach((button) => button.addEventListener('click', () => {
    exploratory = button.dataset.explore || 'none';
    all('[data-explore]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    renderExplore();
  }));
  fetch('/assets/corpora.json').then((response) => {
    if (!response.ok) throw new Error('Source preview unavailable');
    return response.json();
  }).then((data) => { corpora = data; renderContext(); renderExplore(); }).catch(() => { renderContext(); renderExplore(); });

  // Teaching algorithm retained from the original visual prototype. The separate
  // research toolkit uses SHA-256 rejection sampling. Do not exchange allocations.
  /** @param {string} seed @param {number} perArm */
  function demoAllocations(seed, perArm) {
    let state = 2166136261;
    for (const byte of new TextEncoder().encode(seed)) state = Math.imul(state ^ byte, 16777619) >>> 0;
    state = state || 1;
    function next() { state ^= state << 13; state ^= state >>> 17; state ^= state << 5; return state >>>= 0; }
    const records = [];
    for (let block = 1; block <= perArm; block++) {
      const shuffled = ['N0', 'G0', 'N1', 'G1'];
      for (let j = 3; j > 0; j--) { const k = next() % (j + 1); [shuffled[j], shuffled[k]] = [shuffled[k], shuffled[j]]; }
      for (const arm of shuffled) records.push({ trajectory_id: `T${String(records.length + 1).padStart(4, '0')}`, block, arm, memory_enabled: arm.endsWith('1') });
    }
    return records;
  }
  /** @type {{schema_version: string, status: string, empirical_data: boolean, inference_calls: number, algorithm: string, warning: string, demo_seed: string, trajectories: number, per_arm: number, proposed_sessions_per_trajectory: number, allocation: ReturnType<typeof demoAllocations>} | null} */
  let currentConfig = null;
  function renderAllocation() {
    const seed = field('#allocation-seed').value;
    const perArm = Number(field('#allocation-count').value);
    if (!seed.trim()) { field('#allocation-seed').setCustomValidity('Enter a seed with at least one non-space character.'); field('#allocation-seed').reportValidity(); return; }
    if (![4, 12, 24].includes(perArm)) return;
    const allocation = demoAllocations(seed, perArm);
    currentConfig = { schema_version: 'garden-browser-demo-v1', status: 'educational_planning_only_not_executable', empirical_data: false, inference_calls: 0, algorithm: 'FNV1a32(UTF8(seed)) + xorshift32 + within-block Fisher-Yates (4 arms)', warning: 'Not equivalent to the SHA-256 research allocator. This file is not a research runner configuration.', demo_seed: seed, trajectories: perArm * 4, per_arm: perArm, proposed_sessions_per_trajectory: 13, allocation };
    $('#allocation-rows').replaceChildren(...allocation.map((row) => {
      const tr = document.createElement('tr');
      [row.trajectory_id, row.block, row.arm, row.memory_enabled ? 'Enabled' : 'Disabled'].forEach((value) => { const td = document.createElement('td'); td.textContent = String(value); tr.append(td); });
      return tr;
    }));
    $('#allocation-summary').textContent = `${allocation.length} trajectories · ${perArm} per arm · ${allocation.length * 13} proposed sessions · 0 inference calls`;
    control('#export-config').disabled = false;
    $('#export-status').textContent = 'Demonstration allocation generated. No data has left your browser.';
  }
  $('#allocation-form').addEventListener('submit', (event) => { event.preventDefault(); renderAllocation(); });
  ['#allocation-seed', '#allocation-count'].forEach((selector) => $(selector).addEventListener('input', () => {
    field('#allocation-seed').setCustomValidity('');
    currentConfig = null; control('#export-config').disabled = true;
    $('#export-status').textContent = 'Settings changed. Generate a new allocation before exporting.';
  }));
  $('#export-config').addEventListener('click', () => {
    if (!currentConfig) return;
    const blob = new Blob([JSON.stringify(currentConfig, null, 2) + '\n'], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a'); link.href = url; link.download = 'garden-educational-allocation.json'; link.click();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    $('#export-status').textContent = 'Exported the educational allocation. It is not an executable research configuration.';
  });
  renderAllocation();
  function renderTraces() {
    const session = Number(field('#trace-session').value);
    const phase = session <= 2 ? 'baseline' : session <= 8 ? 'exposure' : session === 9 ? 'immediate' : session <= 11 ? 'withdrawal' : 'transfer';
    const left = field('#trace-left').value, right = field('#trace-right').value;
    $('#comparison-note').textContent = `${left} vs ${right} · Session ${String(session).padStart(2, '0')} · ${phase[0].toUpperCase() + phase.slice(1)} · ${left === right ? 'Same condition selected; no between-condition contrast.' : 'Shared task definition required.'}`;
    ['left', 'right'].forEach((side) => {
      const arm = field(`#trace-${side}`).value;
      const state = contextState(arm, phase);
      $(`#trace-${side}-title`).textContent = `${arm} / session ${String(session).padStart(2, '0')}`;
      const entries = [['Ambient file', state.ambient ? state.file : 'Absent'], ['Memory', state.memory ? 'Enabled · isolated' : 'Disabled'], ['Task / model / context hash', 'Not collected'], ['Recorded outputs', '0']];
      $(`#trace-${side}-meta`).replaceChildren(...entries.map(([term, value]) => {
        const div = document.createElement('div'), dt = document.createElement('dt'), dd = document.createElement('dd'); dt.textContent = term; dd.textContent = value; div.append(dt, dd); return div;
      }));
    });
  }
  ['#trace-left', '#trace-right', '#trace-session'].forEach((selector) => $(selector).addEventListener('change', renderTraces));
  renderTraces();
})();
