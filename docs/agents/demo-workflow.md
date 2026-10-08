# Demo workflow

Start with `.demo/project.json` and run `python3 scripts/demo_workspace.py status`.
The current human-readable overview is `docs/demo/DOSSIER.md` (regenerate with `render`).
For dependency provenance, installed skill locations and pending Depot checks,
read [setup evidence](setup.md).

| Stage | Skill | Canonical location |
| --- | --- | --- |
| Story and data assumptions | develop-langfuse-demo-story | docs/demo/story/ |
| Prototype brief, review and evidence | prototype-langfuse-demo | docs/demo/prototype/ |
| Runnable prototype and fixtures | prototype-langfuse-demo | design/prototype/ |
| Build/delivery evidence | author-langfuse-demo-kit | docs/demo/authoring/ |

Use the maintained langfuse and langfuse-brand-assets skills for product and visual guidance.
Resolve missing skills from the recorded my-skills revision; do not silently invent their instructions.
Shared skill sources are maintained outside this kit. Inspect existing local skill edits before updates.

Keep business truth in the story contract and concrete prototype state/fixtures in the prototype.
Link by stable IDs; record accepted changes upstream rather than maintaining competing data models.
Each stage consumes an accepted, current upstream handoff. Authoring preserves the accepted examples.
An upstream edit marks downstream work stale until its impact is reviewed and checkpoints are renewed.

Save the user's actual acceptance in a stage review Markdown file; do not invent approval.
For ready-for-review checkpoints record the review request instead. Then run:

    python3 scripts/demo_workspace.py handoff story --status accepted --decision-file docs/demo/story/REVIEW.md --paths docs/demo/story --note 'Story reviewed by the user.'

Replace the stage and paths for later handoffs. Include every authoritative input/output,
especially design/prototype for prototype acceptance. Directory inventories detect added files.
Exclude dependencies/build outputs and credentials. The script checks hashes and dependencies;
it cannot establish the truth of an acceptance statement or execute live verification.

Initial setup records a verified core release and repository association; it does not claim a runtime kit exists.
At authoring, use that release's supported synth-authoring scaffold and reconcile it into this repo,
preserving these documents and existing work. Validate the actual runtime and CI pins against the chosen release.
Record offline/live/admission/rehearsal evidence separately; accepted documents do not mean deployable.

Planning uses these files, not GitHub issues. Create issues only when requested.
Changing stages requires the user's request, not merely a status change.
