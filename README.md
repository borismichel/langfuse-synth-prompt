# Langfuse prompt demo

Planning workspace for the `prompt` demo kit. The scenario and presenter journey
will be defined during story development.

- [Workspace dossier](docs/demo/DOSSIER.md): stage status and handoffs.
- [Demo workflow](docs/agents/demo-workflow.md): canonical files and stage rules.
- [Setup evidence](docs/agents/setup.md): dependencies, installed skills and pending integration checks.

## Next action

Review the [complete story packet](docs/demo/story/REVIEW.md). It is ready for
review; user acceptance is pending. The [prototype brief](docs/demo/story/PROTOTYPE_HANDOFF.md)
preserves the three-stage journey, both evaluation tracks and session-first
companion navigation. No prototype or runtime has been built.

Check handoffs with `python3 scripts/demo_workspace.py status`. Refresh the
generated dossier with `python3 scripts/demo_workspace.py render`.

The repository records a core release association. Runtime scaffolding belongs
to the authoring stage. Depot Docs publication requires a manifest declaring the
dossier, a signed kit release, successful admission, and registry sync.
