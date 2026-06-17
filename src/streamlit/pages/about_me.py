import streamlit as st
from pathlib import Path

st.title("👤 About Me")
st.markdown("---")

st.markdown((Path(__file__).parent.parent / "content" / "about_me.md").read_text(encoding="utf-8"))
