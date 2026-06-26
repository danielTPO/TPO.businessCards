# bizcard

Professional business card generator with the **Anthropic / Claude design language** — clean, minimal, and print-ready.

Produces 300 DPI PDFs with embedded fonts and CMYK-safe RGB colours, plus PNG/JPEG screen previews. Batch-processes CSV/JSON contact lists and emits a contact-sheet proof PDF for print sign-off.

---

## Quick start

```bash
# 1. Clone and install
git clone https://github.com/tpo-group/bizcard.git && cd bizcard
pip install -e .

# 2. Download Inter fonts (one-time setup)
python scripts/download_fonts.py

# 3. Generate a single card
python -m bizcard generate \
  --name "Daniel Landry" \
  --title "Intern" \
  --phone "(xxx) xxx-xxxx" \
  --email "d@tpo.group" \
  --signal "daniellandry" \
  --qr-url "https://linkedin.com/in/daniellandry" \
  --output ./output
  
# 4. Batch generate from CSV
python -m bizcard batch \
  --input examples/sample_contacts.csv \
  --template claude-dark \
  --output ./output/

# 5. Contact-sheet proof PDF
python -m bizcard preview \
  --input examples/sample_contacts.csv \
  --output ./output/
```

---

## Design language

The default templates (`claude-minimal` and `claude-dark`) implement the Anthropic visual identity:

| Token | Light | Dark |
|---|---|---|
| Background | `#FFFFFF` | `#0D0D0D` |
| Primary text | `#1A1A1A` | `#F5F5F0` |
| Secondary text | `#6B6B6B` | `#9A9A94` |
| Accent (copper) | `#C96A3A` | `#C96A3A` |

**Anatomy of a claude-minimal card:**

```
┌──────────────────────────────────────────┐
│                                          │
│  Jane Smith                      J S    │  ← name (Inter Bold 18pt) + monogram
│  Senior Engineer                         │  ← title (Inter Regular 9pt, grey)
│                                          │
│ ─────────────────────────────────────── │  ← copper accent rule (0.5pt)
│                                          │
│  Acme Corp                               │  ← company (Inter Medium 8.5pt)
│  jane@acme.com                           │  ← details (Inter Regular 8pt, grey)
│  +1 555 000 1234                         │
│  acme.com                                │
│                                          │
└──────────────────────────────────────────┘
```

---

## Project structure

```
bizcard/
├── __init__.py
├── __main__.py          # python -m bizcard entry point
├── cli.py               # click CLI (generate / batch / preview / list-templates)
├── config.py            # DesignTokens + BizCardSettings (env vars)
├── models/
│   ├── contact.py       # Contact — validated data model
│   └── card.py          # CardSpec — physical dimensions
├── templates/
│   ├── base.py          # BaseTemplate + RenderContext abstraction
│   ├── claude_minimal.py  # Reference implementation (light)
│   ├── claude_dark.py     # Dark variant
│   └── registry.py      # TemplateRegistry factory
├── services/
│   ├── ingest.py        # CSV / JSON / vCard ingestion
│   ├── layout.py        # Layout planning
│   ├── render.py        # RenderService (PDF + image)
│   ├── export.py        # ExportService (file I/O + contact sheet)
│   └── qr.py            # QR code generation
└── assets/fonts/        # Inter TTF files (downloaded separately)
```

---

## CLI reference

### `generate` — single card

```
python -m bizcard generate [OPTIONS]

  --name TEXT          Full name (required)
  --title TEXT         Job title
  --company TEXT       Company name
  --email TEXT         Email address
  --phone TEXT         Phone number
  --website TEXT       Website URL
  --linkedin TEXT      LinkedIn handle or URL
  --address TEXT       Mailing address
  --logo PATH          Logo image file (PNG)
  --qr-url TEXT        URL to encode as a QR code
  --back / --no-back   Include back face
  --png / --no-png     Also write PNG preview
  -t, --template TEXT  Template name  [default: claude-minimal]
  --orientation        landscape | portrait  [default: landscape]
  -o, --output PATH    Output directory  [default: ./output]
```

### `batch` — multiple contacts

```
python -m bizcard batch --input contacts.csv --template claude-dark --output ./cards/
```

