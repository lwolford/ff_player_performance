import pandas as pd
import streamlit as st

from html_elements import player_card, preload_headshots
from utils import (
    WEEKLY_STATS_PATH, POSITIONS,
    apply_dst_logos, add_headshot_lg, build_preload_urls, filter_by_position, read_page_content,
)

st.title("🏈 Carrying the Load")
st.caption(read_page_content(__file__, "team_carriers.md"))
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    df = apply_dst_logos(df)

    player_team = df.groupby(["player_name", "team", "position"]).agg(
        player_team_points=("fantasy_points_ppr", "sum"),
        headshot_url=("headshot_url", "first"),
    ).reset_index()

    team_totals = player_team.groupby("team")["player_team_points"].sum().reset_index()
    team_totals.columns = ["team", "team_total"]

    merged = player_team.merge(team_totals, on="team")
    merged["share_pct"] = merged["player_team_points"] / merged["team_total"] * 100
    merged = merged.reset_index(drop=True)
    merged = add_headshot_lg(merged)
    return merged, build_preload_urls(merged, "share_pct")

base_data, preload_urls = load_data()
preload_headshots(preload_urls)

selected = st.segmented_control("Position", POSITIONS, default="All", label_visibility="collapsed")
filtered = filter_by_position(base_data, selected)
top4 = filtered.nlargest(4, "share_pct")

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, top4.to_dict("records")), start=1):
    with col:
        player_card(
            row["player_name"],
            row["position"],
            row["headshot_url_lg"],
            f"{round(row['share_pct'], 1)}%",
            title=row["team"],
            rank=rank,
            label="Team Point Share",
        )
