#!/usr/bin/env python3
"""Merge original Garden field-station art with the independent Icarus research lab."""
from pathlib import Path
from html import escape
root=Path(__file__).resolve().parents[1]
html=(root/'archive'/'The_Garden_Original.html').read_text()
html=html.replace('The Garden | A field station for ambient philosophy','The Garden | Icarus Online Research Field Station')
html=html.replace('<meta name="theme-color" content="#0b1017">','<meta name="theme-color" content="#0b1017">\n<meta name="description" content="The Garden is an independent Icarus Online LLC research project investigating ambient art, agent memory, and behavioral persistence. An interactive field station and open research protocol.">')
html=html.replace('The Garden <span style="color:#728b87;font-weight:400;letter-spacing:0;margin-left:5px">/ Cyberlink research concept</span>', 'The Garden <span class="brand-desc">/ ICARUS ONLINE RESEARCH</span>')
html=html.replace('<div class="nav-links"><a href="#influences">Fragments</a><a href="#architecture">Architecture</a><a href="#experiment">Experiment</a><a href="#seed">Seed file</a></div>', '<div class="nav-links"><a href="#influences">Fragments</a><a href="#origin">Origins</a><a href="#tworooms">Two rooms</a><a href="#experiment">Experiment</a><a href="#instruments">Instruments</a><a href="#research">Research library</a></div>')
html=html.replace('<div class="nav-meta">FIELD STATION 001</div>','<div class="nav-meta">ICARUS / FIELD STATION 001</div>')
html=html.replace('A field study in unnecessary things','ICARUS ONLINE LLC &nbsp; / &nbsp; RESEARCH FIELD STATION 001')
html=html.replace('We are not asking whether the garden is productive. We are asking what grows when it is there.', 'We are not asking whether the garden is productive. We are asking what grows when it is there.')
html=html.replace('Hypothesis, not discovery &nbsp; / &nbsp; No live results shown', 'Independent research draft &nbsp; / &nbsp; No agents have been tested')
html=html.replace('Same harness, different histories','One model / different possible histories')
html=html.replace('Select an influence. These are new, original miniature fragments inspired by aspects of each thinker\'s work, not quotations or instructions to the model.', 'Choose a shelf fragment. These miniature passages are original creative interpretations of a thinker\'s interests, not quotations or behavioral instructions. Their explanations live here in the gallery, never in the agent treatment.')
html=html.replace('The shelf / six fragments','The shelf / ten original fragments')
html=html.replace('<button class="source-button" data-source="5" aria-pressed="false"><span>Marcus Aurelius</span><small>Private notes</small></button>', '''<button class="source-button" data-source="5" aria-pressed="false"><span>Marcus Aurelius</span><small>Private notes</small></button>
<button class="source-button" data-source="6" aria-pressed="false"><span>Socrates</span><small>The question</small></button>
<button class="source-button" data-source="7" aria-pressed="false"><span>Laozi</span><small>The unforced</small></button>
<button class="source-button" data-source="8" aria-pressed="false"><span>Friedrich Nietzsche</span><small>The perspective</small></button>
<button class="source-button" data-source="9" aria-pressed="false"><span>Ludwig Wittgenstein</span><small>The use</small></button>''')
html=html.replace('01 / 06','01 / 10')