Accepts `.csv`, `.json`, and `.vcf` (vCard) files.

### `preview` — contact-sheet proof

```
python -m bizcard preview --input contacts.csv --output ./cards/
```

Generates a US Letter PDF with all cards laid out in a grid for print sign-off.

### `list-templates`

```
python -m bizcard list-templates
```

---

## Programmatic API

```python
from bizcard.models.card import CardSpec
from bizcard.models.contact import Contact
from bizcard.services.export import ExportService
from bizcard.services.render import RenderService
from bizcard.templates.registry import TemplateRegistry

contact = Contact(
    name="Jane Smith",
    title="Senior Engineer",
    company="Acme Corp",
    email="jane@acme.com",
)

spec = CardSpec.standard_landscape(dpi=300)
renderer = RenderService(spec=spec)
template = TemplateRegistry.get("claude-minimal")

# Render to bytes (no file I/O)
pdf_bytes = renderer.render_pdf(contact, template)
preview_img = renderer.render_image(contact, template, dpi=150)

# Export to disk
exporter = ExportService(output_dir="./output")
paths = exporter.generate_card(contact, template, pdf=True, png=True)
```

---

## Adding a new template

1. Create `bizcard/templates/my_template.py`:

```python
from bizcard.config import DesignTokens, hex_to_rgb
from bizcard.templates.base import BaseTemplate, RenderContext
from bizcard.models.contact import Contact

class MyTemplate(BaseTemplate):
    @property
    def name(self) -> str:
        return "my-template"

    @property
    def description(self) -> str:
        return "My custom card style"

    def design_tokens(self) -> DesignTokens:
        return DesignTokens(
            bg_color="#2D2D2D",
            text_primary="#FFFFFF",
            accent_color="#00D1FF",
        )

    def render(self, contact: Contact, ctx: RenderContext) -> None:
        t = self.design_tokens()
        ctx.fill_background(hex_to_rgb(t.bg_color))
        ctx.draw_text(
            t.margin_left, t.margin_top,
            contact.name,
            font_name=t.font_display,
            size_pt=t.size_name,
            color=hex_to_rgb(t.text_primary),
        )
        # ... add more drawing calls
```

2. Register it (once, at application startup):

```python
from bizcard.templates.registry import TemplateRegistry
from my_template import MyTemplate

TemplateRegistry.register(MyTemplate)
```

No changes to core rendering or export code required.

---

## Configuration

All settings can be overridden via environment variables (prefix `BIZCARD_`):

```bash
BIZCARD_OUTPUT_DIR=/tmp/cards
BIZCARD_DPI=600
BIZCARD_PREVIEW_DPI=150
BIZCARD_DEFAULT_TEMPLATE=claude-dark
BIZCARD_DEFAULT_ORIENTATION=portrait
```

Or via a `.env` file in the working directory.

---

## Docker

```bash
docker build -t bizcard .

docker run --rm -v "$PWD/output:/data/output" bizcard generate --name "Jane Smith" --title "Senior Engineer" --email jane@acme.com --output /data/output/

For the web app, run:

```bash
docker run --rm -p 8000:8000 --env-file .env bizcard
```
```

The Dockerfile downloads the Inter font family automatically during the build.

---

## Development

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v
python -m pytest tests/ --cov=bizcard --cov-report=term-missing
```

---

## Font setup

The Inter font family (SIL Open Font Licence 1.1) is not bundled. Run once after cloning:

```bash
python scripts/download_fonts.py
```

Or place TTF files manually in `bizcard/assets/fonts/`:
- `Inter-Regular.ttf`
- `Inter-Medium.ttf`
- `Inter-Bold.ttf`
- `Inter-Light.ttf`
- `Inter-SemiBold.ttf`

If fonts are missing the application falls back to Helvetica (ReportLab built-in) and PIL's default bitmap font — output will render but without the intended typography.

---

## Output files

| File | Description |
|---|---|
| `{last}_{first}_businesscard.pdf` | Print-ready PDF at 300 DPI with bleed |
| `{last}_{first}_businesscard.png` | Screen preview PNG at 150 DPI |
| `contact_sheet.pdf` | Multi-card proof layout on US Letter pages |

---

## License

MIT
