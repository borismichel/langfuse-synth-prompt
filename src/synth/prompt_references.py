"""Keep native prompt associations on generations, without redundant root fields."""
from copy import deepcopy

from langfuse_synth_core.seed import otlp

ROOT_PROMPT_METADATA = frozenset(otlp.OBS_METADATA_PREFIX + key for key in (
    'prompt_references', 'prompt_name', 'prompt_version', 'resolved_version'))


def remove_root_prompt_references(events: list[dict]) -> list[dict]:
    """Copy events, removing only redundant root prompt metadata.

    Every generation's native prompt name/version and metadata stay untouched.
    Root request metadata, operation identity and input/output are preserved.
    """
    result = deepcopy(events)
    for event in result:
        if otlp.is_trace_root(event):
            event['attributes'] = [item for item in event['attributes']
                                   if item['key'] not in ROOT_PROMPT_METADATA]
    return result


# Preserve the internal call signature for older kit integrations; its semantics
# now follow the user's generation-only prompt association requirement.
annotate_prompt_references = remove_root_prompt_references
