"""Immediately forward kit progress to Depot's standard stdout log stream."""


def report(message: str) -> None:
    print(message, flush=True)
