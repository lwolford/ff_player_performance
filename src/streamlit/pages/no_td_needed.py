import pandas as pd
import streamlit as st

from html_elements import player_card, preload_headshots
from utils import (
    WEEKLY_STATS_PATH, POSITIONS,
    apply_dst_logos, add_headshot_lg, build_preload_urls, filter_by_position, read_page_content,
)

st.title("🚫 We Need TDs?")
st.caption(read_page_content(__file__, "no_td_needed.md"))
st.markdown("---")

TD_COLS = [
    "passing_tds",
    "rushing_tds",
    "receiving_tds",
    "special_teams_tds",
    "def_tds",
    "fumble_recovery_tds",
]

@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    df = apply_dst_logos(df)
    df = add_headshot_lg(df[df[TD_COLS].fillna(0).sum(axis=1) == 0])
    return df, build_preload_urls(df, "fantasy_points_ppr")

weekly_data, preload_urls = load_data()
preload_headshots(preload_urls)

selected = st.segmented_control("Position", POSITIONS, default="All", label_visibility="collapsed")
filtered = filter_by_position(weekly_data, selected)
top4 = filtered.nlargest(4, "fantasy_points_ppr")

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, top4.to_dict("records")), start=1):
    with col:
        player_card(
            row["player_name"],
            row["position"],
            row["headshot_url_lg"],
            round(row["fantasy_points_ppr"], 2),
            title=f"Week {int(row['week'])}",
            rank=rank,
        )
