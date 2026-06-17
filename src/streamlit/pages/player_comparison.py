import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from html_elements import player_card_with_games
from utils import (
    WEEKLY_STATS_PATH, POSITION_COLORS,
    apply_dst_logos, add_headshot_lg, hex_to_rgba, read_page_content,
)

st.title("⚖️ Player Comparison")
st.caption(read_page_content(__file__, "player_comparison.md"))
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

sel_col1, sel_col2 = st.columns(2, gap="large")
with sel_col1:
    player1 = st.selectbox(
        "Player 1",
        player_names,
        index=player_names.index("Josh Allen") if "Josh Allen" in player_names else None,
        placeholder="Select first player...",
        label_visibility="collapsed",
        key="p1",
    )
with sel_col2:
    player2 = st.selectbox(
        "Player 2",
        player_names,
        index=player_names.index("Drake Maye") if "Drake Maye" in player_names else None,
        placeholder="Select second player...",
        label_visibility="collapsed",
        key="p2",
    )

if not player1 and not player2:
    st.stop()

st.markdown("---")

card_col1, card_col2 = st.columns(2, gap="large")
all_weeks = list(range(1, 18))
week_labels = [f"Wk {w}" for w in all_weeks]
fig = go.Figure()

# Player 1 extends left (direction=-1), Player 2 extends right (direction=1)
players = [(player1, card_col1, -1), (player2, card_col2, 1)]
colors_used = []

for player, col, direction in players:
    if not player:
        continue

    df = weekly_data[weekly_data["display_name"] == player].sort_values("week")
    pos = df["position"].iloc[0]
    color = POSITION_COLORS.get(pos, "#888888")

    if color in colors_used:
        color = hex_to_rgba(color, 0.55)
    colors_used.append(color)

    total = df["fantasy_points_ppr"].sum()
    avg = total / len(df)

    with col:
        player_card_with_games(
            player,
            pos,
            df["headshot_url_lg"].iloc[0],
            round(total, 2),
            games=len(df),
            title="Season Total",
            avg=round(avg, 2),
        )

    week_pts = df.set_index("week")["fantasy_points_ppr"].clip(lower=0)
    played_labels = [f"Wk {w}" for w in week_pts.index]

    fig.add_trace(go.Scatter(
        name=player,
        x=week_pts.values * direction,
        y=played_labels,
        mode="lines",
        fill="tozerox",
        line=dict(color=color, width=2, shape="spline", smoothing=0.8),
        fillcolor=hex_to_rgba(color, 0.25),
        customdata=week_pts.values,
        hovertemplate=f"{player}<br>%{{y}}<br>%{{customdata:.2f}} pts<extra></extra>",
    ))

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# Symmetric x-axis: use the larger of the two sides for both
all_abs = [abs(v) for trace in fig.data for v in trace.x if v is not None]
max_abs_data = max(all_abs, default=0)
max_abs_range = max_abs_data * 1.25

if max_abs_data > 0:
    step = 10
    ticks = list(range(0, int(max_abs_data * 1.1) + step, step))
    tickvals = sorted([-t for t in ticks if t > 0] + ticks)
    ticktext = [str(abs(t)) for t in tickvals]
else:
    tickvals, ticktext, max_abs_range = [], [], 50

right_labels = [
    dict(
        xref="paper", yref="y",
        x=1.02, y=label,
        text=label,
        xanchor="left", yanchor="middle",
        showarrow=False,
        font=dict(color="rgba(255,255,255,0.5)", size=12),
    )
    for label in week_labels
]

fig.update_layout(
    showlegend=False,
    plot_bgcolor="#1a1a2e",
    paper_bgcolor="#1a1a2e",
    font_color="#e8e8f0",
    xaxis=dict(
        title="PPR Points",
        range=[-max_abs_range, max_abs_range],
        tickvals=tickvals,
        ticktext=ticktext,
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=True,
        zerolinecolor="rgba(255,255,255,0.3)",
        zerolinewidth=2,
    ),
    yaxis=dict(
        title="",
        categoryarray=week_labels,
        categoryorder="array",
        autorange="reversed",
        gridcolor="rgba(255,255,255,0.05)",
    ),
    margin=dict(l=60, r=90, t=20, b=40),
    annotations=right_labels,
)
st.markdown(
    '<style>[data-testid="stPlotlyChart"]{border-radius:18px;overflow:hidden;border:1px solid #e0e0e0;}</style>',
    unsafe_allow_html=True,
)
st.plotly_chart(fig, width="stretch")
