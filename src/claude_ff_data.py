"""
Fantasy Football Player Performance EDA — Data Fetching (Updated)
=================================================================
Source  : 2025_ff_data.csv  (nfl_data_py weekly player stats)
Covers  : QB / RB / WR / TE  →  existing fantasy_points_ppr column
          K  (Kicker)         →  calculated from fg/pat range buckets
          DST (Team Defense)  →  aggregated from individual defenders
                                 + blocked kicks + points-allowed tiers

Default scoring rules used
──────────────────────────
Kicker
  PAT made          +1 pt
  FG  0–39 yds      +3 pts
  FG 40–49 yds      +4 pts
  FG 50–59 yds      +5 pts
  FG 60+  yds       +6 pts
  Missed FG <40 yds  -1 pt  (misses ≥40 yds = no penalty)

DST
  Sack              +1 pt
  Interception      +2 pts
  Fumble recovery   +2 pts   (fumble_recovery_opp for defensive players)
  Safety            +2 pts
  Def / ST TD       +6 pts
  Blocked kick      +2 pts   (FG or PAT)
  Points allowed
    0 pts scored    +10 pts
    1–6 pts         +7 pts
    7–13 pts        +4 pts
    14–20 pts       +1 pt
    21–27 pts        0 pts
    28–34 pts       -1 pt
    35+ pts         -4 pts

Usage
──────────────────────────
  pip install pandas numpy
  python ff_data_fetch.py
"""

import pandas as pd
import numpy as np

# ── 0. Load & filter to regular season ───────────────────────────────────────
print("Loading 2025_ff_data.csv...")
raw = pd.read_csv(r"C:\Users\13012\OneDrive\Documents\vs-code-projects\ff_player_performance\data\2025_ff_data.csv", low_memory=False)
df  = raw[raw["week"] < 18].copy()
print(f"  Rows (regular season): {len(df):,}  |  Columns: {df.shape[1]}")


# ════════════════════════════════════════════════════════════════════════════
# SECTION 1 — SKILL POSITIONS  (QB / RB / WR / TE)
#   fantasy_points_ppr is already populated by nfl_data_py — no changes needed
# ════════════════════════════════════════════════════════════════════════════
SKILL_POSITIONS = ["QB", "RB", "WR", "TE"]

# Keep every original column — nothing stripped
skill_weekly = df[df["position"].isin(SKILL_POSITIONS)].copy().reset_index(drop=True)
print(f"\n[Skill] Weekly rows : {len(skill_weekly):,}")


# ════════════════════════════════════════════════════════════════════════════
# SECTION 2 — KICKERS
#   fantasy_points / fantasy_points_ppr = FG/PAT points
#                                        + any incidental skill-stat points
#                                          (fake FG/punt rushes, passes, etc.)
# ════════════════════════════════════════════════════════════════════════════
kickers = df[df["position"] == "K"].copy()

# ── FG + PAT points ───────────────────────────────────────────────────────────
fg_pat_pts = (
    kickers["fg_made_0_19"]  * 3 +
    kickers["fg_made_20_29"] * 3 +
    kickers["fg_made_30_39"] * 3 +
    kickers["fg_made_40_49"] * 4 +
    kickers["fg_made_50_59"] * 5 +
    kickers["fg_made_60_"]   * 5 +
    kickers["pat_made"]      * 1 +
    # Penalty for short misses only (inside 40 yds)
    (kickers["fg_missed_0_19"] + kickers["fg_missed_20_29"] +
     kickers["fg_missed_30_39"]) * -1
).fillna(0)

