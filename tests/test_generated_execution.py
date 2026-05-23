import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


def load_cli_module():
    script_path = next(Path(__file__).parents[1].glob("AUTOQAGPT_COMPARE*.py"))
    spec = importlib.util.spec_from_file_location("autoqallms_compare_execution", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GeneratedExecutionTests(unittest.TestCase):
    def test_generated_script_uses_active_python_interpreter(self):
        module = load_cli_module()
        execution_log = Mock()
        process_result = Mock(returncode=0, stdout="Test 1 Passed\n", stderr="")
        previous_directory = os.getcwd()

        with tempfile.TemporaryDirectory() as directory:
            os.chdir(directory)
            try:
                with patch("subprocess.run", return_value=process_result) as run:
                    result = module.execute_selenium_code(
                        "print('Test 1 Passed')",
                        execution_log,
                    )
            finally:
                os.chdir(previous_directory)

        run.assert_called_once_with(
            [sys.executable, "generated_test.py"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result, (1, 0))

    def test_generated_script_failure_is_not_reported_as_test_results(self):
        module = load_cli_module()
        execution_log = Mock()
        process_result = Mock(
            returncode=1,
            stdout="",
            stderr="ModuleNotFoundError: No module named 'selenium'",
        )
        previous_directory = os.getcwd()

        with tempfile.TemporaryDirectory() as directory:
            os.chdir(directory)
            try:
                with patch("subprocess.run", return_value=process_result):
                    with self.assertRaises(RuntimeError):
                        module.execute_selenium_code("print('test')", execution_log)
            finally:
                os.chdir(previous_directory)


if __name__ == "__main__":
    unittest.main()
