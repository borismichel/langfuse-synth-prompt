# Text-component release rehearsal — 2026-10-09

The exact admitted release is `v0.2.1`, source
`f8cdd9dab4b7d46a706e122c83734113ba457c7f`, with signed image digest
`sha256:1683eeba9c4be0596346c8fec8e45febc736562223627d8dfb7ca79bf780e555`.
The fresh target is [prompt-components-demo](https://cloud.langfuse.com/project/cmv0nl149090gad0f8c5p5xcb)
in **Boris Demo Enterprise** (`cmtqvkiw701e6ad0dtv73tds4`). Earlier populated
projects were preserved. This records observed checks, not new user acceptance.

## Automatic admission and setup

[Admission 3e3f4be3](http://localhost:3009/admin/admission/3e3f4be3-1f46-4b33-b47d-033cb60c1ea7)
passed register, build, spawn, seed, verify and companion smoke. Both setup stages
completed automatically. The initially empty project had no manually provisioned
model connection or evaluators. Depot supplied its selected Anthropic key only to
the explicitly declared setup step. The actual seed container had the Langfuse
pair and no model-provider key. Historical generation remained model-free.

The delivered deployment showed 1,638 traces, 5,137 observations, 360 sessions and
32 dataset items. Its runbook contained the three accepted beats and component
instructions. [Admission receipt](evidence/depot-admission-v0.2.1.json).

## Native portfolio and composition

Opened the native prompt portfolio, product versions and Metrics. The product
history shows usage, latency, cost and categorical factual results by version.
The `building-blocks` folder contains four text families: reference context,
factual boundaries, voice and structured output. Voice v1 is plain English;
v2 has the `playful` label. Admission verified all 72 opening agent versions in
raw and resolved forms, including their native dependency graphs.

From product v7, used **Add prompt reference** to copy the voice `playful`
reference into the first system message, saved v9 with commit message
“Reuse shared theatrical voice”, then added `staging`. The second system message
retains the pinned reference-context v1. Native Tagged and Resolved views show
the reference chips and full resolved instructions. No accepted reference data,
history placeholder, current-message variable or base instruction was replaced.

Seeded agent dependencies pin component versions. This presenter-created candidate
uses a label; moving `playful` later can change its resolved dependency. Inspect it
again before later experiments or promotion, or use a pinned component version.

[Folder](evidence/components-folder.png), [voice](evidence/components-voice.png),
[metrics](evidence/components-prompt-metrics.png),
[staged composition](evidence/components-staging-v9.png).

## Real experiment comparison

Ran exactly once per version on the same eight cases and frozen dataset snapshot
`2026-10-09T07:59:55.242Z`, explicitly selecting `claude-sonnet-5-5` for both.
All eight attached evaluator mappings were complete. The same evaluator IDs and
versions were used in both runs; their experiment overrides use top-level `eval_*`
item metadata. The native runner records the reference-context message as a user
message after the system instruction; exact content and ordered history were verified.

- Baseline v7: `cmv0owg9n0anead0eor8fs3x4`.
- Composed candidate v9: `cmv0ou3ho01bwad0e8d1lb505`.
- 16 real outputs and 128 actual EVAL results were read back.

| Criterion | v7 | v9 |
| --- | --- | --- |
| Dark-side delivery mean | 0 | 0.3375 |
| Record fidelity | 8 Pass | 8 Pass |
| Claim support | 8 Pass | 8 Pass |
| Respectful tone mean | 1 | 1 |

The style change is mixed: five candidates score above zero, three remain at zero.
Input-signal distributions are identical across the pair. No generation was retried
to obtain a preferred score. The native comparison's directional indicator is
relative to its displayed ordering; use the named run values rather than inferring
which prompt improved from an arrow alone.

[Full experiment evidence](evidence/components-experiments.json),
[native comparison](evidence/components-native-comparison.png).

## Promotion, companion and session

Before promotion, sent the first runbook question through the Depot-served companion.
It used production v7 and returned ordinary prose. The authenticated owner then
selected **Save and promote to production** on v9. Production protection remained
enabled; the user's earlier separate enforcement verification is preserved, and
this owner session does not claim a fresh member-denial test.

Started a new conversation and sent all four runbook messages once. The same
Sonnet 5.5 model picked up v9 on every turn. The first reply starts “Listen closely”
and uses the salary/force/orbit metaphor; subsequent turns retain restrained
theatrical phrasing while explaining the correction, own-transfer exclusion and
document requirements.

The companion's **Open session** destination is
[conversation-30d86b2acd544663a6464c8324603253](https://cloud.langfuse.com/project/cmv0nl149090gad0f8c5p5xcb/sessions/conversation-30d86b2acd544663a6464c8324603253).
Native chat view shows four user/reply pairs once each and one system section.
The third-turn peek shows the request root, reference retriever and generation;
the generation has the actual `products/explainer - v9` prompt link and model.

Readback verified 12 observations, ordered history lengths 0/2/4/6, and 32 EVAL
results on the correct subjects. All factual checks passed; tone was 1 and style
0.5 on every reply. Only turn three triggered frustration, profanity and
disagreement. The product questions do not invoke the fee calculator; no TOOL
execution is claimed for this session.

Submitted thumbs-down on the third reply with comment “The fee explanation is
clear, but this tone feels too theatrical for customer support.” The resulting
BOOLEAN `user-thumbs` score is 0 on the third request root, separate from the
disagreement judge. The UI confirmed Feedback saved and disabled resubmission.

The online `user_disagreement` rule maps observation metadata
`$.current_user_message` and `$.prior_messages`, with production/online/user_input
filters. It does not map experiment item metadata. Reply rules use output and
observation metadata. The same evaluator definitions have separate experiment
`$.eval_*` overrides, verified against the actual scores.

[Complete live evidence](evidence/components-live-session.json),
[before promotion](evidence/components-before-promotion.png),
[promoted v9](evidence/components-production-v9.png),
[feedback](evidence/components-live-feedback.png),
[native session](evidence/components-native-session.png),
[generation prompt link](evidence/components-generation-prompt.png).

## Presentation and reset notes

The admitted companion is available through
[Depot](http://localhost:3009/live/2f05a0c7-ee11-49a1-9557-b3798284ae7c).
New conversation resets local conversation context without deleting history.
To rehearse the opening again, an administrator may move product `production`
back to v7 and start a new chat; preserve all real results. Do not reseed this
populated project.

The admission carrier's generic **Open Langfuse project** shortcut still targets
the regional host, because admission does not populate its project identifier
through the normal deployment verification flow. The exact project link above
and companion session links are correct. This limitation is disclosed rather
than represented as a verified project shortcut.
