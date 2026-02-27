"""Tests for data models.

Covers: ModelResponse new fields (role, routing, analysis), defaults,
and to_dict() serialization of all fields.
"""

from __future__ import annotations

from mutual_dissent.models import ModelResponse


class TestModelResponseDefaults:
    """New fields have correct default values."""

    def test_role_defaults_to_empty_string(self) -> None:
        r = ModelResponse(
            model_id="test/model",
            model_alias="test",
            round_number=0,
            content="hello",
        )
        assert r.role == ""

    def test_routing_defaults_to_none(self) -> None:
        r = ModelResponse(
            model_id="test/model",
            model_alias="test",
            round_number=0,
            content="hello",
        )
        assert r.routing is None

    def test_analysis_defaults_to_empty_dict(self) -> None:
        r = ModelResponse(
            model_id="test/model",
            model_alias="test",
            round_number=0,
            content="hello",
        )
        assert r.analysis == {}

    def test_analysis_default_is_independent(self) -> None:
        """Each instance gets its own dict (not shared mutable default)."""
        r1 = ModelResponse(model_id="test/model", model_alias="test", round_number=0, content="a")
        r2 = ModelResponse(model_id="test/model", model_alias="test", round_number=0, content="b")
        r1.analysis["score"] = 0.9
        assert "score" not in r2.analysis


class TestModelResponseToDict:
    """to_dict() includes all fields including new ones."""

    def test_to_dict_includes_role(self) -> None:
        r = ModelResponse(
            model_id="test/model",
            model_alias="test",
            round_number=0,
            content="hello",
            role="initial",
        )
        d = r.to_dict()
        assert d["role"] == "initial"

    def test_to_dict_includes_routing(self) -> None:
        routing = {"vendor": "anthropic", "mode": "auto", "via_openrouter": True}
        r = ModelResponse(
            model_id="test/model",
            model_alias="test",
            round_number=0,
            content="hello",
            routing=routing,
        )
        d = r.to_dict()
        assert d["routing"] == routing

    def test_to_dict_includes_analysis(self) -> None:
        r = ModelResponse(
            model_id="test/model",
            model_alias="test",
            round_number=0,
            content="hello",
            analysis={"score": 0.5},
        )
        d = r.to_dict()
        assert d["analysis"] == {"score": 0.5}

    def test_to_dict_defaults(self) -> None:
        """Default values appear correctly in to_dict() output."""
        r = ModelResponse(
            model_id="test/model",
            model_alias="test",
            round_number=0,
            content="hello",
        )
        d = r.to_dict()
        assert d["role"] == ""
        assert d["routing"] is None
        assert d["analysis"] == {}
