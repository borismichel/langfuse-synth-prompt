"""Native stored prompt references, separate from resolved historical fixtures.

Langfuse resolves these text dependencies before the SDK compiles variables and
message placeholders. Current customer-facing prompts follow the voice label;
task-specific and historical references remain pinned.
"""
from __future__ import annotations

from copy import deepcopy

from .catalog import load_fixture


LEGACY_COMPOSITION_REVISION = "native-text-components-v1"
COMPOSITION_REVISION = "native-text-components-v2"

# Share presentation style only where it is part of the agent's job.
VOICE_PROMPTS = {"PR-01", "PR-02", "PR-03", "PR-08"}
FACTUAL_PROMPTS = {"PR-01", "PR-02", "PR-03", "PR-06", "PR-07", "PR-08", "PR-09"}
STRUCTURED_PROMPTS = {"PR-04", "PR-07"}


def building_blocks() -> dict[str, dict]:
    """Four reusable text prompts; the playful voice preserves the accepted edit."""
    contents = {
        "reference-context": "Supplied reference_context:\n{{reference_context}}",
        "factual-boundaries": "Preserve source facts and uncertainty. Never invent information or claim an action was completed.",
        "voice": "Return a concise, respectful answer in plain English.",
        "structured-output": "Return only the allowed structured result.",
    }
    blocks = {key: {"name": f"building-blocks/{key}", "versions": [
        {"version": 1, "prompt": content, "labels": ["production"]},
    ]} for key, content in contents.items()}
    blocks["voice"]["versions"].append({
        "version": 2, "prompt": load_fixture("product")["prompt_comparison"]["change"],
        "labels": ["playful"],
    })
    return blocks


def prompt_reference(name: str, version: int) -> str:
    return f"@@@langfusePrompt:name={name}|version={version}@@@"


def compose_chat_prompt(resolved: list[dict], *, prompt_id: str | None = None,
                        version: int | None = None) -> list[dict]:
    """Replace exact reusable fragments without changing resolved message bytes.

    Only message content is composed. The history placeholder and user variable
    retain their native chat representation. No local resolver runs in live use.
    """
    stored = deepcopy(resolved)
    blocks = building_blocks()
    for message in stored:
        if "content" not in message:
            continue
        content = message["content"]
        if "@@@langfusePrompt:" in content:
            raise ValueError("Composition expects resolved fixture text, not existing references")
        for key, block in blocks.items():
            # None retains the original v1 policy for verification of older seeds.
            if prompt_id is not None and (
                (key == "voice" and prompt_id not in VOICE_PROMPTS)
                or (key == "factual-boundaries" and prompt_id not in FACTUAL_PROMPTS)
                or (key == "structured-output" and prompt_id not in STRUCTURED_PROMPTS)
            ):
                continue
            for component in block["versions"]:
                reference = prompt_reference(block["name"], component["version"])
                if key == "voice" and component["version"] == 1 and prompt_id in VOICE_PROMPTS and version in (7, 8):
                    reference = f"@@@langfusePrompt:name={block['name']}|label=production@@@"
                content = content.replace(component["prompt"], reference)
        message["content"] = content
    return stored
