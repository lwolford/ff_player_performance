import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from html_elements import player_banner
from utils import (
    WEEKLY_STATS_PATH, POSITION_COLORS, DST_LOGO_URLS,
    apply_dst_logos, add_headshot_lg, hex_to_rgba, read_page_content,
)

st.title("🔍 Player Lookup")
st.caption(read_page_content(__file__, "player_lookup.md"))
st.markdown("---")


@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    df = apply_dst_logos(df)
    df = add_headshot_lg(df)
    df["display_name"] = df["player_display_name"].fillna(df["player_name"])
    return df


weekly_data = load_data()
player_names = sorted(weekly_data["display_name"].unique())

_default = player_names.index("A.J. Brown") if "A.J. Brown" in player_names else None
selected_player = st.selectbox(
    "Player",
    player_names,
    index=_default,
    placeholder="Type a player name...",
    label_visibility="collapsed",
)

if not selected_player:
    st.stop()

player_df = weekly_data[weekly_data["display_name"] == selected_player].sort_values("week")
pos = player_df["position"].iloc[0]
color = POSITION_COLORS.get(pos, "#888888")

total_pts = player_df["fantasy_points_ppr"].sum()
avg_pts = player_df["fantasy_points_ppr"].mean()
games = len(player_df)

player_banner(
    selected_player,
    pos,
    player_df["headshot_url_lg"].iloc[0],
    total=total_pts,
    avg=avg_pts,
    games=games,
)

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

all_weeks = list(range(1, 18))
week_pts = (
    player_df.set_index("week")["fantasy_points_ppr"]
    .reindex(all_weeks, fill_value=None)
)

bar_colors = [
    color if (v is not None and not pd.isna(v) and v >= avg_pts)
    else hex_to_rgba(color, 0.35)
    for v in week_pts.values
]
text_vals = [f"{v:.1f}" if (v is not None and not pd.isna(v)) else "" for v in week_pts.values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=all_weeks,
    y=week_pts.values,
    marker_color=bar_colors,
    text=text_vals,
    textposition="outside",
    textfont=dict(size=10, color="rgba(255,255,255,0.6)"),
    cliponaxis=False,
    hovertemplate="Week %{x}<br>%{y:.2f} pts<extra></extra>",
))

fig.add_hline(
    y=avg_pts,
    line_dash="dash",
    line_color="rgba(255,255,255,0.25)",
    annotation_text=f"Avg: {avg_pts:.1f}",
    annotation_position="top left",
    annotation_font_color="rgba(255,255,255,0.5)",
    annotation_font_size=11,
)

fig.update_layout(
    plot_bgcolor="#1a1a2e",
    paper_bgcolor="#1a1a2e",
    font_color="#e8e8f0",
    xaxis=dict(
        title="Week",
        tickmode="linear",
        dtick=1,
        tickvals=all_weeks,
        gridcolor="rgba(255,255,255,0.05)",
    ),
    yaxis=dict(
        title="PPR Points",
        gridcolor="rgba(255,255,255,0.05)",
        rangemode="tozero",
    ),
    margin=dict(l=40, r=20, t=32, b=40),
    showlegend=False,
    height=360,
)

st.markdown(
    '<style>[data-testid="stPlotlyChart"]{border-radius:18px;overflow:hidden;border:1px solid #e0e0e0;}</style>',
    unsafe_allow_html=True,
)
st.plotly_chart(fig, width="stretch")
