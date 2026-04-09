"""Conftest: trigger all registrations so the singletons are populated for every test."""

import infrastructure.parsers.banks  # noqa: F401
import mail_services  # noqa: F401
