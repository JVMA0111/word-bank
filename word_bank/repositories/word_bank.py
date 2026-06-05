from __future__ import annotations

from typing import Any

from word_bank.auth import get_current_user
from word_bank.db import get_connection
from word_bank.db.schema import TABLES


def _rows_to_dicts(rows: list) -> list[dict[str, Any]]:
    return rows  # get_connection já retorna dicts


def _fetch_all(table: str) -> list[dict[str, Any]]:
    uid = get_current_user()
    with get_connection() as conn:
        rows = conn.execute(
            f"SELECT * FROM {table} WHERE user_id = %s ORDER BY id", (uid,)
        ).fetchall()
    return rows


def _insert(table: str, data: dict[str, Any]) -> None:
    uid = get_current_user()
    payload = {"user_id": uid, **data}
    columns = ", ".join(payload.keys())
    placeholders = ", ".join(["%s"] * len(payload))
    with get_connection() as conn:
        conn.execute(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
            tuple(payload.values()),
        )


def _update(table: str, row_id: int, data: dict[str, Any]) -> None:
    uid = get_current_user()
    assignments = ", ".join(f"{col} = %s" for col in data)
    with get_connection() as conn:
        conn.execute(
            f"UPDATE {table} SET {assignments} WHERE id = %s AND user_id = %s",
            (*data.values(), row_id, uid),
        )


def _delete(table: str, row_id: int) -> None:
    uid = get_current_user()
    with get_connection() as conn:
        conn.execute(
            f"DELETE FROM {table} WHERE id = %s AND user_id = %s", (row_id, uid)
        )


def count_rows(table: str) -> int:
    uid = get_current_user()
    with get_connection() as conn:
        row = conn.execute(
            f"SELECT COUNT(*) AS n FROM {table} WHERE user_id = %s", (uid,)
        ).fetchone()
    return row["n"] if row else 0


def get_stats() -> dict[str, int]:
    return {table: count_rows(table) for table in TABLES}


def is_empty() -> bool:
    return all(count_rows(t) == 0 for t in TABLES)


# --- Verbs ---

def list_verbs() -> list[dict]:
    return _fetch_all("verbs")


def add_verb(data: dict) -> None:
    _insert("verbs", data)


def update_verb(row_id: int, data: dict) -> None:
    _update("verbs", row_id, data)


def delete_verb(row_id: int) -> None:
    _delete("verbs", row_id)


def list_be_forms() -> list[dict]:
    return _fetch_all("be_forms")


def add_be_form(data: dict) -> None:
    _insert("be_forms", data)


def update_be_form(row_id: int, data: dict) -> None:
    _update("be_forms", row_id, data)


def delete_be_form(row_id: int) -> None:
    _delete("be_forms", row_id)


# --- Adjectives ---

def list_adjectives() -> list[dict]:
    return _fetch_all("adjectives")


def add_adjective(data: dict) -> None:
    _insert("adjectives", data)


def update_adjective(row_id: int, data: dict) -> None:
    _update("adjectives", row_id, data)


def delete_adjective(row_id: int) -> None:
    _delete("adjectives", row_id)


def list_possessive_adjectives() -> list[dict]:
    return _fetch_all("possessive_adjectives")


def add_possessive_adjective(data: dict) -> None:
    _insert("possessive_adjectives", data)


def update_possessive_adjective(row_id: int, data: dict) -> None:
    _update("possessive_adjectives", row_id, data)


def delete_possessive_adjective(row_id: int) -> None:
    _delete("possessive_adjectives", row_id)


# --- Nouns ---

def list_nouns() -> list[dict]:
    return _fetch_all("nouns")


def add_noun(data: dict) -> None:
    _insert("nouns", data)


def update_noun(row_id: int, data: dict) -> None:
    _update("nouns", row_id, data)


def delete_noun(row_id: int) -> None:
    _delete("nouns", row_id)


# --- Pronouns ---

def list_subject_pronouns() -> list[dict]:
    return _fetch_all("subject_pronouns")


def list_object_pronouns() -> list[dict]:
    return _fetch_all("object_pronouns")


def list_possessive_pronouns() -> list[dict]:
    return _fetch_all("possessive_pronouns")


def add_subject_pronoun(data: dict) -> None:
    _insert("subject_pronouns", data)


def add_object_pronoun(data: dict) -> None:
    _insert("object_pronouns", data)


def add_possessive_pronoun(data: dict) -> None:
    _insert("possessive_pronouns", data)


def update_subject_pronoun(row_id: int, data: dict) -> None:
    _update("subject_pronouns", row_id, data)


def update_object_pronoun(row_id: int, data: dict) -> None:
    _update("object_pronouns", row_id, data)


def update_possessive_pronoun(row_id: int, data: dict) -> None:
    _update("possessive_pronouns", row_id, data)


def delete_subject_pronoun(row_id: int) -> None:
    _delete("subject_pronouns", row_id)


def delete_object_pronoun(row_id: int) -> None:
    _delete("object_pronouns", row_id)


def delete_possessive_pronoun(row_id: int) -> None:
    _delete("possessive_pronouns", row_id)


# --- Tense ---

def list_tense_examples() -> list[dict]:
    return _fetch_all("tense_examples")


def add_tense_example(data: dict) -> None:
    _insert("tense_examples", data)


def update_tense_example(row_id: int, data: dict) -> None:
    _update("tense_examples", row_id, data)


def delete_tense_example(row_id: int) -> None:
    _delete("tense_examples", row_id)


# --- Yes/No ---

def list_yesno_examples() -> list[dict]:
    return _fetch_all("yesno_examples")


def add_yesno_example(data: dict) -> None:
    _insert("yesno_examples", data)


def update_yesno_example(row_id: int, data: dict) -> None:
    _update("yesno_examples", row_id, data)


def delete_yesno_example(row_id: int) -> None:
    _delete("yesno_examples", row_id)
