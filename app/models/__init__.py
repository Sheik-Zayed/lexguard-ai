"""Models package — import all models here for SQLAlchemy discovery."""
from .user import User
from .document import Document, ClauseAnalysis
from .legal_case import LegalCase
from .lawyer import Lawyer
from .emergency_alert import EmergencyAlert

__all__ = ["User", "Document", "ClauseAnalysis", "LegalCase", "Lawyer", "EmergencyAlert"]
