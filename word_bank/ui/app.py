"""Aplicação principal Streamlit."""

import streamlit as st

from word_bank.auth import login_form
from word_bank.config import DEFAULT_XLSX
from word_bank.db.connection import init_db
from word_bank.repositories import word_bank as repo
from word_bank.services.seed import seed_from_excel
from word_bank.ui.components.layout import render_hero, render_sidebar
from word_bank.ui.theme import apply_theme
from word_bank.ui.views import adjectives, nouns, tense, verbs, yesno

VIEWS = {
    "verbs": verbs.render,
    "adjectives": adjectives.render,
    "nouns": nouns.render,
    "tense": tense.render,
    "yesno": yesno.render,
}


def _bootstrap_data() -> None:
    if not repo.is_empty():
        return
    if DEFAULT_XLSX.exists():
        seed_from_excel(DEFAULT_XLSX)
        st.toast("Dados importados da planilha WORD BANK.xlsx", icon="📥")
        st.rerun()
    st.warning(
        "Banco vazio. Coloque **WORD BANK.xlsx** em `~/Downloads` "
        "ou adicione registros manualmente."
    )


def main() -> None:
    st.set_page_config(
        page_title="My English Word Bank",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_theme()
    init_db()

    if not login_form():
        st.stop()

    _bootstrap_data()

    page = render_sidebar()
    render_hero()
    VIEWS[page]()