# ── Extra skill-stat points (fake FG/punt plays, etc.) ───────────────────────
# Standard (non-PPR) component
skill_std = (
    kickers["rushing_yards"].fillna(0)            * 0.1  +
    kickers["rushing_tds"].fillna(0)              * 6    +
    kickers["rushing_2pt_conversions"].fillna(0)  * 2    +
    kickers["receiving_yards"].fillna(0)          * 0.1  +
    kickers["receiving_tds"].fillna(0)            * 6    +
    kickers["receiving_2pt_conversions"].fillna(0)* 2    +
    kickers["passing_yards"].fillna(0)            * 0.04 +
    kickers["passing_tds"].fillna(0)              * 4    +
    kickers["passing_interceptions"].fillna(0)    * -2   +
    kickers["passing_2pt_conversions"].fillna(0)  * 2    +
    (kickers["sack_fumbles_lost"].fillna(0)  +
     kickers["rushing_fumbles_lost"].fillna(0) +
     kickers["receiving_fumbles_lost"].fillna(0)) * -2
)
# PPR adds 1 pt per reception
skill_ppr = skill_std + kickers["receptions"].fillna(0) * 1

kickers["fantasy_points"]     = fg_pat_pts + skill_std
kickers["fantasy_points_ppr"] = fg_pat_pts + skill_ppr

# Keep every original column — nothing stripped
kicker_weekly = kickers.copy().reset_index(drop=True)
print(f"[Kicker] Weekly rows: {len(kicker_weekly):,}")


# ════════════════════════════════════════════════════════════════════════════
# SECTION 3 — DST (Team Defense / Special Teams)
#
#   Step 3a : Aggregate individual defensive player stats → team level
#   Step 3b : Add blocked kicks (inferred from opponent kicker rows)
#   Step 3c : Points allowed joined from games_2025.csv
#   Step 3d : Apply DST scoring tiers
# ════════════════════════════════════════════════════════════════════════════

# ── 3a. Aggregate defensive player stats per team per week ───────────────────
# Defensive position groups: DB (CBs, Safeties), DL (DEs, DTs), LB
DEF_POSITION_GROUPS = ["DB", "DL", "LB"]
defenders = df[df["position_group"].isin(DEF_POSITION_GROUPS)]

dst_agg = (
    defenders
    .groupby(["team", "week"], as_index=False)
    .agg(
        sacks          = ("def_sacks",            "sum"),
        interceptions  = ("def_interceptions",    "sum"),
        safeties       = ("def_safeties",         "sum"),
        # def_tds covers pick-6s; fumble_recovery_tds covers fumble-return TDs
        # (these are separate columns and must both be aggregated)
        def_tds        = ("def_tds",              "sum"),
        fum_rec_tds    = ("fumble_recovery_tds",  "sum"),
    )
    .reset_index(drop=True)
)

# fumble_recovery_opp is aggregated across ALL players — any position can
# recover an opponent's fumble on special teams (e.g. an RB on a kickoff unit).
all_fum_rec = (
    df.groupby(["team", "week"], as_index=False)
    .agg(fum_recoveries = ("fumble_recovery_opp", "sum"))
)
dst_agg = dst_agg.merge(all_fum_rec, on=["team", "week"], how="left")
dst_agg["fum_recoveries"] = dst_agg["fum_recoveries"].fillna(0)

# Also add special-teams TDs from ALL players on the team
# (return TDs by WR/RB on ST units count for the DST)
st_tds = (
    df.groupby(["team", "week"], as_index=False)
    .agg(st_tds = ("special_teams_tds", "sum"))
)
dst_agg = dst_agg.merge(st_tds, on=["team", "week"], how="left")
dst_agg["st_tds"] = dst_agg["st_tds"].fillna(0)

# Total touchdowns for DST: pick-6s + fumble-return TDs + ST return TDs
dst_agg["total_dst_tds"] = dst_agg["def_tds"] + dst_agg["fum_rec_tds"] + dst_agg["st_tds"]

# ── 3b. Blocked kicks — credit to the blocking team (opponent_team) ──────────
# Blocked FGs and PATs come from kicker rows; blocked punts from punter rows.
k_rows = kickers
p_rows = df[df["position"] == "P"].copy()

