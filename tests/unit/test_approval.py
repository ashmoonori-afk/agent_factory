from __future__ import annotations

import hashlib

from factory.approval.records import ApprovalRecord


def _make_valid_record() -> ApprovalRecord:
    return ApprovalRecord(
        decision="APPROVED",
        timestamp="2026-03-25T14:30:00Z",
        user_input="YES",
        action_type="architecture_approval",
        detail="single-agent with csv-reader, sql-executor",
    )


def test_valid_record_has_no_errors() -> None:
    record = _make_valid_record()
    errors = record.validate()
    assert errors == []


def test_hash_is_deterministic() -> None:
    record = _make_valid_record()
    hash1 = ApprovalRecord.compute_hash(
        record.action_type, record.detail, record.timestamp
    )
    hash2 = ApprovalRecord.compute_hash(
        record.action_type, record.detail, record.timestamp
    )
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 hex digest


def test_hash_matches_expected() -> None:
    payload = (
        "architecture_approval:single-agent with csv-reader, sql-executor:2026-03-25T14:30:00Z"
    )
    expected = hashlib.sha256(payload.encode()).hexdigest()
    actual = ApprovalRecord.compute_hash(
        "architecture_approval",
        "single-agent with csv-reader, sql-executor",
        "2026-03-25T14:30:00Z",
    )
    assert actual == expected


def test_hash_changes_with_different_input() -> None:
    hash1 = ApprovalRecord.compute_hash("a", "b", "c")
    hash2 = ApprovalRecord.compute_hash("a", "b", "d")
    assert hash1 != hash2


def test_validate_rejects_non_approved_decision() -> None:
    record = _make_valid_record()
    record.decision = "REJECTED"
    errors = record.validate()
    assert len(errors) > 0
    assert any("APPROVED" in e for e in errors)


def test_validate_rejects_empty_decision() -> None:
    record = _make_valid_record()
    record.decision = ""
    errors = record.validate()
    assert len(errors) > 0


def test_validate_rejects_missing_timestamp() -> None:
    record = _make_valid_record()
    record.timestamp = ""
    errors = record.validate()
    assert len(errors) > 0


def test_validate_rejects_invalid_timestamp() -> None:
    record = _make_valid_record()
    record.timestamp = "not-a-date"
    errors = record.validate()
    assert len(errors) > 0


def test_validate_rejects_empty_action_type() -> None:
    record = _make_valid_record()
    record.action_type = ""
    errors = record.validate()
    assert len(errors) > 0


def test_from_dict_creates_record() -> None:
    data = {
        "decision": "APPROVED",
        "timestamp": "2026-03-25T14:30:00Z",
        "user_input": "YES",
        "action_type": "architecture_approval",
        "detail": "single-agent",
    }
    record = ApprovalRecord.from_dict(data)
    assert record.decision == "APPROVED"
    assert record.action_type == "architecture_approval"


def test_from_dict_raises_on_missing_field() -> None:
    data = {"decision": "APPROVED"}
    try:
        ApprovalRecord.from_dict(data)
        assert False, "Should have raised"
    except (KeyError, TypeError):
        pass


def test_to_dict_round_trips() -> None:
    record = _make_valid_record()
    data = record.to_dict()
    assert data["decision"] == "APPROVED"
    assert data["timestamp"] == "2026-03-25T14:30:00Z"
    assert "hash" in data
