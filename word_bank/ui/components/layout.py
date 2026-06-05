"""Componentes de layout da interface."""

import streamlit as st

from word_bank.auth import logout
from word_bank.repositories import word_bank as repo

PAGES = {
    "verbs": {"label": "Verbs", "icon": "⚡", "desc": "Verbos e formas do BE"},
    "adjectives": {"label": "Adjectives", "icon": "✨", "desc": "Adjetivos e possessivos"},
    "nouns": {"label": "Nouns", "icon": "📦", "desc": "Substantivos e pronomes"},
    "tense": {"label": "Tense Activity", "icon": "🕐", "desc": "Exemplos nos tempos verbais"},
    "yesno": {"label": "Yes/No", "icon": "💬", "desc": "Perguntas e respostas"},
}


def render_hero() -> None:
    st.markdown(
        """
        <div>
            <p class="hero-title">My English Word Bank</p>
            <p class="hero-subtitle">Seu caderno digital de vocabulário — registre, revise e pratique.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(icon: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-icon">{icon}</div>
            <div>
                <p class="section-title">{title}</p>
                <p class="section-desc">{description}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## 📚 Word Bank")
        st.caption("Navegação")

        page = st.radio(
            "Seção",
            options=list(PAGES.keys()),
            format_func=lambda k: f"{PAGES[k]['icon']}  {PAGES[k]['label']}",
            label_visibility="collapsed",
        )

        st.divider()
        st.markdown("**Resumo**")
        stats = repo.get_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Verbos", stats["verbs"] + stats["be_forms"])
            st.metric("Adjetivos", stats["adjectives"])
            st.metric("Substantivos", stats["nouns"])
        with col2:
            st.metric("Tempos", stats["tense_examples"])
            st.metric("Yes/No", stats["yesno_examples"])
            total = sum(stats.values())
            st.metric("Total", total)

        st.divider()
        user_name = st.session_state.get("user_name", "")
        st.caption(f"Conectado como **{user_name}**")
        if st.button("Sair", use_container_width=True):
            logout()

    return page


def card_start(title: str) -> None:
    st.markdown(f'<div class="card-panel"><h3>{title}</h3>', unsafe_allow_html=True)


def card_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)
