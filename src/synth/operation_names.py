"""Application operation names shared by historical replay and the companion."""
from collections import defaultdict
from copy import deepcopy

from langfuse_synth_core.seed import otlp

from .catalog import prompt_by_id
from .receipt import attributes

ROOT_NAME_BY_PROMPT = {
    'PR-01': 'explain-product',
    'PR-02': 'explain-fees',
    'PR-03': 'guide-application',
    'PR-04': 'classify-service-intent',
    'PR-05': 'rewrite-service-query',
    'PR-06': 'summarize-conversation',
    'PR-07': 'extract-document-fields',
    'PR-08': 'draft-customer-message',
    'PR-09': 'prepare-handoff-note',
}
SERVICE_FLOW_NAME = 'review-service-request'
PRODUCTION_ENVIRONMENT = 'production'
LEGACY_EXPERIMENT_DESCRIPTION = 'Authored historical illustration; no model or managed judge executed.'
EXPERIMENT_DESCRIPTION = 'Prompt version comparison against the regression dataset.'
LEGACY_SCORE_COMMENT_PREFIX = 'Authored fixture expectation; no judge executed. '


def experiment_run_name(prompt_id: str, version: int) -> str:
    label = {2: 'baseline', 4: 'candidate'}.get(int(version), 'comparison')
    return f'{prompt_by_id(prompt_id)["name"]} · v{version} {label}'


def normalize_operations(events: list[dict]) -> list[dict]:
    """Use operational names while retaining explicit replay provenance.

    This pure helper changes names, tags, environments and metadata only. IDs,
    timestamps, model accounting, payloads, score values and parent links stay intact.
    It is for authored events, never actual companion observations.
    """
    result = normalize_surface_descriptions(events)
    refs = defaultdict(dict)
    for event in result:
        if otlp.is_span(event):
            a = attributes(event)
            if a.get(otlp.OBS_TYPE) == 'generation':
                pid = a.get(otlp.OBS_METADATA_PREFIX + 'prompt_id')
                if pid not in ROOT_NAME_BY_PROMPT:
                    raise ValueError('Operational naming requires a known generation prompt ID.')
                refs[event['traceId']][pid] = int(a[otlp.PROMPT_VERSION])
    for event in result:
        if not otlp.is_span(event):
            if event.get('type') == 'score-create' and event['body'].get('environment') == 'production-history':
                event['body']['environment'] = PRODUCTION_ENVIRONMENT
            continue
        a = attributes(event)
        prompt_versions = refs[event['traceId']]
        if not prompt_versions:
            raise ValueError('Operational naming requires prompt generations in each trace.')
        pids = sorted(prompt_versions)
        name = ROOT_NAME_BY_PROMPT[pids[0]] if len(pids) == 1 else SERVICE_FLOW_NAME
        if otlp.is_trace_root(event):
            event['name'] = name
        if a.get(otlp.OBS_TYPE) == 'generation':
            event['name'] = 'generate-response'
        environment = 'experiment' if a.get('langfuse.environment') == 'experiment' else PRODUCTION_ENVIRONMENT
        changes = {
            'langfuse.trace.name': name,
            'langfuse.environment': environment,
            otlp.OBS_METADATA_PREFIX + 'cohort': environment,
            otlp.OBS_METADATA_PREFIX + 'evidence_kind': 'authored-synthetic-history',
            otlp.OBS_METADATA_PREFIX + 'evaluation_mode': 'replay',
        }
        if 'langfuse.experiment.name' in a:
            if len(pids) != 1:
                raise ValueError('Historical experiment naming requires exactly one prompt.')
            changes['langfuse.experiment.name'] = experiment_run_name(pids[0], prompt_versions[pids[0]])
        managed = set(changes) | {'langfuse.trace.tags'}
        event['attributes'] = [item for item in event['attributes'] if item['key'] not in managed]
        event['attributes'].extend(otlp.string_attr(key, value) for key, value in changes.items())
        event['attributes'].append({'key': 'langfuse.trace.tags', 'value': {
            'arrayValue': {'values': [{'stringValue': pid} for pid in pids]}}})
    return result


def normalize_surface_descriptions(events: list[dict]) -> list[dict]:
    """Remove only the exact legacy display wording; retain target provenance.

    Score values, subjects and the full remaining rubric comment stay unchanged.
    Authored/replay status remains explicit on every target observation metadata.
    """
    result = deepcopy(events)
    for event in result:
        if otlp.is_span(event):
            for item in event['attributes']:
                if (item['key'] == 'langfuse.experiment.description'
                        and item['value'].get('stringValue') == LEGACY_EXPERIMENT_DESCRIPTION):
                    item['value']['stringValue'] = EXPERIMENT_DESCRIPTION
        elif event.get('type') == 'score-create':
            comment = event['body'].get('comment')
            if isinstance(comment, str) and comment.startswith(LEGACY_SCORE_COMMENT_PREFIX):
                event['body']['comment'] = comment[len(LEGACY_SCORE_COMMENT_PREFIX):]
    return result
