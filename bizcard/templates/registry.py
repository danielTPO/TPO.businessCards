"""Template registry and factory.

The registry maps template slug names to their :class:`~bizcard.templates.base.BaseTemplate`
subclasses.  New templates are added by calling :meth:`TemplateRegistry.register`
— no changes to core rendering or export code are required.

Built-in templates are registered at module import time.  Third-party packages
can register additional templates via the ``bizcard.templates`` entry-point
group defined in ``pyproject.toml``.

Example — adding a custom template::

    from bizcard.templates.registry import TemplateRegistry
    from bizcard.templates.base import BaseTemplate

    class AcmeTemplate(BaseTemplate):
        name = "acme"
        ...

    TemplateRegistry.register(AcmeTemplate)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from bizcard.templates.base import BaseTemplate

log = logging.getLogger(__name__)

_REGISTRY: dict[str, "BaseTemplate"] = {}


class TemplateRegistry:
    """Singleton registry that maps template names to instances.

    All access is class-method based — you never instantiate this class.
    """

    @classmethod
    def register(cls, template_class: Type["BaseTemplate"]) -> None:
        """Register a template class.

        Args:
            template_class: A concrete subclass of :class:`BaseTemplate`.

        Raises:
            ValueError: If a template with the same name is already registered.
        """
        instance = template_class()
        name = instance.name
        if name in _REGISTRY:
            log.warning("Template '%s' already registered — overwriting", name)
        _REGISTRY[name] = instance
        log.debug("Registered template '%s'", name)

    @classmethod
    def get(cls, name: str) -> "BaseTemplate":
        """Return the template instance for *name*.

        Args:
            name: The template slug, e.g. ``"claude-minimal"``.

        Raises:
            KeyError: If no template with that name is registered.
        """
        _ensure_defaults_registered()
        try:
            return _REGISTRY[name]
        except KeyError:
            available = ", ".join(sorted(_REGISTRY))
            raise KeyError(
                f"Unknown template '{name}'. Available: {available}"
            ) from None

    @classmethod
    def list_templates(cls) -> list["BaseTemplate"]:
        """Return all registered template instances, sorted by name."""
        _ensure_defaults_registered()
        return sorted(_REGISTRY.values(), key=lambda t: t.name)

    @classmethod
    def names(cls) -> list[str]:
        """Return sorted list of registered template names."""
        _ensure_defaults_registered()
        return sorted(_REGISTRY)


_defaults_registered = False


def _ensure_defaults_registered() -> None:
    """Lazily register the built-in templates on first access."""
    global _defaults_registered
    if _defaults_registered:
        return
    _defaults_registered = True

    from bizcard.templates.tpo_standard import TPOStandardTemplate
    from bizcard.templates.claude_minimal import ClaudeMinimalTemplate
    from bizcard.templates.claude_dark import ClaudeDarkTemplate
    from bizcard.templates.anthropic_light import AnthropicLightTemplate
    from bizcard.templates.anthropic_dark import AnthropicDarkTemplate

    for cls in (
        TPOStandardTemplate,
        ClaudeMinimalTemplate,
        ClaudeDarkTemplate,
        AnthropicLightTemplate,
        AnthropicDarkTemplate,
    ):
        instance = cls()
        _REGISTRY[instance.name] = instance
        log.debug("Auto-registered built-in template '%s'", instance.name)