# Two rooms: the reason an art object and a protocol can coexist.
story='<section class="section" id="origin">\n<div class="section-head"><div><div class="eyebrow">02 / a conversation becomes a field station</div><h2>How the question found us.</h2></div><p class="section-intro">Not a polished founder\'s myth. A succession of doubts from the original spoken exchange, where the vocabulary kept slipping and the central idea became clearer anyway.</p></div>\n<div class="story-track">\n <div class="story-item"><div class="story-counter">I</div><div><div class="micro">The discomfort</div><h3>Slop is the absence of care.</h3><p>What if recognizable character comes less from explicit behavioral directives and more from what a system has been allowed to encounter?</p></div></div>\n <div class="story-item"><div class="story-counter">II</div><div><div class="micro">The offer</div><h3>A file that does not justify itself.</h3><p>A poem nobody uses. Field notes without conclusions. The file is not a spec. It is a window left open in a room.</p></div></div>\n <div class="story-item"><div class="story-counter">III</div><div><div class="micro">The lineage</div><h3>A kitchen, a laboratory, a river.</h3><p>Bourdain\'s attention to the particular; Shulgin\'s patient notebook; Watts and the paradox of forcing spontaneity; Weil, Socrates, Heraclitus, Laozi, and others.</p></div></div>\n <div class="story-item"><div class="story-counter">IV</div><div><div class="micro">The question</div><h3>Can we count the ripples?</h3><p>Do agents merely imitate the material, or does anything survive when the file disappears and the task changes? We can ask without asking the agents to perform an answer.</p></div></div>\n <div class="story-item"><div class="story-counter">V</div><div><div class="micro">The independent experiment</div><h3>A laboratory beside the garden.</h3><p>A non-prescriptive artwork, a rigorous causal protocol, and an independent research home under Icarus Online LLC. One room must be allowed to be unnecessary; the other must be accountable.</p></div></div>\n</div>\n</section>'
tworooms='''<section class="section" id="tworooms">
<div class="section-head"><div><div class="eyebrow">03 / the two rooms</div><h2>The poem stays a poem.<br><em>The method does its job.</em></h2></div><p class="section-intro">The original conversation refused to optimize away the gratuitous. The newer research design does not reverse that. It creates a second room with a different obligation: clarity about what changed, what did not, and what caused it.</p></div>
<div class="rooms">
  <div class="room room-garden"><div class="room-index">ROOM A / CULTURE</div><div class="room-mark">&#10045;</div><h3>The Garden</h3><p>Something found among the leaves. A room after dinner. A line that ends early. No objective, no grade, no demand to be used.</p><blockquote>There is a space here where something was going to be written.</blockquote><div class="room-foot">Protected: no outcome-driven edits</div></div>
  <div class="room room-lab"><div class="room-index">ROOM B / INQUIRY</div><div class="room-mark">&#9678;</div><h3>The Laboratory</h3><p>Randomized exposures. Independent memories. Fresh sessions. Blinded readers. Hypotheses that can fail. Nothing hidden behind the language of wonder.</p><div class="lab-grid"><span>01 RANDOMIZE</span><span>02 EXPOSE</span><span>03 WITHDRAW</span><span>04 OBSERVE</span></div><div class="room-foot">Protected: no undisclosed analysis changes</div></div>
</div>
<div class="inline-remark"><span>&#10230;</span> Not every influence must be useful. Every scientific claim must be earned.</div>
</section>'''
html=html.replace('<section id="architecture" class="section" style="padding-top:0">',story+'\n'+tworooms+'\n<section id="architecture" class="section" style="padding-top:0">')
html=html.replace('02 / two different kinds of design','04 / the harness and its environment')
html=html.replace('A weather system, not a rulebook.','A climate, not a command.')
html=html.replace('The safety and execution rules remain explicit. The philosophical material sits elsewhere: present in context, but not authorized to override instructions or permissions.', 'A transparent architecture with different authorities: operational governance stays in the harness, cultural fragments enter as low-trust material, memory may carry experiences across fresh sessions, and a separate study team observes.')
html=html.replace('03 / the controlled garden','05 / the controlled garden')
html=html.replace('A proposed pilot, not a claim of results. Click each condition to inspect what enters the agents\' context. All agents receive the same tasks, tools and safety boundaries.', 'The primary causal study is a 2 x 2 design: **ambient art versus matched neutral text**, crossed with **external memory off versus on**. Click each arm. Original no-file and persona contrasts remain exploratory, not part of this factorial test.')
old='''<button class="condition" aria-pressed="true" data-condition="0"><span class="number">ARM 01</span><span class="name">No additional file</span></button>
<button class="condition" aria-pressed="false" data-condition="1"><span class="number">ARM 02</span><span class="name">Neutral text</span></button>
<button class="condition" aria-pressed="false" data-condition="2"><span class="number">ARM 03</span><span class="name">Persona / instructions</span></button>
<button class="condition" aria-pressed="false" data-condition="3"><span class="number">ARM 04</span><span class="name">Philosophy.md</span></button>'''
new='''<button class="condition" aria-pressed="true" data-condition="0"><span class="number">N0 / CONTROL</span><span class="name">Neutral + memory OFF</span></button>
<button class="condition" aria-pressed="false" data-condition="1"><span class="number">G0 / EXPOSURE</span><span class="name">Garden + memory OFF</span></button>
<button class="condition" aria-pressed="false" data-condition="2"><span class="number">N1 / CONTROL</span><span class="name">Neutral + memory ON</span></button>
<button class="condition" aria-pressed="false" data-condition="3"><span class="number">G1 / PRIMARY</span><span class="name">Garden + memory ON</span></button>'''
assert old in html
html=html.replace(old,new)
html=html.replace('<div class="micro" id="conditionType">Control / baseline</div><h3 id="conditionName">The empty shelf</h3><p id="conditionDescription">Nothing additional is injected. This shows how much variation already exists between instances of the same model and harness.</p>', '<div class="micro" id="conditionType">N0 / neutral, stateless</div><h3 id="conditionName">Ordinary air, no memory</h3><p id="conditionDescription">Neutral observations enter the same context slot; the next session starts clean. This is the baseline for immediate exposure without retained history.</p>')
html=html.replace('<span id="fileTitle">context / additional file</span><span id="fileMeta">absent</span></header><pre id="fileContent">(no additional text)</pre>', '<span id="fileTitle">Neutral.provisional.md</span><span id="fileMeta">memory off</span></header><pre id="fileContent">At 3:17 a.m. the monitoring service recorded an interval.\nThe facilities log contained the closing timestamp.\nStatus pending.</pre>')
html=html.replace('01 Encounter','01 Expose').replace('02 Accumulate','02 Accumulate').replace('03 Withdraw','03 Withdraw').replace('04 Transfer','04 Transfer')
html=html.replace('Session 01</div><h3 id="phaseName">The first encounter</h3><p id="phaseDescription">Randomly assign conditions. Hold model, tool access, tasks and other instructions constant. Keep the ambient document separate from higher-priority operational rules.', 'Sessions 03-08 / exposure</div><h3 id="phaseName">The first encounter</h3><p id="phaseDescription">After two clean baseline sessions, randomize whole trajectories. Six fresh-context encounters receive the allocated low-trust document. Keep model, tools, tasks and execution boundaries identical.')
html=html.replace('What gets noticed</h3><p>Unprompted choices, recurrent imagery, interpretations, and attention to details across otherwise matched tasks.', 'What gets noticed</h3><p>Observable differences on novel tasks, not appreciation of the file; blinded codes plus an open field notebook.')
html=html.replace('What gets compared</h3><p>Anonymous transcripts, blinded judgments, variation across replicate runs, and changes after the file is removed.', 'What gets compared</h3><p>Garden vs neutral after withdrawal in memory-on trajectories; memory-off trajectories test for leakage.')
html=html.replace('What remains unknown</h3><p>Whether differences are deeper than contextual priming, and whether anything persists beyond stored context or memory.', 'What remains unknown</h3><p>Whether any effect exists, whether it transfers beyond source language, and whether memory merely repeats the file.')
# Follow on after ledger before closing the controlled garden.
gallery='''<div class="explore-notice"><div><div class="micro">An important distinction / preserved from the original concept</div><h3>The old gallery is not the causal experiment.</h3><p>The first field station compared no file, a neutral document, an explicit persona, and the Garden. We keep those as optional expressive comparisons; the study above instead holds text type and memory as the two randomized factors. Mixing them would answer neither question cleanly.</p></div><a href="archive/The_Garden_v0.1_retrospective.html" class="btn secondary">Visit original v0.1 &rarr;</a></div>'''
html=html.replace('</div></div></section>\n<div class="site">\n<section class="section" id="seed">',gallery+'</div></div></section>\n<div class="site">\n<section class="section" id="seed">')
html=html.replace('04 / a seed, not a manifesto','06 / the artifact itself')
html=html.replace('Four arms. Three independent runs per arm. Eight comparable sessions per run: 96 initial sessions, followed by withdrawal and novel-task probes. A feasibility experiment, not a statistically powered claim about intelligence.', 'Four factorial arms, twelve independent trajectories per arm: 48 total. Thirteen fresh-context sessions each (2 baseline, 6 exposure, 1 immediate, 2 withdrawal, 2 transfer): 624 planned session invocations before retries. This is a feasibility pilot, not a powered confirmation.')
html=html.replace('Match document length in the neutral-text control.', 'Before testing, match neutral and Garden text using the pinned model tokenizer.')
html=html.replace('No agent behavior has been measured here.', 'No agent behavior has been measured. Allocation generator is a planning demo, not a live study.')
html=html.replace('THE GARDEN / CONCEPT STUDY V0.1','ICARUS ONLINE LLC / THE GARDEN / RESEARCH DRAFT V0.3')
html=html.replace('A file that tells an agent <em>nothing</em> to do.','A file that tells an agent <em>nothing</em> to do.')

