# Langfuse prompt demo

Planning workspace for the `prompt` demo kit. The scenario and presenter journey
will be defined during story development.

- [Workspace dossier](docs/demo/DOSSIER.md): stage status and handoffs.
- [Demo workflow](docs/agents/demo-workflow.md): canonical files and stage rules.
- [Setup evidence](docs/agents/setup.md): dependencies, installed skills and pending integration checks.

## Next action

Invoke `$develop-langfuse-demo-story` in this repository. Save the story packet
under `docs/demo/story/`; initialization has not started or accepted any stage.

Check handoffs with `python3 scripts/demo_workspace.py status`. Refresh the
generated dossier with `python3 scripts/demo_workspace.py render`.

The repository records a core release association. Runtime scaffolding belongs
to the authoring stage. Depot Docs publication requires a manifest declaring the
dossier, a signed kit release, successful admission, and registry sync.
