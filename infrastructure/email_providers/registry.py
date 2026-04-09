from typing import Callable

from domain.ports.email_provider import EmailProvider

type EmailProviderConstructor = Callable[..., EmailProvider]


class EmailProviderRegistry:
    """Factory that maps provider keys to constructors that produce EmailProvider instances."""

    def __init__(self) -> None:
        self._constructors: dict[str, EmailProviderConstructor] = {}

    def register(
        self, provider_key: str, constructor: EmailProviderConstructor
    ) -> None:
        self._constructors[provider_key] = constructor

    def get_provider(self, provider_key: str, **kwargs) -> EmailProvider:
        constructor = self._constructors.get(provider_key)
        if constructor is None:
            available = list(self._constructors.keys())
            raise ValueError(
                f"No provider registered for '{provider_key}'. Available: {available}"
            )
        return constructor(**kwargs)

    def get_available_providers(self) -> list[str]:
        return sorted(self._constructors.keys())


# Module-level singleton — import and use this instead of instantiating directly.
email_provider_registry = EmailProviderRegistry()
