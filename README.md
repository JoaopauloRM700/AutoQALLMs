# AutoQALLMs

AutoQALLMs generates automated browser test scripts from a website URL using an LLM. The original local workflow is the comparison CLI in `AUTOQAGPT_COMPARE_LLM'S.py`: it downloads HTML, extracts testable elements, requests Selenium Python code, executes the generated script in Chrome, and appends execution metrics to the dataset.

## Local CLI Workflow

Run these commands from the repository root:

```powershell
cd "D:\workspace\Testes exploratórios automatizados por agentes inteligentes em ambientes web\AutoQALLMs"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Fill `.env` with the key for the selected model:

```dotenv
OPENAI_API_KEY=
ANTHROPIC_KEY=
XAI_API_KEY=
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
```

Chrome must be installed locally. Start the original comparison workflow with:

```powershell
python ".\AUTOQAGPT_COMPARE_LLM'S.py"
```

The terminal asks for:

1. A target website URL.
2. A model choice: `gpt4`, `claude`, `grok`, or `gemini`.

During the run the terminal and execution log show:

1. URL and model used.
2. HTML retrieval completion and response size.
3. Extracted links, headings, images, forms, inputs, buttons, and selects.
4. LLM generation start and elapsed time.
5. A preview of the generated Selenium script.
6. Selenium execution output and passed/failed totals.
7. Paths of generated artifacts.

## Generated Files

Files are created relative to the directory where the CLI is started. When launched from the repository root, they are:

| File | Behavior |
| --- | --- |
| `generated_test.py` | Latest generated Selenium Python test; overwritten on each successful generation. |
| `training_dataset.json` | Accumulated execution summary and element fingerprints; appended after test execution. |
| `logs/autoqallms_YYYYMMDD_HHMMSS.log` | Full terminal-oriented trace for one CLI run. |

`generated_test.py`, `logs/`, `.env`, and `.venv/` are ignored by Git.

## Application Layout

- `AUTOQAGPT_COMPARE_LLM'S.py`: original local comparison flow with model selection, Selenium execution, dataset recording, and execution log.
- `logger.py`: JSON dataset persistence and timestamped log writing.
- `AUTOQAGPT.py`: earlier GPT-4-only CLI variant.
- `backend/`: FastAPI generation API introduced later.
- `frontend/`: React interface introduced later; its current code points to the hosted API rather than the local backend.

## Notes

- The CLI extracts server-returned HTML with `requests` and BeautifulSoup. Content rendered only after client-side JavaScript execution is not included in this extraction.
- Generated test code comes from the selected provider and is executed locally. Only run it against websites and accounts you are authorized to test.
- For a Google AI Studio key, set `GEMINI_API_KEY` locally and select `gemini`; the default model is `gemini-2.5-flash`.