blocked_fg = (
    k_rows[k_rows["fg_blocked"] > 0]
    .groupby(["opponent_team", "week"], as_index=False)["fg_blocked"]
    .sum()
    .rename(columns={"opponent_team": "team", "fg_blocked": "blocked_fg"})
)
blocked_pat = (
    k_rows[k_rows["pat_blocked"] > 0]
    .groupby(["opponent_team", "week"], as_index=False)["pat_blocked"]
    .sum()
    .rename(columns={"opponent_team": "team", "pat_blocked": "blocked_pat"})
)
blocked_punt = (
    p_rows[p_rows["punt_blocked"] > 0]
    .groupby(["opponent_team", "week"], as_index=False)["punt_blocked"]
    .sum()
    .rename(columns={"opponent_team": "team", "punt_blocked": "blocked_punt"})
) if "punt_blocked" in df.columns else pd.DataFrame(columns=["team", "week", "blocked_punt"])

dst_agg = (
    dst_agg
    .merge(blocked_fg,   on=["team", "week"], how="left")
    .merge(blocked_pat,  on=["team", "week"], how="left")
    .merge(blocked_punt, on=["team", "week"], how="left")
)
dst_agg["blocked_fg"]   = dst_agg["blocked_fg"].fillna(0)
dst_agg["blocked_pat"]  = dst_agg["blocked_pat"].fillna(0)
dst_agg["blocked_punt"] = dst_agg["blocked_punt"].fillna(0)
dst_agg["total_blocked_kicks"] = (
    dst_agg["blocked_fg"] + dst_agg["blocked_pat"] + dst_agg["blocked_punt"]
)

# ── 3c. Points allowed — joined directly from games_2025.csv ─────────────────
# Each game row has home_team/home_score and away_team/away_score.
# We build a team-per-game view so every team gets its opponent's exact score
# as points_allowed, then join to dst_agg on game_id (shared with weekly data).
games = pd.read_csv(r"C:\Users\13012\OneDrive\Documents\vs-code-projects\ff_player_performance\data\cleaned_data\games_2025.csv")
games_reg = games[games["game_type"] == "REG"][
    ["game_id", "week", "home_team", "home_score", "away_team", "away_score"]
].copy()

# Reshape: one row per team per game
home_view = games_reg.rename(columns={
    "home_team": "team", "away_team": "opponent_team",
    "away_score": "points_allowed",   # home team allowed the away score
}).assign(points_scored=games_reg["home_score"])[
    ["game_id", "week", "team", "opponent_team", "points_allowed", "points_scored"]
]
away_view = games_reg.rename(columns={
    "away_team": "team", "home_team": "opponent_team",
    "home_score": "points_allowed",   # away team allowed the home score
}).assign(points_scored=games_reg["away_score"])[
    ["game_id", "week", "team", "opponent_team", "points_allowed", "points_scored"]
]
team_game = pd.concat([home_view, away_view], ignore_index=True)

dst_agg = dst_agg.merge(
    team_game[["team", "week", "opponent_team", "points_allowed"]],
    on=["team", "week"], how="left"
)

# Recompute total_blocked_kicks after the games-CSV merge as a safeguard.
dst_agg["total_blocked_kicks"] = (
    dst_agg["blocked_fg"] + dst_agg["blocked_pat"] + dst_agg["blocked_punt"]
)

# ── 3c-ii. Manual DST corrections ────────────────────────────────────────────
# Use this dict for any DST stats still missing from the raw data.
# Format: (team, week) → {column: value_to_ADD (not replace)}
DST_CORRECTIONS = {
    # Example: ('HOU', 2): {'total_blocked_kicks': 1},
}

for (team, week), adjustments in DST_CORRECTIONS.items():
    mask = (dst_agg["team"] == team) & (dst_agg["week"] == week)
    for col, delta in adjustments.items():
        dst_agg.loc[mask, col] = dst_agg.loc[mask, col] + delta

