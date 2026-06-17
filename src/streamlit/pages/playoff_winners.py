import pandas as pd
import streamlit as st

from html_elements import player_card, preload_headshots
from utils import (
    WEEKLY_STATS_PATH, POSITIONS,
    apply_dst_logos, add_headshot_lg, build_preload_urls, filter_by_position, read_page_content,
    SLIDER_THUMB_CSS,
)

st.title("🥇 When It Matters Most")
st.caption(read_page_content(__file__, "playoff_winners.md"))
st.markdown("---")

st.markdown(SLIDER_THUMB_CSS, unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    df = apply_dst_logos(df)
    df = df[df["week"].isin([15, 16, 17])][["player_name", "headshot_url", "position", "fantasy_points_ppr"]]
    df = df.groupby(by=["player_name", "headshot_url", "position"]).agg(
        row_counts=("fantasy_points_ppr", "count"),
        points_ppr_avg=("fantasy_points_ppr", "mean"),
        points_ppr_std=("fantasy_points_ppr", "std"),
    ).reset_index()
    df = df[df["row_counts"] == 3]
    df = add_headshot_lg(df)
    return df, build_preload_urls(df, "points_ppr_avg")

base_data, preload_urls = load_data()
preload_headshots(preload_urls)

col_seg, col_label, col_slider = st.columns([3, 1.3, 1.3], vertical_alignment="center")
with col_seg:
    selected = st.segmented_control("Position", POSITIONS, default="All", label_visibility="collapsed")
with col_label:
    st.markdown(
        '<p style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.45);letter-spacing:0.06em;text-transform:uppercase;white-space:nowrap;text-align:right;margin:0;padding:0;position:relative;top:-8px;">Consistency Penalty</p>',
        unsafe_allow_html=True,
    )
with col_slider:
    st.slider(
        "Consistency Penalty",
        min_value=0.0, max_value=1.0, value=0.5, step=0.05, format="%.2f",
        key="playoff_penalty",
        label_visibility="collapsed",
        help="0 = pure average · 1 = heavily penalizes inconsistency",
    )

penalty = st.session_state.get("playoff_penalty", 0.5)
scored = base_data.assign(
    playoff_winner_score=base_data["points_ppr_avg"] - penalty * base_data["points_ppr_std"]
)

filtered = filter_by_position(scored, selected)
top4 = filtered.nlargest(4, "playoff_winner_score")

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, top4.to_dict("records")), start=1):
    with col:
        player_card(
            row["player_name"],
            row["position"],
            row["headshot_url_lg"],
            round(row["playoff_winner_score"], 2),
            title="Weeks 15–17",
            rank=rank,
            label="Playoff Score",
        )
