import pandas as pd
import streamlit as st

from html_elements import player_card, preload_headshots
from utils import (
    WEEKLY_STATS_PATH, POSITIONS,
    apply_dst_logos, add_headshot_lg, build_preload_urls, filter_by_position, read_page_content,
)

st.title("🔻 They Participated")
st.caption(read_page_content(__file__, "worst_players.md"))
st.markdown("---")


@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    df = apply_dst_logos(df)

    player_stats = df.groupby(["player_name", "position"]).agg(
        game_count=("fantasy_points_ppr", "count"),
        total_points=("fantasy_points_ppr", "sum"),
        headshot_url=("headshot_url", "first"),
    ).reset_index()

    player_stats = player_stats[player_stats["game_count"] >= 16]
    player_stats = player_stats.sort_values("total_points", ascending=True).reset_index(drop=True)
    player_stats = add_headshot_lg(player_stats)
    return player_stats, build_preload_urls(player_stats)


season_data, preload_urls = load_data()
preload_headshots(preload_urls)

selected = st.segmented_control("Position", POSITIONS, default="All", label_visibility="collapsed")
filtered = filter_by_position(season_data, selected)
bottom4 = filtered.head(4)

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, bottom4.to_dict("records")), start=1):
    with col:
        player_card(
            row["player_name"],
            row["position"],
            row["headshot_url_lg"],
            round(row["total_points"], 2),
            title="Season Total",
            rank=rank,
        )
