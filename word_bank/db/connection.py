import psycopg2
import psycopg2.extras
import streamlit as st

from word_bank.db.schema import SCHEMA


class _Cursor:
    """Wrapper fino sobre psycopg2 cursor para manter API compatível com sqlite3."""

    def __init__(self, cur):
        self._cur = cur

    def execute(self, sql, params=None):
        # psycopg2 usa %s; aceita tanto ? quanto %s para compatibilidade
        if params is not None:
            self._cur.execute(sql, params)
        else:
            self._cur.execute(sql)
        return self

    def fetchall(self):
        return [dict(row) for row in self._cur.fetchall()]

    def fetchone(self):
        row = self._cur.fetchone()
        return dict(row) if row else None


class _Connection:
    def __init__(self):
        self._conn = psycopg2.connect(
            st.secrets["DATABASE_URL"],
            cursor_factory=psycopg2.extras.RealDictCursor,
        )

    def execute(self, sql, params=None):
        cur = _Cursor(self._conn.cursor())
        return cur.execute(sql, params)

    def executescript(self, sql):
        cur = self._conn.cursor()
        cur.execute(sql)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, *_):
        if exc_type:
            self._conn.rollback()
        else:
            self._conn.commit()
        self._conn.close()


def get_connection() -> _Connection:
    return _Connection()


@st.cache_resource(show_spinner=False)
def init_db() -> None:
    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
    try:
        cur = conn.cursor()
        cur.execute(SCHEMA)
        conn.commit()
    finally:
        conn.close()
