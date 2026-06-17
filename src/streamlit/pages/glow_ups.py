import pandas as pd
import streamlit as st

from html_elements import player_card, preload_headshots
from utils import (
    WEEKLY_STATS_PATH, POSITIONS,
    apply_dst_logos, add_headshot_lg, build_preload_urls, filter_by_position, read_page_content,
)

st.title("📈 Late Bloomers")
st.caption(read_page_content(__file__, "glow_ups.md"))
st.markdown("---")

FIRST_HALF = range(1, 9)
SECOND_HALF = range(9, 18)
MIN_GAMES_PER_HALF = 3


@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    df = apply_dst_logos(df)
    df = add_headshot_lg(df)

    first = (
        df[df["week"].isin(FIRST_HALF)]
        .groupby(["player_name", "position"])
        .agg(
            first_avg=("fantasy_points_ppr", "mean"),
            first_games=("fantasy_points_ppr", "count"),
            headshot_url_lg=("headshot_url_lg", "first"),
        )
        .reset_index()
    )
    second = (
        df[df["week"].isin(SECOND_HALF)]
        .groupby(["player_name", "position"])
        .agg(
            second_avg=("fantasy_points_ppr", "mean"),
            second_games=("fantasy_points_ppr", "count"),
        )
        .reset_index()
    )

    merged = first.merge(second, on=["player_name", "position"])
    merged = merged[
        (merged["first_games"] >= MIN_GAMES_PER_HALF) &
        (merged["second_games"] >= MIN_GAMES_PER_HALF) &
        (merged["first_games"] + merged["second_games"] >= 14)
    ].copy()
    merged["improvement"] = merged["second_avg"] - merged["first_avg"]
    merged = merged.sort_values("improvement", ascending=False).reset_index(drop=True)

    return merged, build_preload_urls(merged)


glow_data, preload_urls = load_data()
preload_headshots(preload_urls)

selected = st.segmented_control("Position", POSITIONS, default="All", label_visibility="collapsed")
filtered = filter_by_position(glow_data, selected)
top4 = filtered.head(4)

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, top4.to_dict("records")), start=1):
    with col:
        player_card(
            row["player_name"],
            row["position"],
            row["headshot_url_lg"],
            f"+{row['improvement']:.1f}",
            title=f"{row['first_avg']:.1f} → {row['second_avg']:.1f} PPR",
            rank=rank,
            label="pts/game gained",
        )
