import streamlit as st
import pandas as pd

from html_elements import player_card, preload_headshots
from utils import set_headshot_resolution, WEEKLY_STATS_PATH, DST_LOGO_URLS, read_page_content

SKILL_POSITIONS = ["VS ALL", "VS QB", "VS RB", "VS WR", "VS TE", "VS K"]

st.title("🛡️ Position Proof")
st.caption(read_page_content(__file__, "defense_vs_position.md"))
st.markdown("---")


@st.cache_data
def load_data():
    df = pd.read_csv(WEEKLY_STATS_PATH)
    dst_names = (
        df[df["position"] == "DST"][["team", "player_name"]]
        .drop_duplicates("team")
        .set_index("team")["player_name"]
        .to_dict()
    )
    return df, dst_names


weekly_data, dst_names = load_data()

selected = st.segmented_control("Position", SKILL_POSITIONS, default="VS ALL", label_visibility="collapsed")
if not selected:
    selected = "VS ALL"

pos = selected.replace("VS ", "")

if pos == "ALL":
    participated = (
        (weekly_data["attempts"].fillna(0) > 0) |
        ((weekly_data["carries"].fillna(0) + weekly_data["targets"].fillna(0)) > 0) |
        ((weekly_data["fg_att"].fillna(0) + weekly_data["pat_att"].fillna(0)) > 0)
    )
    skill_df = weekly_data[weekly_data["position"].isin(["QB", "RB", "WR", "TE", "K"]) & participated].copy()
elif pos == "QB":
    participated = weekly_data["attempts"].fillna(0) > 0
    skill_df = weekly_data[(weekly_data["position"] == pos) & participated].copy()
elif pos == "K":
    participated = (weekly_data["fg_att"].fillna(0) + weekly_data["pat_att"].fillna(0)) > 0
    skill_df = weekly_data[(weekly_data["position"] == pos) & participated].copy()
else:
    participated = (weekly_data["carries"].fillna(0) + weekly_data["targets"].fillna(0)) > 0
    skill_df = weekly_data[(weekly_data["position"] == pos) & participated].copy()

agg = (
    skill_df.groupby("opponent_team")["fantasy_points_ppr"]
    .agg(total_allowed="sum", games="count")
    .reset_index()
)

agg = agg[agg["games"] >= 5]
top4 = agg.nsmallest(4, "total_allowed").reset_index(drop=True)

top4["display_name"] = top4["opponent_team"].map(dst_names).fillna(top4["opponent_team"])
top4["logo_url"] = top4["opponent_team"].map(DST_LOGO_URLS).fillna("")
top4["logo_url_lg"] = top4["logo_url"].apply(lambda u: set_headshot_resolution(u, 512))

preload_headshots(top4["logo_url_lg"].tolist())

cols = st.columns(4, gap="small")
for rank, (col, row) in enumerate(zip(cols, top4.to_dict("records")), start=1):
    with col:
        player_card(
            row["display_name"],
            "DST",
            row["logo_url_lg"],
            round(row["total_allowed"], 2),
            title="All Positions" if pos == "ALL" else f"{int(row['games'])} {pos}s Faced",
            rank=rank,
            label="Total PPR Allowed",
        )
