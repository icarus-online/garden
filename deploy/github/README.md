# Garden main rules proposal

Tracking: [Garden #4](https://github.com/icarus-online/garden/issues/4).
The JSON beside this file is a **disabled proposal**, not an installed rule.
It targets only `main`: require a PR, one approving review, approval after the
last push, resolved conversations and current-base `validate` CI; block deletion
and non-fast-forward updates. The current-main CI job name was read back as
`validate` from run 39877088833. The proposal binds it to GitHub Actions app
15368, verified from the accepted commit's check runs. Recheck that identity
before activation rather than trusting its name alone.

Activation is blocked by missing existing administration access and an unnamed
eligible independent reviewer. The owner cannot supply their own approving
review on their PR. Confirm the reviewer's existing access and agree a documented
owner recovery procedure before making this blocking rule active. Do not grant
access, invent a bypass actor, broaden a token or weaken the review count to
work around the gap. The proposal intentionally grants no bypass.

An existing authorized repository administrator can import the proposal,
verify its target/check identity and change enforcement to `active` after those
prerequisites. Read back effective branch rules and test a normal PR afterward.
Rollback is disabling only this new ruleset; retain its prior configuration and
do not remove unrelated organization rules. API fields were checked against
[GitHub's ruleset reference](https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset).

On October 23, 2026 (Pacific), the connected GitHub tools lacked administration
writes, the local broker returned `scope_denied`, and the browser had no signed-in
owner session. No repository rule or notification preference was changed.
