from abc import ABC, abstractmethod


class EmailProvider[TRawMessage, TTransaction](ABC):
    @abstractmethod
    def authenticate(self) -> None:
        """Authenticate against the remote email provider."""

    @abstractmethod
    def build_service(self) -> None:
        """Initialize provider client/service objects after authentication."""

    @abstractmethod
    def build_query(self) -> str:
        """Build a provider-specific query string from neutral search criteria."""

    @abstractmethod
    def fetch_emails(self) -> list[TRawMessage]:
        """Retrieve raw messages from the provider."""

    @abstractmethod
    def get_transactions(self) -> list[TTransaction]:
        """Parse fetched raw messages into transactions."""