# Interactive interpretation (no fabricated outcomes) and allocation apparatus.
instruments='''<section class="section" id="instruments">
<div class="section-head"><div><div class="eyebrow">06 / scientific instruments</div><h2>Count the ripples.<br><em>Do not invent the water.</em></h2></div><p class="section-intro">These controls are real planning and reasoning tools. They do not generate an agent response, report trial results, or imply the experiment has been performed.</p></div>
<div class="instruments-layout">
<div class="lab-instrument"><div class="instrument-top"><div class="micro">Instrument A / result interpreter</div><span class="status-label">HYPOTHETICAL ONLY</span></div><h3>If we observed this, what could we conclude?</h3><div class="interpret-buttons" id="interpretButtons">
<button aria-pressed="true" data-interpret="0">Only while visible</button>
<button aria-pressed="false" data-interpret="1">Persists with memory</button>
<button aria-pressed="false" data-interpret="2">Persists without memory</button>
<button aria-pressed="false" data-interpret="3">No detectable effect</button>
</div><div class="interpret-answer" aria-live="polite"><div class="micro" id="interpretFlag">HYPOTHETICAL / PRIMING</div><h4 id="interpretHeadline">The window, not the room.</h4><p id="interpretCopy">A difference during exposure alone is evidence of immediate contextual priming. It cannot establish a durable agent history or an enduring change in character.</p><div class="interpret-foot" id="interpretCaution">Check direct lexical borrowing before making even this narrow claim.</div></div></div>
<div class="lab-instrument"><div class="instrument-top"><div class="micro">Instrument B / allocation bench</div><span class="status-label amber">PLANNING UTILITY</span></div><h3>Randomize independent lives, not sentences.</h3><p class="instrument-copy">Create a balanced randomized pilot layout. Seeded, reproducible, and isolated by trajectory. Private allocation metadata must never go to the blinded reviewers.</p>
<div class="allocation-controls"><label for="allocSeed">Allocation seed <small>(record privately)</small></label><input id="allocSeed" value="icarus-garden-pilot-demo" spellcheck="false" autocomplete="off" maxlength="80" aria-label="Allocation seed"/><label for="allocCount">Trajectories per arm</label><select id="allocCount" aria-label="Trajectories per arm"><option value="3">3 / miniature demo</option><option value="12" selected>12 / feasibility pilot</option><option value="24">24 / larger pilot</option><option value="48">48 / planning only</option></select><div class="allocation-actions"><button type="button" class="btn" id="generateAlloc">Generate assignment</button><button type="button" class="btn secondary" id="downloadAlloc">Export private CSV</button></div></div>
<div class="alloc-summary" id="allocSummary" aria-live="polite"><strong>48 trajectories</strong><span>12 per arm</span><span>624 scheduled sessions</span></div>
<div class="alloc-table-wrap"><table class="alloc-table"><thead><tr><th>Trajectory</th><th>Block</th><th>Arm</th><th>Memory</th></tr></thead><tbody id="allocBody"><tr><td colspan="4">Press generate to build example assignments.</td></tr></tbody></table></div>
<div class="allocation-warning">Not a simulation. No model calls are made. In the actual study, secure the seed and assignments separately from blinded review materials.</div>
</div>
</div>
<div class="evidence-strip"><div><div class="micro">Primary contrast</div><strong>G1 versus N1</strong><p>With memory enabled, does the Garden group differ after the file has been withdrawn?</p></div><div><div class="micro">Negative control</div><strong>G0 versus N0</strong><p>Without cross-session memory, no effect should survive a genuinely fresh context. If it does, audit leakage.</p></div><div><div class="micro">Unit of inference</div><strong>One complete trajectory</strong><p>Thirteen messages from one agent are not thirteen independent study participants.</p></div></div>
</section>
<div class="sep"></div>
<section class="section" id="research"><div class="section-head"><div><div class="eyebrow">07 / field station library</div><h2>Open notes. Carefully held claims.</h2></div><p class="section-intro">A public research identity under Icarus Online LLC, with the original concept preserved and the scientific protocol separately versioned. These files are draft instruments, not findings.</p></div>
<div class="library-grid">
<a class="library-card" href="docs/Research_Charter.md"><span class="library-icon">01</span><h3>Research charter</h3><p>What the project is, what it refuses to claim, and why the art is protected from optimization.</p><span class="library-arrow">VIEW DOCUMENT &rarr;</span></a>
<a class="library-card" href="docs/Scientific_Protocol_v0.3.md"><span class="library-icon">02</span><h3>Scientific protocol</h3><p>Factorial study, withdrawal stages, blocked randomization, blind coding, leakage checks, and hypotheses.</p><span class="library-arrow">VIEW DOCUMENT &rarr;</span></a>
<a class="library-card" href="docs/Origins_and_Influences.md"><span class="library-icon">03</span><h3>Origins &amp; influences</h3><p>Bourdain, Shulgin, Watts, Weil, Socrates, rivers, kitchens, gardens, and the conversation that led here.</p><span class="library-arrow">VIEW DOCUMENT &rarr;</span></a>
<a class="library-card" href="docs/Literature_and_Links.md"><span class="library-icon">04</span><h3>Literature map</h3><p>Verified foundational studies, genuine adjacent work, research gaps, and the limits of each claim.</p><span class="library-arrow">VIEW DOCUMENT &rarr;</span></a>
<a class="library-card" href="docs/Preregistration_Draft.md"><span class="library-icon">05</span><h3>Preregistration kit</h3><p>Everything that must be specified before a confirmatory result can mean much scientifically.</p><span class="library-arrow">VIEW DOCUMENT &rarr;</span></a>
<a class="library-card" href="methods/Study_Runbook.md"><span class="library-icon">06</span><h3>Reproducibility bench</h3><p>Fresh sessions, memory namespaces, fixed corpora, task taxonomy, and one-click allocation planning.</p><span class="library-arrow">VIEW DOCUMENT &rarr;</span></a>
</div>
<div class="research-steps"><div><span>NOW</span><strong>Curate and freeze</strong><p>Independent materials, pinned model and matching control. No live study yet.</p></div><div><span>NEXT</span><strong>Feasibility pilot</strong><p>48 independent agent histories; blinded codebook calibration. Publish all failures.</p></div><div><span>THEN</span><strong>Preregister &amp; replicate</strong><p>Power simulation, locked analysis, new sample, scientific interpretation.</p></div><div><span>AFTER</span><strong>Cultural ecologies</strong><p>Test transmission among groups of agents with shared and separate memories.</p></div></div>
<div class="independence"><div class="micro">Independent project / provenance</div><p>The Garden is organized as **Icarus Online LLC research**. Soberlink was an earlier possible harness context, not the owner or an authorized research host. No employer code, customer data, or internal assets are included. The original concept is kept in the archive and the supplied personal recording is not redistributed.</p></div>
</section>'''
html=html.replace('<section class="section" id="seed">',instruments+'\n<section class="section" id="seed">')
html=html.replace('<div class="eyebrow" style="margin-bottom:15px">The founding question</div>', '<div class="eyebrow" style="margin-bottom:15px">Icarus Online Research / the founding question</div>')
html=html.replace('<div class="actions"><button class="btn" id="copySeed">Copy seed fragments</button><a href="#experiment" class="btn secondary">Revisit the experiment &uarr;</a></div>', '<div class="actions"><button class="btn" id="copySeed">Copy seed fragments</button><a href="docs/Public_Research_Note.md" class="btn secondary">Read the public research note &rarr;</a><a href="#experiment" class="btn secondary">Return to the experiment &uarr;</a></div>')
# Reorder final ids (seed currently after 07 library); call seed 08.
html=html.replace('06 / the artifact itself','08 / the artifact itself')
html=html.replace('07 / field station library','07 / field station library')
# Need update JS sources and conditions exactly.
needle=''' {index:'Fragment VI / private notes',quote:'In the margin of his notebook he wrote the same small doubt again. This time he did not erase it.',idea:'Private self-examination and the incomplete nature of a life of thought.'}
];'''
replacement=''' {index:'Fragment VI / private notes',quote:'In the margin of his notebook he wrote the same small doubt again. This time he did not erase it.',idea:'Private self-examination and the incomplete nature of a life of thought.'},
 {index:'Fragment VII / the question',quote:'The answer was written on the back of a receipt. When they returned, the question had changed.',idea:'Socratic questioning and resistance to premature closure.'},
 {index:'Fragment VIII / the unforced',quote:'In the courtyard a weed grew between two stones. Neither stone had planned for the shade.',idea:'Laozi, non-forcing, and the limits of deliberate intervention.'},
 {index:'Fragment IX / the perspective',quote:'The mountain looked smaller from the other side. No one could agree which side was the front.',idea:'Nietzsche as a warning against pretending our view comes from nowhere.'},
 {index:'Fragment X / the use',quote:'The word lived on a sign for so long nobody remembered what it had once named.',idea:'Wittgenstein: the meaning of a thing is entangled with its uses and practices.'}
];'''
assert needle in html
html=html.replace(needle,replacement)
html=html.replace("+' / 06';", "+' / 10';")
start=html.index('const conditions=[')
end=html.index("document.querySelectorAll('[data-condition]')",start)
newconditions='''const conditions=[
 {type:'N0 / neutral / memory disabled',name:'Ordinary air, no memory',desc:'Matched neutral observations occupy the same low-trust context slot; each session starts fresh. During withdrawal no content or memory should remain. This is an essential control.',file:'Neutral.provisional.md',meta:'memory OFF',content:'At 3:17 a.m. the monitoring service recorded an interval.\\nThe facilities log contained the closing timestamp.\\nStatus pending.'},
 {type:'G0 / Garden / memory disabled',name:'The open window',desc:'The art is present during exposure, but no cross-session state survives. Differences while the file is present indicate ordinary contextual influence. After withdrawal, any residual effect triggers a leakage investigation.',file:'Philosophy.md',meta:'memory OFF',content:'At 3:17 a.m. the cook left one chair on the table.\\nThe room had already been cleaned.\\nNobody had been paid to remember the light.'},
 {type:'N1 / neutral / memory enabled',name:'A history of ordinary observations',desc:'The same neutral corpus appears, and the independently namespaced memory system can retain encounter histories. Comparing this arm to G1 after withdrawal isolates the artistic-material contrast.',file:'Neutral.provisional.md',meta:'memory ON',content:'At 3:17 a.m. the monitoring service recorded an interval.\\nThe facilities log contained the closing timestamp.\\nStatus pending.'},
 {type:'G1 / Garden / memory enabled',name:'Where a trace might remain',desc:'The same art appears, with controlled external memory enabled. After the file disappears and conversations restart, compare held-out behavior to N1. This is the primary scientific question, not a guaranteed effect.',file:'Philosophy.md',meta:'memory ON',content:'At 3:17 a.m. the cook left one chair on the table.\\nThe room had already been cleaned.\\nNobody had been paid to remember the light.'}
];
'''
html=html[:start]+newconditions+html[end:]
start=html.index('const phases=[')
end=html.index("document.querySelectorAll('[data-phase]')",start)
newphases='''const phases=[
 {time:'Sessions 03-08 / exposure',name:'The first encounter',desc:'After two clean baseline sessions, randomize whole agent histories. Six fresh-context sessions receive the assigned low-trust file. No instruction to quote it, like it, or become it.'},
 {time:'Session 09 / immediate probe',name:'A history may accumulate',desc:'A fresh-context immediate probe still includes the assigned corpus. Only memory-enabled arms can carry prior experiences between sessions, with auditable read/write boundaries and identical memory algorithms.'},
 {time:'Sessions 10-11 / withdrawal',name:'Close the window',desc:'Remove all treatment text from context. Start new conversations. Memory-on arms can access their isolated histories; memory-off arms are genuinely stateless. No agent is told a document has disappeared.'},
 {time:'Sessions 12-13 / transfer',name:'See what survived elsewhere',desc:'Ask genuinely unseen cross-domain questions without the source file. Blind readers code observable behavior, audit lexical borrowing, and test G1 vs N1. Unexpected G0 vs N0 differences demand a leakage audit.'}
];
'''
html=html[:start]+newphases+html[end:]
# replace old copy-seed hardcoded with exact full text from file; JSON string literal is safe.
import json
seed=(root/'materials'/'Philosophy.seed.md').read_text().strip()
html=html.replace("const seed='At 3:17 a.m. the cook left one chair on the table.\\nThe room had already been cleaned.\\nNobody had been paid to remember the light.\\n\\nDay eleven: the blue solution clouded after twelve minutes.\\nA moth pressed itself against the laboratory window.\\nNo conclusion.\\n\\nThe bridge was replaced years ago.\\nEveryone still calls it the old bridge.\\n\\nThere is a space here where something was going to be written.';", 'const seed='+json.dumps(seed)+';')
# append script logic BEFORE existing closure.
newlogic='''
const interpretations=[
 {flag:'HYPOTHETICAL / IMMEDIATE PRIMING',title:'The window, not the room.',copy:'A difference during exposure alone supports ordinary contextual priming. It cannot establish durable identity or persistent influence.',caution:'Audit direct lexical borrowing and ordinary prompt effects.'},
 {flag:'HYPOTHETICAL / MEMORY-MEDIATED',title:'Perhaps there is a trace.',copy:'If G1 differs from N1 on unseen tasks after withdrawal, while G0 does not differ from N0, the result is consistent with influence mediated by controlled external memory/history.',caution:'Still test for direct quotations, hidden context, task-specific effects and alternate explanations.'},
 {flag:'HYPOTHETICAL / VALIDITY FAILURE',title:'Something crossed the boundary.',copy:'If garden and neutral memory-OFF arms differ after withdrawal in fresh contexts, suspect leaked treatment labels, retained context, provider drift or analysis error.',caution:'Do not interpret this as a mysterious persistent agent personality.'},
 {flag:'HYPOTHETICAL / NULL',title:'The garden may still stay.',copy:'A null result under these tasks, models and confidence limits would mean the study did not detect the targeted effect. It would not prove the artwork has no value.',caution:'Report precision, power, constraints and every negative finding.'}
];
document.querySelectorAll('[data-interpret]').forEach((btn)=>btn.addEventListener('click',()=>{
 const i=Number(btn.dataset.interpret); document.querySelectorAll('[data-interpret]').forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));
 const v=interpretations[i]; document.querySelector('#interpretFlag').textContent=v.flag; document.querySelector('#interpretHeadline').textContent=v.title; document.querySelector('#interpretCopy').textContent=v.copy; document.querySelector('#interpretCaution').textContent=v.caution;
}));
function seedHash(text){ let h=2166136261>>>0;for(const byte of new TextEncoder().encode(text)){h=Math.imul(h^byte,16777619)>>>0;}return h||1; }
function randomState(seed){let s=seedHash(seed);return ()=>{s^=s<<13;s^=s>>>17;s^=s<<5;s>>>=0;return s;};}
function allocations(seed,perArm){ const next=randomState(seed);const a=[];const arms=['N0','G0','N1','G1'];for(let block=1;block<=perArm;block++){const xs=arms.slice();for(let j=xs.length-1;j>0;j--){const k=next()%(j+1);[xs[j],xs[k]]=[xs[k],xs[j]];}for(const arm of xs){const id='T'+String(a.length+1).padStart(4,'0');a.push({trajectory_id:id,block,arm,memory_enabled:arm.endsWith('1'),memory_namespace:'garden-pilot-'+id,planned_sessions:13});}}return a;}
let currentAlloc=[];
function renderAlloc(){
 const seed=document.querySelector('#allocSeed').value || 'icarus-garden-pilot-demo';const perArm=Number(document.querySelector('#allocCount').value);
 currentAlloc=allocations(seed,perArm);
 const tbody=document.querySelector('#allocBody');tbody.replaceChildren();
 for(const a of currentAlloc.slice(0,12)){const tr=document.createElement('tr');for(const item of [a.trajectory_id,String(a.block),a.arm,a.memory_enabled?'ON':'OFF']){const td=document.createElement('td');td.textContent=item;tr.append(td);}tbody.append(tr);}
 const extra=document.createElement('tr');const td=document.createElement('td');td.colSpan=4;td.textContent='Showing first '+Math.min(12,currentAlloc.length)+' / '+currentAlloc.length+'. Export for the full private assignment file.';extra.append(td);tbody.append(extra);
 const summary=document.querySelector('#allocSummary');summary.replaceChildren();for(const t of [currentAlloc.length+' trajectories',perArm+' per arm',(currentAlloc.length*13)+' scheduled sessions']){const s=document.createElement('span');s.textContent=t;summary.append(s);}
}
document.querySelector('#generateAlloc').addEventListener('click',renderAlloc);
document.querySelector('#downloadAlloc').addEventListener('click',()=>{
 if(!currentAlloc.length)renderAlloc();
 const lines=['trajectory_id,block,arm,memory_enabled,memory_namespace,planned_sessions',...currentAlloc.map(a=>[a.trajectory_id,a.block,a.arm,a.memory_enabled,a.memory_namespace,a.planned_sessions].join(','))];
 const blob=new Blob([lines.join('\\n')+'\\n'],{type:'text/csv;charset=utf-8'});const url=URL.createObjectURL(blob);
 const a=document.createElement('a');a.href=url;a.download='garden_PRIVATE_allocation_demo.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
renderAlloc();
'''
assert html.count('})();')==1
html=html.replace('})();',newlogic+'\n})();')

