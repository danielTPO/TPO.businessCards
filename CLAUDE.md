# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A business card generator for TPO Group. It has two parts that share the `bizcard/` Python package:

1. **CLI tool** (`python -m bizcard`) — generates print-ready PDFs and PNG previews from CSV/JSON/vCard contact lists.
2. **Web ordering system** — a React/Vite frontend (`src/`) + a Python serverless API (`api/orders.py`) deployed on Vercel. The API generates a PDF, uploads it to Vercel Blob, and submits a print job to Cloudprinter CloudCore.

## Commands

### Python CLI
```bash
pip install -e ".[dev]"          # install with dev deps
python -m bizcard --help         # list commands
python -m bizcard generate --name "Jane Smith" --email jane@tpo.group --output ./output
python -m bizcard batch --input examples/sample_contacts.csv --output ./output
python -m pytest tests/ -v
python -m pytest tests/ --cov=bizcard --cov-report=term-missing
```

### Web app (Docker)
```bash
docker build -t tpo-bizcard .
docker run --rm -p 8000:8000 --env-file .env tpo-bizcard
# open http://localhost:8000
```

### Local dev (frontend + API separately)
```bash
# Terminal 1 — Python API
pip install -e ".[dev]" && pip install -r requirements.txt
uvicorn api.orders:app --reload --port 8000

# Terminal 2 — Vite (proxies /api → localhost:8000)
npm install && npm run dev
```

## Architecture

### Python package (`bizcard/`)

Data flows: `ingest.py` → `Contact` model → `RenderService` → `ExportService`

- **`models/contact.py`** — `Contact` is a Pydantic model; the only required field is `name`.
- **`models/card.py`** — `CardSpec` holds physical dimensions and DPI. Use `CardSpec.standard_landscape(dpi=300)` as the default.
- **`templates/`** — each template subclasses `BaseTemplate` and implements `render(contact, ctx)` using a `RenderContext` drawing API. Templates are looked up by name string via `TemplateRegistry.get("template-name")`. The active templates are: `tpo-standard`, `claude-minimal`, `claude-dark`, `anthropic-light`, `anthropic-dark`.
- **`services/render.py`** — `RenderService` drives ReportLab (PDF) and Pillow (PNG). It calls `template.render()` with a `RenderContext` that wraps both backends.
- **`services/export.py`** — `ExportService` handles file naming, output directories, and the contact-sheet proof PDF.
- **`config.py`** — `DesignTokens` (colours, fonts, sizes) and `BizCardSettings` (env vars prefixed `BIZCARD_`).

### Web API (`api/`)

`api/orders.py` is a FastAPI app run with uvicorn. In production it also serves the built React frontend from `dist/` via `StaticFiles`. The flow for `POST /api/orders`:
1. `_generator.py` — renders PDF bytes via `bizcard` + template `tpo-standard`
2. `_storage.py` — uploads to Vercel Blob (needs `BLOB_READ_WRITE_TOKEN`)
3. `_cloudprinter.py` — submits print job to Cloudprinter CloudCore (needs `CLOUDPRINTER_API_KEY`)

Required env vars (copy `.env.example` → `.env`):
- `CLOUDPRINTER_API_KEY`
- `CLOUDPRINTER_WEBHOOK_KEY`
- `BLOB_READ_WRITE_TOKEN`

### Frontend (`src/`)

React 18 + Vite. Single-page form that POSTs to `/api/orders`. Key components:
- `OrderForm.jsx` — the submission form; validates `@tpo.group` email client-side before posting
- `CardPreview.jsx` — static visual of the card design
- `StatusBanner.jsx` — success/error feedback after submission

## Fonts

All font files are committed to `bizcard/assets/fonts/`. Do not add a download step to the Dockerfile — the `COPY . .` instruction brings them along. The `scripts/download_fonts.py` script is only for local developer setup (when fonts are missing after a fresh clone that skips LFS or similar).

## Adding a new template

1. Create `bizcard/templates/my_template.py` subclassing `BaseTemplate` — implement `name`, `description`, `design_tokens()`, and `render()`.
2. Add it to the `_ensure_defaults_registered()` list in `bizcard/templates/registry.py`.
