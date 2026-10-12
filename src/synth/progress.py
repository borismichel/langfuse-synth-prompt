"""Immediately forward kit progress to Depot's standard stdout log stream."""
from contextlib import contextmanager
import threading
import time


PROGRESS_INTERVAL_SECONDS = 15.0


def report(message: str) -> None:
    print(message, flush=True)


class _Progress:
    def __init__(self, log):
        self.log = log
        self.phase = ''
        self.changed_at = time.monotonic()
        self.lock = threading.Lock()

    def __call__(self, message):
        with self.lock:
            self.phase = message
            self.changed_at = time.monotonic()
            self.log(message)

    def heartbeat(self, done):
        while not done.wait(PROGRESS_INTERVAL_SECONDS):
            with self.lock:
                elapsed = time.monotonic() - self.changed_at
                if elapsed >= PROGRESS_INTERVAL_SECONDS:
                    self.log(f'Still waiting ({elapsed:.0f}s since last progress): {self.phase}')


@contextmanager
def progress_scope(label: str, log=report):
    """One heartbeat per command, shared by nested setup/verification phases.

    A wait notice describes elapsed time only, never invented completed work.
    Stop the helper on success or failure; exception messages may contain secrets.
    """
    if isinstance(log, _Progress):
        log(label)
        yield log
        return
    progress = _Progress(log)
    progress(label)
    done = threading.Event()
    worker = threading.Thread(target=progress.heartbeat, args=(done,), daemon=True)
    worker.start()
    try:
        yield progress
    except Exception as exc:
        progress(f'Work stopped ({type(exc).__name__}); inspect the failed step.')
        raise
    finally:
        done.set()
        worker.join()
