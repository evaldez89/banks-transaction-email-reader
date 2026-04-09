"""Email provider implementations."""

from infrastructure.email_providers.registry import email_provider_registry

from .gmail_email_provider import GmailEmailProvider

email_provider_registry.register("gmail", GmailEmailProvider)

__all__ = ["GmailEmailProvider"]
