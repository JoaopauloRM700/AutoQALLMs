# Gemini CLI Provider Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow the existing terminal workflow to generate Selenium code through a Google AI Studio Gemini API key.

**Architecture:** Add one REST-backed provider function to the existing comparison CLI, dispatch to it when the user selects `gemini`, and preserve the existing parsing, generated-script execution, log, and dataset behavior. Use the already-installed `requests` package rather than adding an SDK dependency.

**Tech Stack:** Python 3, `requests`, Google Gemini `generateContent` REST API, `unittest`.

---

### Task 1: Gemini REST Provider

**Files:**
- Create: `tests/test_gemini_provider.py`
- Modify: `AUTOQAGPT_COMPARE_LLM'S.py`

- [x] **Step 1: Write a failing provider test**

Create a unit test that loads the CLI script, replaces `requests.post`, invokes `generate_with_gemini("prompt")`, and asserts it calls the configured `gemini-2.5-flash:generateContent` endpoint with `GEMINI_API_KEY` and returns candidate text.

- [x] **Step 2: Verify failure**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_gemini_provider -v`

Expected: failure because `generate_with_gemini` is not implemented.

- [x] **Step 3: Implement the provider and dispatch**

Read `GEMINI_API_KEY` and optional `GEMINI_MODEL` from `.env`, POST the existing prompt to Gemini, return the generated text, accept `gemini` in the model prompt, and route model selection to the new function.

- [x] **Step 4: Verify the provider test**

Run: `.\.venv\Scripts\python.exe -m unittest tests.test_gemini_provider -v`

Expected: all Gemini provider tests pass.

### Task 2: Local Configuration And Verification

**Files:**
- Modify: `.env.example`
- Modify: `README.md`
- Modify locally ignored file: `.env`

- [x] **Step 1: Document Gemini setup**

Add `GEMINI_API_KEY` and `GEMINI_MODEL=gemini-2.5-flash` to the example and README, and explain selecting `gemini` in the CLI.

- [x] **Step 2: Prepare the local secret placeholder**

Add blank Gemini settings to `.env` without copying keys into tracked files; the user inserts the Google AI Studio key locally.

- [x] **Step 3: Verify all focused behavior**

Run: `.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v`

Run: `.\.venv\Scripts\python.exe -c "import pathlib, py_compile, runpy; script=next(pathlib.Path('.').glob('AUTOQAGPT_COMPARE*.py')); py_compile.compile(str(script), doraise=True); runpy.run_path(str(script), run_name='import_check')"`

Expected: tests and import/syntax verification pass without making an external Gemini request.
