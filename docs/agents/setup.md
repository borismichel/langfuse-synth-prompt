# Initialization evidence

Verified on 2026-10-08. Identity and dependency pins live in
[`project.json`](../../.demo/project.json); stage state lives in the generated
[dossier](../demo/DOSSIER.md).

## Repository

The user selected `borismichel/langfuse-synth-prompt` with public visibility.
The initial directory was empty. The demo slug `prompt` follows its repository
name; the business scenario remains for story development.

## Core and Depot

GitHub's annotated `v4.1.1` tag resolves to
`6b86ac16d797cd0c6a80da1cdd68e8fc8998c18d`. The repository releases core through
pushed version tags as described in that ref's `RELEASING.md`; the GitHub Releases
list is empty. The tag object is `571f47a003b5f64c6177e48f0a26685ddc3ed75c`.
The neighbouring core checkout contains later commits and uncommitted changes;
these are excluded from this kit's recorded association.

The intended Depot is `borismichel/langfuse-demo-depot`. Its current kit-author
guide was read from GitHub during setup. The live instance URL is unresolved,
so `GET /api/v1/contract-version` compatibility remains pending. Recheck that
endpoint before runtime scaffolding and release.

Depot source at `9f50aff0fd4a2ea244d0ba1c52c5de780ca00d1d` pins core
`v4.1.1` in `api/pyproject.toml`, verified through GitHub. This establishes source
alignment; it does not establish the deployed instance's version.

Initialization creates no runtime manifest. During authoring, add the existing
`docs/demo/DOSSIER.md` under `assets.docs` with title `Demo Workspace and Handoffs`,
preserving other entries. Validate with matching core tools. Signed release,
admission, registry registration and sync are prerequisites for Depot's Docs tab.
Until then, local files and GitHub are the working document surface.

## Workflow skill availability

All five required skills are discoverable through the existing user installation;
no per-kit copies were installed. The clean shared-skills checkout and GitHub
`main` both resolve to the revision recorded in project metadata.

| Skill | Installed location relative to the user's home | Comparison with recorded source |
| --- | --- | --- |
| develop-langfuse-demo-story | `.codex/skills/develop-langfuse-demo-story` | Matches |
| prototype-langfuse-demo | `.codex/skills/prototype-langfuse-demo` | `references/dependencies.md` describes installed dependency links rather than source/archive packaging |
| author-langfuse-demo-kit | `.agents/skills/author-langfuse-demo-kit` | Matches |
| langfuse | `.agents/skills/langfuse` (also linked from story dependencies) | Trailing whitespace in `references/cli.md` |
| langfuse-brand-assets | `.codex/skills/langfuse-brand-assets` | Trailing blank lines in `assets/tokens.css` |

The initialization skill and its bundled helper match the recorded shared-skills
source. Installed differences were inspected and preserved. This provenance
records an inspection, not an enforced lock on future user-level skill changes.

## Next stage

Invoke `$develop-langfuse-demo-story`. Its packet belongs in `docs/demo/story/`.
Story, prototype and authoring are all unstarted. Empty stage directories are
created locally by the helper and enter Git when their first artifacts exist.
