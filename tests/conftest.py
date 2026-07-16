"""Test bootstrap for the UIT Portfolio Studio smoke suite.

Two things MUST happen before ``app`` is imported:
  1. Point ``UIT_DATA_DIR`` at a throwaway temp dir so tests never touch the
     operator's real ~/.uit-portfolio projects (DATA_DIR is resolved at import).
  2. Force ``CLAUDECODE=1`` so ``get_claude_bin()`` returns None and the app runs
     in DEMO mode — the whole suite runs with no Claude backend or credentials,
     which is exactly the path we want to keep from regressing.
"""

import os
import tempfile

# Set env BEFORE importing app (module-level, runs at collection time).
os.environ["UIT_DATA_DIR"] = tempfile.mkdtemp(prefix="uit-portfolio-test-")
os.environ["CLAUDECODE"] = "1"  # force demo mode; nested real CLI would crash anyway

import pytest
from fastapi.testclient import TestClient

import app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture
def client2():
    """A second browser — its own cookie jar, so its own session id. Used to
    verify one browser's projects are invisible to another's."""
    return TestClient(app_module.app)


@pytest.fixture
def app_mod():
    return app_module


def parse_sse(text: str):
    """Parse the SSE stream body into a list of (event, data) tuples."""
    events = []
    for block in text.split("\n\n"):
        block = block.strip("\n")
        if not block:
            continue
        ev, data_lines = None, []
        for line in block.split("\n"):
            if line.startswith("event: "):
                ev = line[len("event: "):]
            elif line.startswith("data: "):
                data_lines.append(line[len("data: "):])
        if ev is not None:
            events.append((ev, "\n".join(data_lines)))
    return events
