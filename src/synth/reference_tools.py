"""Application-invoked reference resolution shared by live and authored history."""
from copy import deepcopy

REFERENCE_TOOL_NAME = "resolve_product_reference"
REFERENCE_RETRIEVER_NAME = "read_product_record"


def reference_arguments(prompt_id: str) -> dict:
    if prompt_id not in {"PR-01", "PR-02", "PR-03"}:
        raise ValueError("Reference resolution requires a connected assistant")
    return {"source_id": "SRC-01", "prompt_id": prompt_id}


def validate_reference(record: dict, arguments: dict) -> dict:
    """Check the local catalog contract before making its facts model context.

    No account lookup or external financial service is performed. A missing or
    malformed record fails the turn instead of supplying incomplete facts.
    """
    reference_arguments(arguments["prompt_id"])
    required = {"id", "name", "currency", "monthly_fee", "waiver", "eligibility",
                "card_replacement_fee", "cash_withdrawals", "opening_documents",
                "processing_time", "unknowns", "action_boundary"}
    if not isinstance(record, dict) or not required <= record.keys():
        raise ValueError("Product reference is incomplete")
    if record["id"] != arguments["source_id"]:
        raise ValueError("Product reference identity mismatch")
    for key in ("monthly_fee", "card_replacement_fee"):
        if type(record[key]) not in (int, float) or record[key] < 0:
            raise ValueError("Product reference has invalid fee fields")
    if not isinstance(record["waiver"], dict) or not {"fee", "condition", "exclusions", "timing"} <= record["waiver"].keys():
        raise ValueError("Product reference has incomplete waiver conditions")
    for key in ("eligibility", "opening_documents", "unknowns"):
        if not isinstance(record[key], list) or not record[key]:
            raise ValueError("Product reference has incomplete conditions")
    return deepcopy(record)
