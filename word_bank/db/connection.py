import psycopg2
import psycopg2.extras
import psycopg2.pool
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


@st.cache_resource(show_spinner=False)
def _get_pool() -> psycopg2.pool.ThreadedConnectionPool:
    """Pool de conexões reaproveitado entre execuções (evita reconectar a cada query)."""
    return psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=5,
        dsn=st.secrets["DATABASE_URL"],
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


class _Connection:
    def __init__(self):
        self._pool = _get_pool()
        self._conn = self._borrow()

    def _borrow(self):
        """Pega uma conexão do pool, descartando conexões mortas."""
        conn = self._pool.getconn()
        try:
            # Valida a conexão; se estiver morta, recria.
            conn.cursor().execute("SELECT 1")
            conn.rollback()
        except psycopg2.Error:
            self._pool.putconn(conn, close=True)
            conn = self._pool.getconn()
        return conn

    def execute(self, sql, params=None):
        cur = _Cursor(self._conn.cursor())
        return cur.execute(sql, params)

    def executescript(self, sql):
        cur = self._conn.cursor()
        cur.execute(sql)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, *_):
        try:
            if exc_type:
                self._conn.rollback()
            else:
                self._conn.commit()
        finally:
            # Devolve a conexão ao pool em vez de fechá-la.
            self._pool.putconn(self._conn)


def get_connection() -> _Connection:
    return _Connection()


@st.cache_resource(show_spinner=False)
def init_db() -> None:
    pool = _get_pool()
    conn = pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute(SCHEMA)
        conn.commit()
    finally:
        pool.putconn(conn)
