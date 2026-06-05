"""Autenticação com bcrypt e persistência no banco (tabela users)."""

import bcrypt
import streamlit as st

from word_bank.db.connection import get_connection


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except ValueError:
        return False


def _get_user(username: str) -> dict | None:
    with get_connection() as conn:
        return conn.execute(
            "SELECT username, name, password_hash FROM users WHERE username = %s",
            (username,),
        ).fetchone()


def _create_user(username: str, name: str, password: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO users (username, name, password_hash) VALUES (%s, %s, %s)",
            (username, name, _hash(password)),
        )


def _login(username: str, password: str) -> None:
    username = username.strip().lower()
    user = _get_user(username)
    if user and _verify(password, user["password_hash"]):
        st.session_state.authenticated = True
        st.session_state.username = user["username"]
        st.session_state.user_name = user["name"]
        st.rerun()
    else:
        st.error("Usuário ou senha incorretos.")


def _register(username: str, name: str, password: str, confirm: str) -> None:
    username = username.strip().lower()
    name = name.strip()

    if not username or not name or not password:
        st.error("Preencha todos os campos.")
        return
    if len(password) < 6:
        st.error("A senha deve ter pelo menos 6 caracteres.")
        return
    if password != confirm:
        st.error("As senhas não coincidem.")
        return
    if _get_user(username):
        st.error("Esse usuário já existe. Escolha outro.")
        return

    _create_user(username, name, password)
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.user_name = name
    st.success("Conta criada com sucesso!")
    st.rerun()


def login_form() -> bool:
    """Renderiza login/cadastro. Retorna True se autenticado."""
    if st.session_state.get("authenticated"):
        return True

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("## 📚 My English Word Bank")
        st.markdown("---")

        tab_login, tab_signup = st.tabs(["Entrar", "Criar conta"])

        with tab_login:
            username = st.text_input("Usuário", key="login_username")
            password = st.text_input("Senha", type="password", key="login_password")
            if st.button("Entrar", use_container_width=True, type="primary"):
                _login(username, password)

        with tab_signup:
            new_name = st.text_input("Nome", key="signup_name")
            new_username = st.text_input("Usuário", key="signup_username")
            new_password = st.text_input("Senha", type="password", key="signup_password")
            confirm = st.text_input(
                "Confirmar senha", type="password", key="signup_confirm"
            )
            if st.button("Criar conta", use_container_width=True, type="primary"):
                _register(new_username, new_name, new_password, confirm)

    return False


def logout() -> None:
    for key in ("authenticated", "username", "user_name"):
        st.session_state.pop(key, None)
    st.rerun()


def get_current_user() -> str:
    return st.session_state.get("username", "")