# ── 3d. Apply DST fantasy scoring ────────────────────────────────────────────
def points_allowed_score(pts):
    """Default ESPN/Yahoo/Sleeper points-allowed tiers."""
    if   pts == 0:        return 10
    elif pts <= 6:        return  7
    elif pts <= 13:       return  4
    elif pts <= 20:       return  1
    elif pts <= 27:       return  0
    elif pts <= 34:       return -1
    else:                 return -4

dst_agg["pa_score"] = dst_agg["points_allowed"].apply(
    lambda x: points_allowed_score(x) if pd.notna(x) else 0
)

dst_agg["fantasy_points_ppr"] = (
    dst_agg["sacks"]               * 1  +
    dst_agg["interceptions"]       * 2  +
    dst_agg["fum_recoveries"]      * 2  +
    dst_agg["safeties"]            * 2  +
    dst_agg["total_dst_tds"]       * 6  +
    dst_agg["total_blocked_kicks"] * 2  +
    dst_agg["pa_score"]
)
dst_agg["fantasy_points"]     = dst_agg["fantasy_points_ppr"]
dst_agg["player_name"]        = dst_agg["team"] + " DST"
dst_agg["player_id"]          = dst_agg["team"] + "_DST"
dst_agg["position"]           = "DST"

# ── Build DST rows that mirror the original CSV schema ───────────────────────
# Start with all-NaN rows for every original column, then fill what we know.
# This lets weekly_stats_2025.csv share a clean schema with skill/kicker rows.
dst_rows = pd.DataFrame(np.nan, index=range(len(dst_agg)), columns=df.columns)

# Identifier fields
dst_rows["player_id"]           = (dst_agg["team"] + "_DST").values
dst_rows["player_name"]         = (dst_agg["team"] + " DST").values
dst_rows["player_display_name"] = (dst_agg["team"] + " DST").values
dst_rows["position"]            = "DST"
dst_rows["position_group"]      = "DST"
dst_rows["headshot_url"]        = dst_agg["team"].map({
    "ARI": "https://a.espncdn.com/i/teamlogos/nfl/500/ari.png",
    "ATL": "https://a.espncdn.com/i/teamlogos/nfl/500/atl.png",
    "BAL": "https://a.espncdn.com/i/teamlogos/nfl/500/bal.png",
    "BUF": "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png",
    "CAR": "https://a.espncdn.com/i/teamlogos/nfl/500/car.png",
    "CHI": "https://a.espncdn.com/i/teamlogos/nfl/500/chi.png",
    "CIN": "https://a.espncdn.com/i/teamlogos/nfl/500/cin.png",
    "CLE": "https://a.espncdn.com/i/teamlogos/nfl/500/cle.png",
    "DAL": "https://a.espncdn.com/i/teamlogos/nfl/500/dal.png",
    "DEN": "https://a.espncdn.com/i/teamlogos/nfl/500/den.png",
    "DET": "https://a.espncdn.com/i/teamlogos/nfl/500/det.png",
    "GB":  "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png",
    "HOU": "https://a.espncdn.com/i/teamlogos/nfl/500/hou.png",
    "IND": "https://a.espncdn.com/i/teamlogos/nfl/500/ind.png",
    "JAX": "https://a.espncdn.com/i/teamlogos/nfl/500/jax.png",
    "KC":  "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
    "LA":  "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png",
    "LAC": "https://a.espncdn.com/i/teamlogos/nfl/500/lac.png",
    "LV":  "https://a.espncdn.com/i/teamlogos/nfl/500/lv.png",
    "MIA": "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png",
    "MIN": "https://a.espncdn.com/i/teamlogos/nfl/500/min.png",
    "NE":  "https://a.espncdn.com/i/teamlogos/nfl/500/ne.png",
    "NO":  "https://a.espncdn.com/i/teamlogos/nfl/500/no.png",
    "NYG": "https://a.espncdn.com/i/teamlogos/nfl/500/nyg.png",
    "NYJ": "https://a.espncdn.com/i/teamlogos/nfl/500/nyj.png",
    "PHI": "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png",
    "PIT": "https://a.espncdn.com/i/teamlogos/nfl/500/pit.png",
    "SEA": "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png",
    "SF":  "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png",
    "TB":  "https://a.espncdn.com/i/teamlogos/nfl/500/tb.png",
    "TEN": "https://a.espncdn.com/i/teamlogos/nfl/500/ten.png",
    "WAS": "https://a.espncdn.com/i/teamlogos/nfl/500/wsh.png",
}).values
dst_rows["team"]                = dst_agg["team"].values
dst_rows["opponent_team"]       = dst_agg["opponent_team"].values
dst_rows["week"]                = dst_agg["week"].values
dst_rows["season"]              = df["season"].iloc[0]
dst_rows["season_type"]         = "REG"

