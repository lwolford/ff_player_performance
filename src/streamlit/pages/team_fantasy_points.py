import streamlit as st
import pandas as pd

from utils import WEEKLY_STATS_PATH, POSITION_COLORS, DST_LOGO_URLS, read_page_content

st.title("🏟️ Team Scores")
st.caption(read_page_content(__file__, "team_fantasy_points.md"))
st.markdown("---")

NFL_DIVISIONS = {
    "AFC": {
        "AFC East":  ["BUF", "MIA", "NE",  "NYJ"],
        "AFC North": ["BAL", "CIN", "CLE", "PIT"],
        "AFC South": ["HOU", "IND", "JAX", "TEN"],
        "AFC West":  ["DEN", "KC",  "LAC", "LV"],
    },
    "NFC": {
        "NFC East":  ["DAL", "NYG", "PHI", "WAS"],
        "NFC North": ["CHI", "DET", "GB",  "MIN"],
        "NFC South": ["ATL", "CAR", "NO",  "TB"],
        "NFC West":  ["ARI", "LA",  "SEA", "SF"],
    },
}

POSITIONS_ORDER = ["QB", "RB", "WR", "TE", "K", "DST"]


@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    # Weekly `team` column means traded players are credited to the right team each week.
    team_pos = (
        df.groupby(["team", "position"])["fantasy_points_ppr"]
        .sum()
        .reset_index()
        .rename(columns={"fantasy_points_ppr": "points"})
    )
    team_totals = team_pos.groupby("team")["points"].sum().rename("total_points")
    return team_pos, team_totals


team_pos_df, team_totals = load_data()

pos_pivot = (
    team_pos_df.pivot_table(index="team", columns="position", values="points", aggfunc="sum")
    .reindex(columns=POSITIONS_ORDER)
    .fillna(0)
)


def _stacked_bar(team: str, height: int = 10, margin_top: int = 8) -> str:
    row = pos_pivot.loc[team] if team in pos_pivot.index else pd.Series(dtype=float)
    total = row.sum()
    if total == 0:
        return ""
    segments = []
    for pos in POSITIONS_ORDER:
        pts = row.get(pos, 0)
        if pts <= 0:
            continue
        pct = pts / total * 100
        color = POSITION_COLORS.get(pos, "#888")
        label = f"{pos}: {pts:.1f} pts ({pct:.1f}%)"
        segments.append(
            f'<div style="width:{pct:.2f}%;background:{color};flex-shrink:0;"'
            f' title="{label}"></div>'
        )
    return (
        f'<div style="width:100%;height:{height}px;border-radius:5px;overflow:hidden;'
        f'background:#2a2a2a;margin-top:{margin_top}px;display:flex;">'
        + "".join(segments)
        + "</div>"
    )


def _team_card(team: str) -> str:
    total = team_totals.get(team, 0)
    logo = DST_LOGO_URLS.get(team, "")
    logo_html = (
        f'<img src="{logo}" style="width:44px;height:44px;object-fit:contain;margin-bottom:6px;">'
        if logo else ""
    )
    bar = _stacked_bar(team)
    return (
        '<div style="text-align:center;padding:14px 8px 12px;border-radius:10px;'
        'background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);">'
        f"{logo_html}"
        f'<div style="font-size:11px;font-weight:700;letter-spacing:0.05em;'
        f'color:rgba(255,255,255,0.55);margin-bottom:2px;">{team}</div>'
        f'<div style="font-size:22px;font-weight:800;color:white;line-height:1.1;">'
        f'{total:,.1f}</div>'
        f'<div style="font-size:10px;color:rgba(255,255,255,0.35);margin-bottom:2px;">PPR pts</div>'
        f"{bar}"
        "</div>"
    )


def _legend_html() -> str:
    items = []
    for pos in POSITIONS_ORDER:
        color = POSITION_COLORS[pos]
        items.append(
            f'<span style="display:inline-flex;align-items:center;margin-right:14px;">'
            f'<span style="width:10px;height:10px;border-radius:3px;background:{color};'
            f'display:inline-block;margin-right:5px;"></span>'
            f'<span style="font-size:12px;color:rgba(255,255,255,0.6);">{pos}</span>'
            f"</span>"
        )
    return (
        '<div style="display:flex;flex-wrap:wrap;align-items:center;'
        'margin-bottom:20px;padding:10px 14px;border-radius:8px;'
        'background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);">'
        + "".join(items)
        + "</div>"
    )


view = st.segmented_control("View", ["Division", "Ranked"], default="Division", label_visibility="collapsed")
st.markdown(_legend_html(), unsafe_allow_html=True)

if view == "Ranked":
    ranked = team_totals.sort_values(ascending=False).reset_index()
    ranked.columns = ["team", "total_points"]
    rows_html = []
    for rank, row in enumerate(ranked.to_dict("records"), start=1):
        team = row["team"]
        total = row["total_points"]
        logo = DST_LOGO_URLS.get(team, "")
        logo_html = f'<img src="{logo}" style="width:36px;height:36px;object-fit:contain;margin:0 14px 0 8px;">' if logo else '<div style="width:36px;margin:0 14px 0 8px;"></div>'
        bar = _stacked_bar(team, height=24, margin_top=0)
        rows_html.append(
            '<div style="display:flex;align-items:center;padding:10px 14px;border-radius:8px;'
            'background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);margin-bottom:6px;">'
            f'<div style="font-size:14px;font-weight:700;color:rgba(255,255,255,0.3);width:28px;text-align:center;">#{rank}</div>'
            f'{logo_html}'
            f'<div style="font-size:13px;font-weight:700;color:white;width:44px;">{team}</div>'
            f'<div style="font-size:18px;font-weight:800;color:white;width:76px;text-align:right;">{total:,.1f}</div>'
            f'<div style="font-size:10px;color:rgba(255,255,255,0.4);width:28px;text-align:center;margin-right:8px;">pts</div>'
            f'<div style="flex:1;">{bar}</div>'
            '</div>'
        )
    st.markdown("".join(rows_html), unsafe_allow_html=True)

else:
    for conf, divisions in NFL_DIVISIONS.items():
        st.markdown(f"## {conf}")
        for div_name, teams in divisions.items():
            st.markdown(f"#### {div_name}")
            cols = st.columns(4, gap="small")
            for col, team in zip(cols, teams):
                with col:
                    st.markdown(_team_card(team), unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
        st.markdown("---")
