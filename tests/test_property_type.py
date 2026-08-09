from datetime import datetime

from src.domain.assets.property_type import PropertyType


def test_string_accepts_string() -> None:
    assert PropertyType.STRING.validate("hello") is True


def test_string_rejects_non_string() -> None:
    assert PropertyType.STRING.validate(123) is False


def test_integer_accepts_integer() -> None:
    assert PropertyType.INTEGER.validate(123) is True


def test_integer_rejects_float() -> None:
    assert PropertyType.INTEGER.validate(123.5) is False


def test_integer_rejects_boolean() -> None:
    assert PropertyType.INTEGER.validate(True) is False


def test_float_accepts_float() -> None:
    assert PropertyType.FLOAT.validate(12.5) is True


def test_float_accepts_integer() -> None:
    assert PropertyType.FLOAT.validate(12) is True


def test_float_rejects_boolean() -> None:
    assert PropertyType.FLOAT.validate(True) is False


def test_float_rejects_string() -> None:
    assert PropertyType.FLOAT.validate("12.5") is False


def test_boolean_accepts_boolean() -> None:
    assert PropertyType.BOOLEAN.validate(True) is True
    assert PropertyType.BOOLEAN.validate(False) is True


def test_boolean_rejects_integer() -> None:
    assert PropertyType.BOOLEAN.validate(1) is False


def test_datetime_accepts_datetime() -> None:
    value = datetime.now()

    assert PropertyType.DATETIME.validate(value) is True


def test_datetime_rejects_string() -> None:
    assert PropertyType.DATETIME.validate("2026-08-09") is False
