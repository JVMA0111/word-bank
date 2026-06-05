"""Autenticação simples com bcrypt e st.secrets."""

import bcrypt
import streamlit as st


def _verify(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def login_form() -> bool:
    """Renderiza o formulário de login. Retorna True se autenticado."""
    if st.session_state.get("authenticated"):
        return True

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("## 📚 My English Word Bank")
        st.markdown("---")
        username = st.text_input("Usuário", key="login_username")
        password = st.text_input("Senha", type="password", key="login_password")

        if st.button("Entrar", use_container_width=True, type="primary"):
            users = st.secrets.get("users", {})
            if username in users and _verify(password, users[username]["password_hash"]):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_name = users[username]["name"]
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    return False


def logout() -> None:
    for key in ("authenticated", "username", "user_name"):
        st.session_state.pop(key, None)
    st.rerun()


def get_current_user() -> str:
    return st.session_state.get("username", "")
