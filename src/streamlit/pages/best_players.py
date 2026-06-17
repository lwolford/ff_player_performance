import pandas as pd
import streamlit as st

from html_elements import player_card, preload_headshots
from utils import (
    SEASON_TOTALS_PATH, POSITIONS,
    apply_dst_logos, add_headshot_lg, build_preload_urls, filter_by_position, read_page_content,
)

st.title("⭐ PPR Royalty")
st.caption(read_page_content(__file__, "best_players.md"))
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv(SEASON_TOTALS_PATH)
    df = apply_dst_logos(df)
    df = add_headshot_lg(df)
    return df, build_preload_urls(df, "total_fantasy_ppr")

season_df, preload_urls = load_data()
preload_headshots(preload_urls)

selected = st.segmented_control("Position", POSITIONS, default="All", label_visibility="collapsed")
filtered = filter_by_position(season_df, selected)
top4 = filtered.nlargest(4, "total_fantasy_ppr")

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, top4.to_dict("records")), start=1):
    with col:
        player_card(
            row["player_name"],
            row["position"],
            row["headshot_url_lg"],
            round(row["total_fantasy_ppr"], 2),
            title="Season Total",
            rank=rank,
        )
