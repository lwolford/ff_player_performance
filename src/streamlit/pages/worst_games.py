import pandas as pd
import streamlit as st

from html_elements import player_card, preload_headshots
from utils import (
    WEEKLY_STATS_PATH, POSITIONS,
    apply_dst_logos, add_headshot_lg, build_preload_urls, read_page_content,
)

st.title("🥶 Walk of Shame")
st.caption(read_page_content(__file__, "worst_games.md"))
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    df = apply_dst_logos(df)
    df = add_headshot_lg(df)
    return df, build_preload_urls(df, "fantasy_points_ppr", largest=False)

weekly_data, preload_urls = load_data()
preload_headshots(preload_urls)

col_seg, col_toggle = st.columns([4, 1], vertical_alignment="center")
with col_seg:
    selected = st.segmented_control("Position", POSITIONS, default="All", label_visibility="collapsed")
with col_toggle:
    include_dst = st.toggle("Include DST", value=False, disabled=selected != "All" and selected is not None)

if selected and selected != "All":
    filtered = weekly_data[weekly_data["position"] == selected]
else:
    filtered = weekly_data if include_dst else weekly_data[weekly_data["position"] != "DST"]

participated = (
    filtered[["attempts", "carries", "targets", "fg_att", "pat_att"]]
    .fillna(0)
    .sum(axis=1) > 0
) | (filtered["position"] == "DST")
bottom4 = filtered[participated].nsmallest(4, "fantasy_points_ppr")

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, bottom4.to_dict("records")), start=1):
    with col:
        player_card(
            row["player_name"],
            row["position"],
            row["headshot_url_lg"],
            round(row["fantasy_points_ppr"], 2),
            title=f"Week {int(row['week'])}",
            rank=rank,
        )
