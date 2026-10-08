"""Application-invoked reference resolution shared by live and authored history."""
from copy import deepcopy
from decimal import Decimal
import math
import re

CHAT_OPERATION_NAME = "handle-chat-turn"
GENERATION_OPERATION_NAME = "generate-response"
FEE_TOOL_NAME = "calculate-fee"
REFERENCE_RETRIEVER_NAME = "retrieve-product-context"


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


def withdrawal_count(prompt_id: str, message: str) -> int | None:
    """Recognise only an explicit monthly count in this current message.

    No number is inferred from history, hypothetical/quoted questions, ambiguous
    corrections, amounts, or a mention of a third withdrawal.
    """
    if prompt_id != "PR-02":
        return None
    match = re.fullmatch(
        r"I made (zero|one|two|three|four|five|six|seven|eight|nine|ten|[0-9]{1,6}) cash withdrawals this calendar month\. What withdrawal fee applies\?",
        message.strip(), flags=re.IGNORECASE)
    if match is None:
        return None
    value = match.group(1).lower()
    words = "zero one two three four five six seven eight nine ten".split()
    return words.index(value) if value in words else int(value)


def fee_arguments(prompt_id: str, message: str, reference: dict) -> dict | None:
    count = withdrawal_count(prompt_id, message)
    if count is None:
        return None
    rule = reference.get("cash_withdrawals")
    if not isinstance(rule, dict):
        raise ValueError("Product reference has invalid withdrawal rule")
    included, rate = rule.get("included_per_calendar_month"), rule.get("fee_each_after_included")
    if type(included) is not int or included < 0:
        raise ValueError("Product reference has invalid included withdrawal count")
    if type(rate) not in (int, float) or not math.isfinite(rate) or rate < 0:
        raise ValueError("Product reference has invalid withdrawal fee")
    if Decimal(str(rate)).as_tuple().exponent < -2:
        raise ValueError("Product reference withdrawal fee requires whole cents")
    if reference.get("currency") != "EUR":
        raise ValueError("Withdrawal calculator requires EUR reference")
    return {"source_id": reference["id"], "currency": reference["currency"],
            "period": "calendar_month", "withdrawal_count": count,
            "included_count": included, "fee_each_after_included": rate}


def calculate_fee(arguments: dict) -> dict:
    """Calculate an explanation from supplied facts; never inspect an account."""
    chargeable = max(0, arguments["withdrawal_count"] - arguments["included_count"])
    total = Decimal(str(arguments["fee_each_after_included"])) * chargeable
    return {"currency": arguments["currency"], "period": arguments["period"],
            "chargeable_withdrawals": chargeable, "total_fee": format(total, ".2f")}


def generation_reference(reference: dict, arguments: dict | None, result: dict | None) -> dict:
    """Keep original reference facts separate from derived model context."""
    context = deepcopy(reference)
    if arguments is not None and result is not None:
        context["calculation_results"] = [{"operation": FEE_TOOL_NAME,
                                           "arguments": deepcopy(arguments), "result": deepcopy(result)}]
    return context