# Map aggregated stats to original column names where they align
dst_rows["def_sacks"]           = dst_agg["sacks"].values
dst_rows["def_interceptions"]   = dst_agg["interceptions"].values
dst_rows["def_safeties"]        = dst_agg["safeties"].values
dst_rows["def_tds"]             = dst_agg["def_tds"].values
dst_rows["fumble_recovery_opp"] = dst_agg["fum_recoveries"].values
dst_rows["special_teams_tds"]   = dst_agg["st_tds"].values
# Blocked kicks re-use the existing fg_blocked / pat_blocked columns
dst_rows["fg_blocked"]          = dst_agg["blocked_fg"].values
dst_rows["pat_blocked"]         = dst_agg["blocked_pat"].values

# Fantasy scores
dst_rows["fantasy_points"]      = dst_agg["fantasy_points_ppr"].values
dst_rows["fantasy_points_ppr"]  = dst_agg["fantasy_points_ppr"].values

# New DST-only columns (not in original schema — appended during concat)
dst_rows["points_allowed"]      = dst_agg["points_allowed"].values
dst_rows["pa_score"]            = dst_agg["pa_score"].values

# Keep the detail-oriented DST file as before (separate, purpose-built columns)
DST_COLS = [
    "player_id", "player_name", "position", "team", "opponent_team", "week",
    "sacks", "interceptions", "fum_recoveries", "safeties",
    "def_tds", "fum_rec_tds", "st_tds", "total_dst_tds",
    "blocked_fg", "blocked_pat", "blocked_punt", "total_blocked_kicks",
    "points_allowed", "pa_score",
    "fantasy_points", "fantasy_points_ppr",
]
dst_weekly = dst_agg[DST_COLS].copy().reset_index(drop=True)
print(f"[DST]    Weekly rows: {len(dst_weekly):,}  (one per team per week)")


# ════════════════════════════════════════════════════════════════════════════
# SECTION 4 — COMBINE INTO UNIFIED weekly_stats & season_totals
# ════════════════════════════════════════════════════════════════════════════

# All three DataFrames share the original 115-column schema.
# dst_rows additionally has points_allowed and pa_score (NaN for other rows).
# Individual defensive players are excluded — absorbed into DST rows.
weekly_combined = pd.concat(
    [skill_weekly, kicker_weekly, dst_rows],
    ignore_index=True
)

# ── Season totals ─────────────────────────────────────────────────────────────
def agg_col(col, agg_fn):
    """Return agg spec only if column exists."""
    return (col, agg_fn) if col in weekly_combined.columns else None

season_totals = (
    weekly_combined
    .groupby(["player_id", "player_name", "player_display_name", "headshot_url", "position", "team"], as_index=False)
    .agg(
        games_played       = ("week",                "count"),
        total_fantasy_ppr  = ("fantasy_points_ppr",  "sum"),
        avg_fantasy_ppr    = ("fantasy_points_ppr",  "mean"),
        std_fantasy_ppr    = ("fantasy_points_ppr",  "std"),
    )
    .sort_values("total_fantasy_ppr", ascending=False)
    .reset_index(drop=True)
)