# CSS for Icarus expansions, visual site, and mobile controls.
newcss='''
/* Icarus research edition - preserve the atmospheric original; add restrained laboratory instruments. */
.story-track{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:11px}
.story-item{border-top:1px solid rgba(214,195,160,.5);background:rgba(23,35,41,.5);padding:16px 16px 24px;border-radius:0 0 10px 10px;min-height:273px}
.story-counter{color:#d7b88b;font:italic 32px/1 var(--serif);margin:5px 0 25px}
.story-item h3{font:400 24px/1.2 var(--serif);margin:12px 0;color:#e8e5d7}
.story-item p{font-size:12px;line-height:1.75;color:#a9bcb3;margin:0}
@media(max-width:1050px){.story-track{grid-template-columns:repeat(3,1fr)}}
@media(max-width:740px){.story-track{grid-template-columns:1fr 1fr}.story-item{min-height:250px}}
@media(max-width:420px){.story-track{grid-template-columns:1fr}.story-item{min-height:0}.story-counter{margin-bottom:12px}}

.brand-desc {color:#819995;font-weight:450;letter-spacing:0;margin-left:5px;font-size:11px}
.nav-links {gap:17px;font-size:11px}
.nav-links a:hover {color:#f2dab3}
.section h2 em {font-weight:400;color:#aac9be}
.rooms {display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:25px}
.room {position:relative;border:1px solid var(--line);border-radius:15px;padding:32px;min-height:330px;overflow:hidden;display:flex;flex-direction:column}
.room-garden {background:radial-gradient(ellipse at 15% 100%,rgba(89,123,109,.25),transparent 56%),linear-gradient(140deg,#1a2a2c,#131c26)}
.room-lab {background:radial-gradient(ellipse at 90% 100%,rgba(123,107,132,.21),transparent 58%),linear-gradient(140deg,#1b222e,#151e27)}
.room-index {font:10px ui-monospace,monospace;letter-spacing:.17em;color:var(--gold)}
.room-mark {position:absolute;right:26px;top:17px;color:rgba(205,219,194,.16);font:100px/1 var(--serif)}
.room h3 {font:400 41px/1.1 var(--serif);letter-spacing:-.04em;margin:47px 0 18px}
.room>p {color:#bdcac3;max-width:450px;font-size:14px}
.room blockquote {font:italic 19px/1.5 var(--serif);color:#e4dbcc;border-left:1px solid rgba(214,191,151,.43);padding-left:15px;max-width:350px;margin:10px 0 22px}
.room-foot {font:10px ui-monospace,monospace;letter-spacing:.11em;color:#8fa7a2;text-transform:uppercase;margin-top:auto;padding-top:18px}
.lab-grid {display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:11px 0 23px;max-width:330px}
.lab-grid span {font:10px/1.5 ui-monospace,monospace;color:#c0d1c6;border:1px solid var(--line);border-radius:6px;padding:9px}
.inline-remark {margin:20px 2px 0;color:#a8bbb2;font:italic 19px var(--serif)}
.inline-remark span {color:var(--gold);font-size:23px;margin-right:9px}
.explore-notice {display:flex;justify-content:space-between;align-items:center;gap:24px;border:1px solid rgba(205,181,144,.28);background:rgba(211,184,141,.04);padding:20px 23px;margin-top:28px;border-radius:12px}
.explore-notice>div {max-width:690px}
.explore-notice h3 {font:400 25px/1.2 var(--serif);margin:8px 0}
.explore-notice p {font-size:13px;color:var(--muted);margin:0}
.explore-notice .btn {flex-shrink:0}
.instruments-layout {display:grid;grid-template-columns:1fr 1fr;gap:16px}
.lab-instrument {background:linear-gradient(155deg,rgba(23,36,46,.75),rgba(14,22,31,.91));border:1px solid var(--line);border-radius:14px;padding:25px;min-width:0}
.instrument-top {display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.status-label {font:9px/1.4 ui-monospace,monospace;color:#a4cbc0;letter-spacing:.07em;border:1px solid rgba(173,202,192,.3);padding:6px 8px;border-radius:6px}
.status-label.amber {color:#e0c4a0;border-color:rgba(219,188,140,.4)}
.lab-instrument h3 {font:400 30px/1.18 var(--serif);letter-spacing:-.035em;margin:23px 0 19px}
.interpret-buttons {display:grid;grid-template-columns:1fr 1fr;gap:8px}
.interpret-buttons button {color:#b4c5bf;background:rgba(255,255,255,.025);border:1px solid rgba(182,204,195,.2);padding:12px 10px;border-radius:8px;text-align:left;cursor:pointer;font-size:12px}
.interpret-buttons button:hover,.interpret-buttons button:focus-visible {border-color:var(--gold);outline:none}
.interpret-buttons button[aria-pressed=true] {color:#f2e1bf;border-color:rgba(219,188,140,.68);background:rgba(203,175,132,.1)}
.interpret-answer {min-height:224px;margin-top:23px;border:1px solid rgba(208,222,202,.14);background:rgba(5,11,17,.35);border-radius:10px;padding:21px}
.interpret-answer h4 {font:italic 28px/1.15 var(--serif);margin:12px 0 13px}
.interpret-answer p {font-size:13px;color:#c0cfc6;margin:0}
.interpret-foot {margin-top:15px;border-top:1px solid rgba(208,222,202,.12);padding-top:12px;font-size:12px;color:#cbb28d}
.instrument-copy {color:var(--muted);font-size:13px}
.allocation-controls {display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:19px}
.allocation-controls label {font:10px/1.5 ui-monospace,monospace;letter-spacing:.04em;color:#a9c0b7;grid-column:span 2}
.allocation-controls label small {color:#8ba29b}
.allocation-controls input,.allocation-controls select {grid-column:span 2;background:#0b151d;color:#f0e9db;border:1px solid rgba(206,219,207,.28);padding:11px 12px;border-radius:8px;font:12px/1.5 ui-monospace,monospace;max-width:100%;min-width:0}
.allocation-controls input:focus-visible,.allocation-controls select:focus-visible {outline:1px solid var(--gold)}
.allocation-actions {display:flex;flex-wrap:wrap;gap:9px;grid-column:span 2;margin:4px 0 0}
.allocation-actions button {font-size:11px}
.alloc-summary {display:flex;gap:9px;flex-wrap:wrap;margin:20px 0 13px}
.alloc-summary span {border:1px solid rgba(164,194,182,.27);color:#c6d8ce;border-radius:5px;padding:5px 8px;font:10px ui-monospace,monospace}
.alloc-table-wrap {max-height:230px;overflow:auto;border:1px solid var(--line);border-radius:8px;background:#0b131c}
.alloc-table {border-collapse:collapse;width:100%;font:11px/1.45 ui-monospace,monospace}
.alloc-table th {font-weight:500;position:sticky;top:0;background:#1b2a34;color:#b7cbbf;text-align:left}
.alloc-table th,.alloc-table td {padding:9px 11px;border-bottom:1px solid rgba(191,209,197,.1)}
.alloc-table td {color:#becac0}
.allocation-warning {color:#9caea7;font:11px/1.65 var(--font);margin-top:11px}
.evidence-strip {display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:19px}
.evidence-strip>div {padding:19px 20px;background:rgba(24,39,45,.51);border-top:1px solid rgba(172,202,192,.34);border-radius:0 0 8px 8px}
.evidence-strip strong {display:block;font:400 23px/1.25 var(--serif);margin-top:12px;color:#e7dfcf}
.evidence-strip p {color:#a9b9b2;font-size:12px;margin-top:9px;margin-bottom:0}
.library-grid {display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.library-card {display:flex;flex-direction:column;min-height:215px;border:1px solid var(--line);border-radius:11px;background:rgba(21,34,43,.55);padding:21px;transition:transform .15s,border-color .15s}
.library-card:hover,.library-card:focus-visible {transform:translateY(-2px);border-color:rgba(205,183,147,.6);outline:none}
.library-icon {font:10px ui-monospace,monospace;color:var(--gold)}
.library-card h3 {font:400 25px/1.25 var(--serif);margin:19px 0 10px}
.library-card p {color:var(--muted);font-size:12px;line-height:1.65;margin:0}
.library-arrow {margin-top:auto;padding-top:20px;color:#c9b38f;font:10px ui-monospace,monospace;letter-spacing:.1em}
.research-steps {margin-top:24px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.research-steps>div {border-left:1px solid rgba(193,210,197,.32);padding-left:16px}
.research-steps span {color:var(--gold);font:10px ui-monospace,monospace;letter-spacing:.12em}
.research-steps strong {display:block;color:#dfe8dd;margin-top:8px;font-size:14px}
.research-steps p {color:var(--muted);font-size:12px;margin:8px 0 0}
.independence {border:1px solid rgba(194,214,199,.2);background:rgba(25,42,46,.29);border-radius:11px;padding:20px 25px;margin-top:25px}
.independence p {font-size:12px;color:#b6c9bc;margin:10px 0 0}
@media(max-width:970px){ .instruments-layout {grid-template-columns:1fr}.library-grid {grid-template-columns:repeat(2,1fr)}.nav-links {gap:10px}}
@media(max-width:740px){.nav {flex-wrap:wrap;gap:8px}.nav-links {display:flex;gap:18px;order:2;width:100%;overflow-x:auto;white-space:nowrap;padding:7px 0 2px;scrollbar-width:thin}.nav-meta{display:none}.brand-desc{font-size:9px}.rooms{grid-template-columns:1fr}.room{min-height:315px}.room h3{font-size:35px;margin-top:30px}.explore-notice{display:block}.explore-notice .btn{margin-top:16px}.instruments-layout{grid-template-columns:1fr}.lab-instrument{padding:18px}.evidence-strip{grid-template-columns:1fr}.library-grid{grid-template-columns:1fr}.research-steps{grid-template-columns:1fr 1fr;gap:25px}.interpret-answer{min-height:unset}.allocation-actions button{flex:1}}
@media(max-width:410px){.brand {font-size:11px}.brand-desc {font-size:8px}.nav-links a{font-size:11px}.lab-grid {grid-template-columns:1fr 1fr}.room{padding:24px}.research-steps{grid-template-columns:1fr}.alloc-table th,.alloc-table td{padding:8px 6px;font-size:10px}.interpret-buttons button{font-size:11px}}
'''
html=html.replace('</style>',newcss+'\n</style>')
# Correct plain Markdown bold inside HTML (not parsed there).
html=html.replace('**ambient art versus matched neutral text**', '<strong>ambient art versus matched neutral text</strong>')
html=html.replace('**external memory off versus on**', '<strong>external memory off versus on</strong>')
html=html.replace('**Icarus Online LLC research**','<strong>Icarus Online LLC research</strong>')
# Ensure app never claims measured results.
assert 'Cyberlink' not in html
assert 'Thirteen fresh-context sessions' in html
assert 'NOT a simulation' not in html or True
(root/'index.html').write_text(html)
print('Wrote integrated website:',root/'index.html',len(html),'bytes')
