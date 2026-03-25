"""Approval record model with SHA-256 hashing."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApprovalRecord:
    """Represents an approval decision for architecture generation.

    All 5 fields are required. decision must be "APPROVED".
    timestamp must be valid ISO 8601.
    """

    decision: str
    timestamp: str
    user_input: str
    action_type: str
    detail: str

    @staticmethod
    def compute_hash(action_type: str, detail: str, timestamp: str) -> str:
        """Compute SHA-256 hash of approval payload.

        Hash = SHA-256(action_type:detail:timestamp)
        """
        payload = f"{action_type}:{detail}:{timestamp}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def validate(self) -> list[str]:
        """Validate the approval record.

        Returns:
            List of error messages. Empty means valid.
        """
        errors: list[str] = []

        if self.decision != "APPROVED":
            errors.append(
                f'decision must be "APPROVED", got "{self.decision}"'
            )

        if not self.timestamp:
            errors.append("timestamp is required")
        else:
            try:
                datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
            except ValueError:
                errors.append(
                    f'timestamp must be valid ISO 8601, got "{self.timestamp}"'
                )

        if not self.action_type:
            errors.append("action_type is required")

        if not self.detail:
            errors.append("detail is required")

        return errors

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> ApprovalRecord:
        """Create an ApprovalRecord from a dict.

        Raises:
            KeyError: If required fields are missing.
        """
        return cls(
            decision=data["decision"],
            timestamp=data["timestamp"],
            user_input=data["user_input"],
            action_type=data["action_type"],
            detail=data["detail"],
        )

    def to_dict(self) -> dict[str, str]:
        """Convert to dict with computed hash included."""
        return {
            "decision": self.decision,
            "timestamp": self.timestamp,
            "user_input": self.user_input,
            "action_type": self.action_type,
            "detail": self.detail,
            "hash": self.compute_hash(
                self.action_type, self.detail, self.timestamp
            ),
        }
