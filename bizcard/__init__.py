"""
bizcard — Professional business card generator with Anthropic/Claude design language.

Programmatic usage::

    from bizcard.models.contact import Contact
    from bizcard.templates.registry import TemplateRegistry
    from bizcard.services.render import RenderService
    from bizcard.services.export import ExportService

    contact = Contact(
        name="Jane Smith",
        title="Senior Engineer",
        company="Acme Corp",
        email="jane@acme.com",
    )
    template = TemplateRegistry.get("claude-minimal")
    renderer = RenderService()
    exporter = ExportService(output_dir="./cards")
    exporter.export_pdf(renderer.render_pdf(contact, template), contact)
"""

__version__ = "0.1.0"
__author__ = "TPO Group"
