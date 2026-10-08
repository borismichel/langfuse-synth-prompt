#!/usr/bin/env python3
"""Create a demo planning workspace and track content-addressed stage handoffs.

Standard library only. No network, Git mutations, core installation or deployment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import quote

STAGES = ('story', 'prototype', 'authoring')
STATE = '.demo/project.json'
SKILLS = ('develop-langfuse-demo-story', 'prototype-langfuse-demo',
          'author-langfuse-demo-kit', 'langfuse', 'langfuse-brand-assets')
IGNORE = {'.git', 'node_modules', '.venv', '__pycache__', 'dist', '.DS_Store'}
BEGIN = '<!-- langfuse-demo-workspace -->'
END = '<!-- /langfuse-demo-workspace -->'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    pending = path.with_suffix(path.suffix + '.tmp')
    pending.write_text(json.dumps(value, indent=2) + '\n')
    pending.replace(path)


def inside(root, relative):
    path = root / relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(root):
        raise ValueError(f'Path must stay inside the kit: {relative}')
    return path


def inventory(root, specs):
    result = {}
    for spec in specs:
        path = inside(root, spec)
        if not path.exists():
            raise ValueError(f'Missing handoff input: {spec}')
        paths = sorted(path.rglob('*')) if path.is_dir() else [path]
        for item in paths:
            rel = item.relative_to(root)
            if any(part in IGNORE for part in rel.parts):
                continue
            if any(part.startswith('.env') for part in rel.parts):
                raise ValueError(f'Environment files cannot be handoff inputs: {rel}')
            inside(root, str(rel))
            if item.is_file():
                result[rel.as_posix()] = hashlib.sha256(item.read_bytes()).hexdigest()
    if not result:
        raise ValueError('A handoff needs at least one existing file.')
    return result


def statuses(root, state):
    result = {}
    records = state['handoffs']
    for index, stage in enumerate(STAGES):
        entry = records.get(stage)
        if not entry:
            result[stage] = 'not-started'
            continue
        try:
            unchanged = inventory(root, entry['paths']) == entry['files']
        except ValueError:
            unchanged = False
        if index:
            parent = STAGES[index - 1]
            unchanged = (unchanged and result[parent] == 'accepted'
                         and entry['input_checkpoint'] == digest(records.get(parent)))
        result[stage] = entry['status'] if unchanged else 'stale'
    return result


def render(root, state):
    status = statuses(root, state)
    lines = [f"# {state['slug']} — demo workspace", '',
             'Generated from `.demo/project.json`; rerun `python3 scripts/demo_workspace.py render`.',
             'This reports handoff state, not runtime or deployment readiness.', '',
             f"Kit repository: {state['repository']}",
             f"Core: {state['core']['repository']} at `{state['core']['ref']}` "
             f"(`{state['core']['commit']}`). Runtime adoption is verified during authoring.",
             f"Depot: {state['depot_repository']}", '',
             'Association is recorded here. Catalog registration and admission are separate delivery actions.',
             'Before a signed release, use this workspace in GitHub/local files. Depot Docs later shows a released snapshot.',
             '', '| Stage | Effective status | Skill |', '| --- | --- | --- |']
    for stage, skill in zip(STAGES, SKILLS[:3]):
        lines.append(f'| {stage} | {status[stage]} | `{skill}` |')
    lines += ['', '## Handoffs', '',
              'A changed upstream checkpoint makes its consumers stale. Re-review and record a new checkpoint.',
              'An accepted authoring handoff is not evidence that admission, deployment or rehearsal passed.', '']
    for stage in STAGES:
        entry = state['handoffs'].get(stage)
        if not entry:
            continue
        lines += [f'### {stage}: {status[stage]}', '', entry['note'], '',
                  f"Recorded decision/evidence: `{entry['decision_file']}`", '']
        for name, sha in sorted(entry['files'].items()):
            url = state['repository'] + '/blob/' + quote(state['branch'], safe='') + '/' + quote(name)
            lines.append(f'- [{name}]({url}) — `{sha[:12]}`')
        lines += ['']
    lines += ['## Readiness', '',
              'Authoring must report offline checks, current-run live verification, signed release,',
              'Depot admission and delivered presenter rehearsal separately, with evidence.',
              'Neither this status file nor an accepted document performs those checks.', '']
    target = inside(root, 'docs/demo/DOSSIER.md')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n'.join(lines))


def initialise(root, args):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.slug):
        raise ValueError('Use a lowercase hyphenated demo slug.')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repository):
        raise ValueError('Repository must be OWNER/NAME.')
    if not re.fullmatch(r'[0-9a-f]{40}', args.core_commit):
        raise ValueError('Resolve the selected core release to its full commit SHA first.')
    if any(p.name in {'langfuse-demo-depot', 'langfuse-synth-core', 'my-skills'} for p in (root, *root.parents)):
        raise ValueError('Initialise a dedicated kit directory, not Depot/core/skills.')
    config = {'schema_version': 1, 'slug': args.slug,
              'repository': 'https://github.com/' + args.repository, 'branch': args.branch,
              'core': {'repository': 'https://github.com/borismichel/langfuse-synth-core',
                       'ref': args.core_ref, 'commit': args.core_commit},
              'depot_repository': args.depot_repository,
              'skills_repository': 'https://github.com/borismichel/my-skills',
              'skills_ref': args.skills_ref, 'handoffs': {}}
    state_path = inside(root, STATE)
    if state_path.exists():
        current = json.loads(state_path.read_text())
        if {k: v for k, v in current.items() if k != 'handoffs'} != {k: v for k, v in config.items() if k != 'handoffs'}:
            raise ValueError('Workspace exists with different identity/pins; review an explicit migration.')
        return current
    agent = inside(root, args.agent_file or ('AGENTS.md' if (root/'AGENTS.md').exists()
                                           else 'CLAUDE.md' if (root/'CLAUDE.md').exists() else 'AGENTS.md'))
    block = '\n'.join([BEGIN, '## Langfuse demo workspace', '',
                       'Read [the workflow](docs/agents/demo-workflow.md) and `.demo/project.json` before demo work.',
                       'Run `python3 scripts/demo_workspace.py status` before consuming a handoff.',
                       'The kit repository owns its story, data model, prototype and implementation.',
                       'Keep shared skills, core transport and Depot application code in their own repositories.', END, ''])
    workflow = '''# Demo workflow

Start with `.demo/project.json` and run `python3 scripts/demo_workspace.py status`.
The current human-readable overview is `docs/demo/DOSSIER.md` (regenerate with `render`).

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
'''
    helper = Path(__file__).read_bytes()
    writes = {'docs/agents/demo-workflow.md': workflow.encode(), 'scripts/demo_workspace.py': helper}
    for rel in (*writes, 'docs/demo/DOSSIER.md'):
        if inside(root, rel).exists():
            raise ValueError(f'Existing unmanaged file needs review: {rel}')
    old = agent.read_text() if agent.exists() else ''
    if BEGIN in old or END in old:
        raise ValueError('Existing workspace instruction block without state needs review.')
    root.mkdir(parents=True, exist_ok=True)
    for directory in ('docs/demo/story', 'docs/demo/prototype', 'docs/demo/authoring', 'design/prototype'):
        inside(root, directory).mkdir(parents=True, exist_ok=True)
    for rel, data in writes.items():
        target = inside(root, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    agent.parent.mkdir(parents=True, exist_ok=True)
    agent.write_text(old.rstrip() + '\n\n' + block if old else block)
    save(state_path, config)
    render(root, config)
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    for name in ('slug', 'repository', 'core-ref', 'core-commit', 'skills-ref'):
        init.add_argument('--' + name, required=True)
    init.add_argument('--branch', default='main')
    init.add_argument('--agent-file', choices=('AGENTS.md', 'CLAUDE.md'))
    init.add_argument('--depot-repository', default='https://github.com/borismichel/langfuse-demo-depot')
    sub.add_parser('status')
    sub.add_parser('render')
    handoff = sub.add_parser('handoff')
    handoff.add_argument('stage', choices=STAGES)
    handoff.add_argument('--status', choices=('ready', 'accepted'), required=True)
    handoff.add_argument('--decision-file', required=True)
    handoff.add_argument('--paths', nargs='+', required=True)
    handoff.add_argument('--note', required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.command == 'init':
            state = initialise(root, args)
        else:
            state = json.loads(inside(root, STATE).read_text())
        if args.command == 'handoff':
            stage = args.stage
            i = STAGES.index(stage)
            if i and statuses(root, state)[STAGES[i-1]] != 'accepted':
                raise ValueError('The upstream handoff must be accepted and unchanged.')
            decision = inside(root, args.decision_file)
            if not decision.is_file() or not decision.read_text().strip():
                raise ValueError('Record the actual review/acceptance in a nonempty decision file.')
            paths = sorted(set(args.paths + [args.decision_file]))
            if any(p in {'.', STATE, 'docs/demo', 'docs/demo/DOSSIER.md'} for p in paths):
                raise ValueError('Select stage files/directories, not the workspace state or generated dossier.')
            files = inventory(root, paths)
            if STATE in files or 'docs/demo/DOSSIER.md' in files:
                raise ValueError('A checkpoint cannot include its own state or generated dossier.')
            state['handoffs'][stage] = {'status': args.status, 'paths': paths, 'files': files,
                                       'decision_file': args.decision_file, 'note': args.note,
                                       'input_checkpoint': digest(state['handoffs'].get(STAGES[i-1])) if i else None}
            save(root/STATE, state)
        if args.command in ('handoff', 'render'):
            render(root, state)
        result = statuses(root, state)
        print(json.dumps(result, indent=2))
        return 1 if 'stale' in result.values() else 0
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
