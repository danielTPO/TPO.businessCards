"""Command-line interface for bizcard.

Usage examples::

    python -m bizcard generate \\
        --name "Jane Smith" --title "Senior Engineer" --company "Acme Corp" \\
        --email jane@acme.com --phone "+1 555 000 1234" --website acme.com \\
        --template claude-minimal --orientation landscape --output ./cards/

    python -m bizcard batch --input contacts.csv --template claude-dark --output ./cards/

    python -m bizcard preview --input contacts.csv --output contact_sheet.pdf

    python -m bizcard list-templates
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

import click
import structlog

from bizcard.config import settings
from bizcard.models.card import CardSpec, Orientation
from bizcard.services.export import ExportService
from bizcard.services.ingest import IngestError, IngestService
from bizcard.services.render import RenderService
from bizcard.templates.registry import TemplateRegistry


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=level,
    )


# ---------------------------------------------------------------------------
# Shared options
# ---------------------------------------------------------------------------

_OUTPUT_DIR_OPT = click.option(
    "--output", "-o",
    default=None,
    show_default=False,
    help="Output directory (default: ./output).",
    type=click.Path(file_okay=False, writable=True),
)

_TEMPLATE_OPT = click.option(
    "--template", "-t",
    default=settings.default_template,
    show_default=True,
    help="Template name (use list-templates to see all options).",
)

_ORIENTATION_OPT = click.option(
    "--orientation",
    type=click.Choice(["landscape", "portrait"], case_sensitive=False),
    default=settings.default_orientation,
    show_default=True,
    help="Card orientation.",
)

_VERBOSE_OPT = click.option(
    "--verbose", "-v",
    is_flag=True,
    default=False,
    help="Enable debug logging.",
)


# ---------------------------------------------------------------------------
# Root group
# ---------------------------------------------------------------------------

@click.group()
@click.version_option()
@_VERBOSE_OPT
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """bizcard — Professional business card generator.

    Renders print-ready PDFs and preview images using the Anthropic / Claude
    design language.  Use a subcommand to generate individual cards, process
    a batch, or produce a contact-sheet proof PDF.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    _configure_logging(verbose)


# ---------------------------------------------------------------------------
# generate — single card
# ---------------------------------------------------------------------------

@cli.command("generate")
@click.option("--name", required=True, help="Full name (required).")
@click.option("--title", default=None, help="Job title.")
@click.option("--company", default=None, help="Company / organisation name.")
@click.option("--email", default=None, help="Email address.")
@click.option("--phone", default=None, help="Phone number.")
@click.option("--website", default=None, help="Website URL.")
@click.option("--linkedin", default=None, help="LinkedIn handle or URL.")
@click.option("--address", default=None, help="Mailing address.")
@click.option("--logo", default=None, help="Path to a logo file (PNG).", type=click.Path(exists=True))
@click.option("--qr-url", default=None, help="URL to encode in a QR code on the card.")
@click.option("--back/--no-back", default=False, help="Include a back face.")
@click.option("--png/--no-png", default=False, help="Also write a PNG preview.")
@_TEMPLATE_OPT
@_ORIENTATION_OPT
@_OUTPUT_DIR_OPT
@click.pass_context
def generate(
    ctx: click.Context,
    name: str,
    title: Optional[str],
    company: Optional[str],
    email: Optional[str],
    phone: Optional[str],
    website: Optional[str],
    linkedin: Optional[str],
    address: Optional[str],
    logo: Optional[str],
    qr_url: Optional[str],
    back: bool,
    png: bool,
    template: str,
    orientation: str,
    output: Optional[str],
) -> None:
    """Generate a business card for a single contact."""
    from bizcard.models.contact import Contact

    _configure_logging(ctx.obj.get("verbose", False))

    out_dir = Path(output) if output else settings.output_dir
    spec = CardSpec.standard_landscape(dpi=settings.dpi)
    if orientation == "portrait":
        spec = CardSpec.standard_portrait(dpi=settings.dpi)

    try:
        tmpl = TemplateRegistry.get(template)
    except KeyError as exc:
        raise click.ClickException(str(exc)) from exc

    contact = Contact(
        name=name,
        title=title,
        company=company,
        email=email,
        phone=phone,
        website=website,
        linkedin=linkedin,
        address=address,
        logo_path=Path(logo) if logo else None,
        qr_url=qr_url,
    )

    renderer = RenderService(spec=spec)
    exporter = ExportService(output_dir=out_dir, renderer=renderer)

    paths = exporter.generate_card(
        contact, tmpl,
        pdf=True,
        png=png,
        include_back=back,
        preview_dpi=settings.preview_dpi,
    )

    for fmt, path in paths.items():
        click.echo(f"  [{fmt.upper()}] {path}")


