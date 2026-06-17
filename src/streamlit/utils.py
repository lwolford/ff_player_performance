import re
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"
WEEKLY_STATS_PATH  = DATA_DIR / "claude_data" / "weekly_stats_2025.csv"
SEASON_TOTALS_PATH = DATA_DIR / "claude_data" / "season_totals_2025.csv"

def set_headshot_resolution(url: str, size: int) -> str:
    if not isinstance(url, str):
        return ""
    if re.search(r"w_\d+,h_\d+", url):
        return re.sub(r"w_\d+,h_\d+", f"w_{size},h_{size}", url)
    # URLs from the 2025 dataset have no size params — inject them into the
    # Cloudinary transformation chain and add face-centered fill crop.
    return re.sub(
        r"(/image/upload/)([^/]+)(/)",
        rf"\1\2,w_{size},h_{size},c_fill,g_face\3",
        url,
    )

POSITIONS = ["All", "QB", "RB", "WR", "TE", "K", "DST"]

# Keyed by nfl-data-py team abbreviation → ESPN 500 px team logo URL.
# Note: LA = Rams (nfl-data-py) maps to ESPN's "lar"; WAS maps to ESPN's "wsh".
DST_LOGO_URLS = {
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
}

POSITION_COLORS = {
    "QB": "#3B82F6",
    "RB": "#22C55E",
    "WR": "#F97316",
    "TE": "#A855F7",
    "K":  "#EAB308",
    "DST": "#EF4444",
}

SLIDER_THUMB_CSS = (
    '<style>div[data-testid="stSlider"] [role="slider"]{'
    "height:38px !important;width:14px !important;border-radius:6px !important;}"
    "</style>"
)


def read_page_content(page_file: str, content_name: str) -> str:
    return (Path(page_file).parent.parent / "content" / content_name).read_text(encoding="utf-8").strip()


def apply_dst_logos(df: pd.DataFrame) -> pd.DataFrame:
    dst_mask = df["position"] == "DST"
    df.loc[dst_mask, "headshot_url"] = df.loc[dst_mask, "team"].map(DST_LOGO_URLS)
    return df


def add_headshot_lg(df: pd.DataFrame, size: int = 512) -> pd.DataFrame:
    df = df.copy()
    df["headshot_url_lg"] = df["headshot_url"].apply(lambda u: set_headshot_resolution(u, size))
    return df


def build_preload_urls(df: pd.DataFrame, column: str | None = None, n: int = 4, largest: bool = True) -> list[str]:
    if column is None:
        top_fn = lambda d: d.head(n)
    elif largest:
        top_fn = lambda d: d.nlargest(n, column)
    else:
        top_fn = lambda d: d.nsmallest(n, column)
    preload = set(top_fn(df)["headshot_url_lg"])
    for pos in POSITIONS[1:]:
        subset = df[df["position"] == pos]
        if not subset.empty:
            preload.update(top_fn(subset)["headshot_url_lg"])
    return list(preload)


def filter_by_position(df: pd.DataFrame, selected: str | None) -> pd.DataFrame:
    if selected and selected != "All":
        return df[df["position"] == selected]
    return df


def hex_to_rgba(color: str, alpha: float = 1.0) -> str:
    if color.startswith("rgba"):
        return color.rsplit(",", 1)[0] + f",{alpha})"
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"
