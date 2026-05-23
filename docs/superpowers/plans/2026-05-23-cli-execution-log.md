# CLI Execution Log Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the original terminal-driven AutoQALLMs comparison flow while saving one readable execution log for each local run.

**Architecture:** Extend `logger.py`, which already owns persisted execution data, with a small `ExecutionLogger` that mirrors terminal messages into timestamped files under `logs/`. Wire only `AUTOQAGPT_COMPARE_LLM'S.py` to use it for extraction, generation, generated-script path, Selenium output, and dataset path; do not move modules or replace the original CLI workflow.

**Tech Stack:** Python 3 standard library `unittest`, existing Python CLI application, JSON dataset storage.

---

### Task 1: Timestamped Log Writer

**Files:**
- Create: `tests/test_logger.py`
- Modify: `logger.py`

- [x] **Step 1: Write the failing test**

```python
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from logger import ExecutionLogger


class ExecutionLoggerTests(unittest.TestCase):
    def test_write_creates_timestamped_log_and_mirrors_text(self):
        messages = []
        with tempfile.TemporaryDirectory() as directory:
            logger = ExecutionLogger(
                log_dir=directory,
                now=lambda: datetime(2026, 5, 23, 15, 30, 12),
                terminal_writer=messages.append,
            )
            logger.write("Fetching and Parsing HTML...")

            expected_path = Path(directory) / "autoqallms_20260523_153012.log"
            self.assertEqual(logger.path, expected_path)
            self.assertEqual(messages, ["Fetching and Parsing HTML..."])
            self.assertEqual(
                expected_path.read_text(encoding="utf-8"),
                "Fetching and Parsing HTML...\n",
            )
```

- [x] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_logger -v`

Expected: `ImportError` because `ExecutionLogger` does not yet exist.

- [x] **Step 3: Write minimal implementation**

```python
class ExecutionLogger:
    def __init__(self, log_dir="logs", now=datetime.now, terminal_writer=print):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.log_dir / f"autoqallms_{now().strftime('%Y%m%d_%H%M%S')}.log"
        self.terminal_writer = terminal_writer

    def write(self, message=""):
        self.terminal_writer(message)
        with self.path.open("a", encoding="utf-8") as log_file:
            log_file.write(f"{message}\n")
```

- [x] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_logger -v`

Expected: one passing test.

### Task 2: CLI Logging Integration

**Files:**
- Modify: `AUTOQAGPT_COMPARE_LLM'S.py`
- Modify: `.gitignore`

- [x] **Step 1: Route execution stages through the logger**

Create the logger after inputs are collected, replace the user-visible stage `print()` calls with `execution_log.write()`, and record absolute paths for `generated_test.py`, `training_dataset.json`, and the `.log` file. Keep the generated Selenium subprocess and JSON dataset behavior unchanged.

- [x] **Step 2: Ignore generated logs**

Add `logs/` to `.gitignore` so local run traces do not enter version control.

- [x] **Step 3: Verify Python syntax**

Run: `python -m py_compile logger.py "AUTOQAGPT_COMPARE_LLM'S.py"`

Expected: exit code `0`.

### Task 3: Local Execution Documentation

**Files:**
- Modify: `README.md`

- [x] **Step 1: Document the supported local CLI path**

Add setup steps for `.venv`, `.env` keys, the comparison CLI command, Chrome requirement, and generated artifact locations (`generated_test.py`, `training_dataset.json`, `logs/*.log`).

- [x] **Step 2: Run focused verification**

Run: `python -m unittest discover -s tests -p "test_*.py" -v`

Expected: all logger tests pass without invoking an external model or browser.