# Boom/bust (position-aware thresholds)
BOOM_THRESHOLDS = {"QB": 20, "RB": 15, "WR": 15, "TE": 10, "K": 10, "DST": 10}

def add_boom_bust(group):
    thresh = BOOM_THRESHOLDS.get(group["position"].iloc[0], 15)
    pts    = group["fantasy_points_ppr"]
    n      = len(pts)
    group  = group.copy()
    group["boom_rate"] = round((pts >= thresh).sum() / n, 3)
    group["bust_rate"] = round((pts < 5).sum()      / n, 3)
    return group

# Compute boom/bust per player-week on a separate working copy, then aggregate
_bb = weekly_combined[["player_id", "position", "fantasy_points_ppr"]].copy()

def _add_rates(group):
    pos    = group["position"].iloc[0]
    thresh = BOOM_THRESHOLDS.get(pos, 15)
    pts    = group["fantasy_points_ppr"]
    n      = len(pts)
    return pd.Series({
        "boom_rate": round((pts >= thresh).sum() / n, 3),
        "bust_rate": round((pts < 5).sum()      / n, 3),
    })

boom_bust_df = (
    _bb.groupby("player_id")
    .apply(_add_rates)
    .reset_index()
)
season_totals = season_totals.merge(boom_bust_df, on="player_id", how="left")


# ════════════════════════════════════════════════════════════════════════════
# SECTION 5 — SAVE
# ════════════════════════════════════════════════════════════════════════════
import os
OUT = os.path.dirname(os.path.abspath(__file__))   # same folder as this script
OUT = r"C:\Users\13012\OneDrive\Documents\vs-code-projects\ff_player_performance\data\claude_data"

weekly_combined.to_csv(os.path.join(OUT, "weekly_stats_2025.csv"),  index=False)
season_totals.to_csv(  os.path.join(OUT, "season_totals_2025.csv"), index=False)
dst_weekly.to_csv(     os.path.join(OUT, "dst_weekly_2025.csv"),    index=False)
kicker_weekly.to_csv(  os.path.join(OUT, "kicker_weekly_2025.csv"), index=False)

print("\n✓ Saved:")
print("  weekly_stats_2025.csv   — all positions combined, one row per player/team per week")
print("  season_totals_2025.csv  — full-season aggregates with boom/bust rates")
print("  dst_weekly_2025.csv     — DST detail (sacks, INTs, PA, etc.)")
print("  kicker_weekly_2025.csv  — Kicker detail (FG buckets, PATs)")

# ── Sanity checks ─────────────────────────────────────────────────────────────
print("\n── Top 10 PPR scorers (full season, all positions) ──")
print(
    season_totals[["player_name", "position", "team",
                   "games_played", "total_fantasy_ppr", "avg_fantasy_ppr"]]
    .head(10)
    .to_string(index=False)
)

print("\n── Top 5 Kickers (season total) ──")
k_totals = season_totals[season_totals["position"] == "K"].head(5)
print(k_totals[["player_name","team","games_played","total_fantasy_ppr","avg_fantasy_ppr"]].to_string(index=False))

print("\n── Top 5 DSTs (season total) ──")
d_totals = season_totals[season_totals["position"] == "DST"].head(5)
print(d_totals[["player_name","team","games_played","total_fantasy_ppr","avg_fantasy_ppr"]].to_string(index=False))

print("\n── DST scoring spot-check (week 1, top 5) ──")
print(
    dst_weekly[dst_weekly["week"] == 1]
    .nlargest(5, "fantasy_points_ppr")
    [["player_name","week","sacks","interceptions","fum_recoveries",
      "safeties","def_tds","fum_rec_tds","total_dst_tds",
      "total_blocked_kicks","points_allowed","pa_score","fantasy_points_ppr"]]
    .to_string(index=False)
)