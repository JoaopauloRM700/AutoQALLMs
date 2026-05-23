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

    def test_new_execution_does_not_reuse_log_from_same_second(self):
        with tempfile.TemporaryDirectory() as directory:
            fixed_time = lambda: datetime(2026, 5, 23, 15, 30, 12)
            first = ExecutionLogger(
                log_dir=directory,
                now=fixed_time,
                terminal_writer=lambda message: None,
            )
            first.write("First execution")

            second = ExecutionLogger(
                log_dir=directory,
                now=fixed_time,
                terminal_writer=lambda message: None,
            )
            second.write("Second execution")

            self.assertNotEqual(first.path, second.path)
            self.assertEqual(
                second.path.read_text(encoding="utf-8"),
                "Second execution\n",
            )


if __name__ == "__main__":
    unittest.main()
