import streamlit as st
from pathlib import Path

st.title("🏠 Fantasy Football EDA Project")
st.caption("A 2025 season breakdown — who dominated, who disappointed, and everything in between.")
st.markdown("---")

content = (Path(__file__).parent.parent / "content" / "home_page.md").read_text(encoding="utf-8")
st.markdown(content)