# ---------------------------------------------------------------------------
# batch — multiple contacts from a file
# ---------------------------------------------------------------------------

@cli.command("batch")
@click.option(
    "--input", "-i", "input_file",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Input file (CSV, JSON, or vCard .vcf).",
)
@click.option("--back/--no-back", default=False, help="Include a back face.")
@click.option("--png/--no-png", default=False, help="Also write PNG previews.")
@_TEMPLATE_OPT
@_ORIENTATION_OPT
@_OUTPUT_DIR_OPT
@click.pass_context
def batch(
    ctx: click.Context,
    input_file: str,
    back: bool,
    png: bool,
    template: str,
    orientation: str,
    output: Optional[str],
) -> None:
    """Generate cards for all contacts in a CSV, JSON, or vCard file."""
    _configure_logging(ctx.obj.get("verbose", False))

    path = Path(input_file)
    out_dir = Path(output) if output else settings.output_dir

    spec = (
        CardSpec.standard_portrait(dpi=settings.dpi)
        if orientation == "portrait"
        else CardSpec.standard_landscape(dpi=settings.dpi)
    )

    try:
        tmpl = TemplateRegistry.get(template)
    except KeyError as exc:
        raise click.ClickException(str(exc)) from exc

    ingest = IngestService()
    try:
        contacts = ingest.from_file(path)
    except IngestError as exc:
        raise click.ClickException(str(exc)) from exc

    if not contacts:
        click.echo("No valid contacts found in input file.", err=True)
        sys.exit(1)

    click.echo(f"Loaded {len(contacts)} contact(s) from {path.name}")

    renderer = RenderService(spec=spec)
    exporter = ExportService(output_dir=out_dir, renderer=renderer)

    results = exporter.generate_batch(
        contacts, tmpl,
        pdf=True,
        png=png,
        include_back=back,
        preview_dpi=settings.preview_dpi,
    )

    click.echo(f"\nGenerated {len(results)} card(s) in {out_dir}/")


# ---------------------------------------------------------------------------
# preview — contact sheet PDF
# ---------------------------------------------------------------------------

@cli.command("preview")
@click.option(
    "--input", "-i", "input_file",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Input file (CSV, JSON, or vCard .vcf).",
)
@click.option(
    "--output-file", "-O",
    default="contact_sheet.pdf",
    show_default=True,
    help="Output filename for the contact sheet PDF.",
)
@click.option(
    "--cards-per-row",
    default=2,
    show_default=True,
    type=int,
    help="Number of card columns per proof page.",
)
@_TEMPLATE_OPT
@_ORIENTATION_OPT
@_OUTPUT_DIR_OPT
@click.pass_context
def preview(
    ctx: click.Context,
    input_file: str,
    output_file: str,
    cards_per_row: int,
    template: str,
    orientation: str,
    output: Optional[str],
) -> None:
    """Generate a contact-sheet proof PDF showing all cards on print pages."""
    _configure_logging(ctx.obj.get("verbose", False))

    path = Path(input_file)
    out_dir = Path(output) if output else settings.output_dir

    spec = (
        CardSpec.standard_portrait(dpi=settings.dpi)
        if orientation == "portrait"
        else CardSpec.standard_landscape(dpi=settings.dpi)
    )

    try:
        tmpl = TemplateRegistry.get(template)
    except KeyError as exc:
        raise click.ClickException(str(exc)) from exc

    ingest = IngestService()
    try:
        contacts = ingest.from_file(path)
    except IngestError as exc:
        raise click.ClickException(str(exc)) from exc

    if not contacts:
        click.echo("No valid contacts found in input file.", err=True)
        sys.exit(1)

    click.echo(f"Loaded {len(contacts)} contact(s) — generating contact sheet…")

    renderer = RenderService(spec=spec)
    exporter = ExportService(output_dir=out_dir, renderer=renderer)

    sheet_path = exporter.generate_contact_sheet(
        contacts, tmpl,
        output_name=output_file,
        cards_per_row=cards_per_row,
        preview_dpi=settings.preview_dpi,
    )
    click.echo(f"  [SHEET] {sheet_path}")


# ---------------------------------------------------------------------------
# list-templates
# ---------------------------------------------------------------------------

@cli.command("list-templates")
def list_templates() -> None:
    """List all available card templates."""
    templates = TemplateRegistry.list_templates()
    if not templates:
        click.echo("No templates registered.")
        return
    click.echo("\nAvailable templates:\n")
    for tmpl in templates:
        marker = " (default)" if tmpl.name == settings.default_template else ""
        click.echo(f"  {tmpl.name}{marker}")
        click.echo(f"    {tmpl.description}")
    click.echo()
