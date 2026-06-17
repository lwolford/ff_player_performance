import pandas as pd
import streamlit as st

from html_elements import player_card_bust, preload_headshots
from utils import (
    WEEKLY_STATS_PATH, POSITIONS,
    apply_dst_logos, add_headshot_lg, build_preload_urls, filter_by_position, read_page_content,
)

st.title("⬇️ You Had One Job")
st.caption(read_page_content(__file__, "biggest_busts.md"))
st.markdown("---")

PARTICIPATED_COLS = ["attempts", "carries", "targets", "fg_att", "pat_att"]


@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    df = apply_dst_logos(df)
    df = add_headshot_lg(df)

    participated = (df[PARTICIPATED_COLS].fillna(0).sum(axis=1) > 0) | (df["position"] == "DST")
    df = df[participated]

    bust_idx = df.groupby("player_name")["fantasy_points_ppr"].idxmin()
    bust_games = df.loc[bust_idx].copy().rename(columns={"fantasy_points_ppr": "bust_score"})

    avg_without_bust = (
        df.drop(index=bust_idx)
        .groupby("player_name")["fantasy_points_ppr"]
        .mean()
        .rename("avg_without_bust")
    )

    game_counts = df.groupby("player_name")["fantasy_points_ppr"].count().rename("game_count")

    result = (
        bust_games
        .merge(avg_without_bust, on="player_name")
        .merge(game_counts, on="player_name")
    )
    result = result[result["game_count"] >= 10].copy()
    result["difference"] = result["avg_without_bust"] - result["bust_score"]
    result = result.sort_values("difference", ascending=False).reset_index(drop=True)

    return result, build_preload_urls(result)


bust_data, preload_urls = load_data()
preload_headshots(preload_urls)

selected = st.segmented_control("Position", POSITIONS, default="All", label_visibility="collapsed")
filtered = filter_by_position(bust_data, selected)
top4 = filtered.head(4)

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, top4.to_dict("records")), start=1):
    with col:
        player_card_bust(
            row["player_name"],
            row["position"],
            row["headshot_url_lg"],
            bust_score=row["bust_score"],
            avg_score=row["avg_without_bust"],
            week=int(row["week"]),
            rank=rank,
        )
