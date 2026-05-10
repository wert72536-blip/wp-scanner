from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Finding:
    def __init__(self, category: str, severity: str, description: str, recommendation: str):
        self.category = category
        self.severity = severity  # low, medium, high, critical
        self.description = description
        self.recommendation = recommendation

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "recommendation": self.recommendation
        }

class BaseDetector(ABC):
    @abstractmethod
    async def detect(
        self,
        session,
        url: str,
        parsed_url,
        html: str,
        headers: dict
    ) -> List[Finding]:
        """Run detection and return findings."""
        pass