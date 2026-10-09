"""Native stored prompt references, separate from resolved historical fixtures.

Langfuse resolves these text dependencies before the SDK compiles variables and
message placeholders. Production references pin component versions so a shared
label move cannot silently change the accepted historical prompt content.
"""
from __future__ import annotations

from copy import deepcopy

from .catalog import load_fixture


COMPOSITION_REVISION = "native-text-components-v1"


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


def compose_chat_prompt(resolved: list[dict]) -> list[dict]:
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
        for block in blocks.values():
            for version in block["versions"]:
                content = content.replace(version["prompt"], prompt_reference(block["name"], version["version"]))
        message["content"] = content
    return stored
