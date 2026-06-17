import pandas as pd
import streamlit as st

from html_elements import player_card_boom, preload_headshots
from utils import (
    WEEKLY_STATS_PATH, POSITIONS,
    apply_dst_logos, add_headshot_lg, build_preload_urls, filter_by_position, read_page_content,
)

st.title("💥 Lightning in a Bottle")
st.caption(read_page_content(__file__, "unexpected_booms.md"))
st.markdown("---")


@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    df = apply_dst_logos(df)
    df = add_headshot_lg(df)

    boom_idx = df.groupby("player_name")["fantasy_points_ppr"].idxmax()
    boom_games = df.loc[boom_idx].copy().rename(columns={"fantasy_points_ppr": "boom_score"})

    avg_without_boom = (
        df.drop(index=boom_idx)
        .groupby("player_name")["fantasy_points_ppr"]
        .mean()
        .rename("avg_without_boom")
    )

    game_counts = df.groupby("player_name")["fantasy_points_ppr"].count().rename("game_count")

    result = (
        boom_games
        .merge(avg_without_boom, on="player_name")
        .merge(game_counts, on="player_name")
    )
    result = result[(result["game_count"] >= 10) & (result["avg_without_boom"] < 10)].copy()
    result["difference"] = result["boom_score"] - result["avg_without_boom"]
    result = result.sort_values("difference", ascending=False).reset_index(drop=True)

    return result, build_preload_urls(result)


boom_data, preload_urls = load_data()
preload_headshots(preload_urls)

selected = st.segmented_control("Position", POSITIONS, default="All", label_visibility="collapsed")
filtered = filter_by_position(boom_data, selected)
top4 = filtered.head(4)

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, top4.to_dict("records")), start=1):
    with col:
        player_card_boom(
            row["player_name"],
            row["position"],
            row["headshot_url_lg"],
            boom_score=row["boom_score"],
            avg_score=row["avg_without_boom"],
            week=int(row["week"]),
            rank=rank,
        )
