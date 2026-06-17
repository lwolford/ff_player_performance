from utils import POSITION_COLORS
import streamlit as st

# Mirror config.toml [theme] — update both together if the palette changes.
_BG1    = "#1a1a2e"
_BG2    = "#2c2c3e"
_TC     = "#e8e8f0"
_BORDER = "rgba(255,255,255,0.08)"
_MUTED  = "rgba(255,255,255,0.45)"


def _val_color(val) -> str:
    return "#EF4444" if str(val).lstrip().startswith("-") else "#ffffff"


def preload_headshots(urls: list) -> None:
    imgs = "".join(
        f'<img src="{url}" style="position:fixed;width:1px;height:1px;opacity:0.01;pointer-events:none;" />'
        for url in urls
    )
    st.markdown(f'<div aria-hidden="true">{imgs}</div>', unsafe_allow_html=True)


def player_banner(player_name: str, position: str, player_icon_url: str, total: float, avg: float, games: int):
    pos_color = POSITION_COLORS.get(position, "#888888")
    img_style = (
        "width:78%;height:78%;margin:11%;object-fit:contain;"
        if position == "DST" else
        "width:100%;height:100%;object-fit:cover;"
    )
    def stat_cell(lbl, val):
        return (
            f'<div style="flex:1;text-align:center;padding:18px 8px;">'
            f'<div style="font-size:10px;color:{_MUTED};letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;">{lbl}</div>'
            f'<div style="font-size:26px;font-weight:700;color:#ffffff;">{val}</div>'
            f'</div>'
        )
    divider = f'<div style="width:1px;background:{_BORDER};margin:12px 0;flex-shrink:0;"></div>'
    st.markdown(
        f'<div style="width:100%;border-radius:18px;overflow:hidden;border:1px solid #e0e0e0;font-family:sans-serif;">'
        f'<div style="background:{pos_color};height:8px;"></div>'
        f'<div style="background:{_BG1};display:flex;align-items:center;padding:24px 28px;gap:24px;">'
        f'<div style="flex-shrink:0;padding:3px;border-radius:50%;background:{pos_color};">'
        f'<div style="width:100px;height:100px;border-radius:50%;overflow:hidden;background:#2a2a3e;">'
        f'<img src="{player_icon_url}" style="{img_style}" /></div></div>'
        f'<div style="flex:1;">'
        f'<div style="font-size:11px;font-weight:600;color:{_MUTED};letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px;">2025 Season</div>'
        f'<div style="font-size:30px;font-weight:800;color:{_TC};line-height:1.1;">{player_name}</div>'
        f'<div style="margin-top:10px;">'
        f'<span style="background:{pos_color};color:#fff;font-size:11px;font-weight:700;padding:3px 12px;border-radius:20px;letter-spacing:0.06em;">{position}</span>'
        f'</div></div></div>'
        f'<div style="background:{_BG2};display:flex;border-top:1px solid {_BORDER};">'
        + stat_cell("Total PPR", round(total, 2))
        + divider
        + stat_cell("Avg / Game", round(avg, 2))
        + divider
        + stat_cell("Games Played", games)
        + f'</div></div>',
        unsafe_allow_html=True,
    )


def player_card_bust(player_name: str, position: str, player_icon_url: str, bust_score: float, avg_score: float, week: int, rank: int = 0):
    pos_color = POSITION_COLORS.get(position, "#888888")
    medal_gradients = {
        1: "linear-gradient(135deg, #B8860B, #FFD700, #FFFACD, #FFD700, #B8860B)",
        2: "linear-gradient(135deg, #707070, #C0C0C0, #FFFFFF, #C0C0C0, #707070)",
        3: "linear-gradient(135deg, #7C3F00, #CD7F32, #F4C07A, #CD7F32, #7C3F00)",
        4: "linear-gradient(135deg, #1e3a5f, #0EA5E9, #BAE6FD, #0EA5E9, #1e3a5f)",
    }
    if rank in medal_gradients:
        ring_open  = f'<div style="padding:3px;border-radius:50%;background:{medal_gradients[rank]};">'
        ring_close = "</div>"
    else:
        ring_open  = '<div style="padding:3px;border-radius:50%;background:rgba(255,255,255,0.1);">'
        ring_close = "</div>"
    img_style = (
        "width:78%;height:78%;margin:11%;object-fit:contain;"
        if position == "DST" else
        "width:100%;height:100%;object-fit:cover;"
    )
    divider = f'<div style="width:1px;background:{_BORDER};margin:8px 0;"></div>'
    def stat_cell(lbl, val, val_color="#ffffff"):
        return (
            f'<div style="flex:1;text-align:center;padding:10px 8px;">'
            f'<div style="font-size:10px;color:{_MUTED};letter-spacing:0.08em;text-transform:uppercase;margin-bottom:2px;">{lbl}</div>'
            f'<div style="font-size:18px;font-weight:700;color:{val_color};">{val}</div>'
            f'</div>'
        )
    st.markdown(
        f'<div style="width:100%;border-radius:18px;overflow:hidden;border:1px solid #e0e0e0;font-family:sans-serif;">'
        f'<div style="background:{pos_color};height:12px;"></div>'
        f'<div style="background:{_BG1};text-align:center;padding:12px 12px 0;font-size:11px;font-weight:600;color:{_MUTED};letter-spacing:0.08em;text-transform:uppercase;">Week {week}</div>'
        f'<div style="background:{_BG1};display:flex;align-items:center;justify-content:center;padding:12px 0 8px;">'
        f'{ring_open}<div style="width:96px;height:96px;border-radius:50%;overflow:hidden;background:#2a2a3e;">'
        f'<img src="{player_icon_url}" style="{img_style}" /></div>{ring_close}</div>'
        f'<div style="background:{_BG1};text-align:center;padding:4px 12px 4px;font-size:14px;font-weight:600;color:{_TC};letter-spacing:0.02em;">{player_name}</div>'
        f'<div style="background:{_BG1};text-align:center;padding:0 12px 10px;">'
        f'<span style="display:inline-block;background:rgba(239,68,68,0.18);border:1px solid rgba(239,68,68,0.4);border-radius:20px;padding:2px 10px;font-size:11px;color:#EF4444;font-weight:600;letter-spacing:0.04em;">↓ {round(avg_score - bust_score, 1)} pts below avg</span>'
        f'</div>'
        f'<div style="background:{_BG2};display:flex;border-top:1px solid {_BORDER};">'
        + stat_cell("Bust Score", round(bust_score, 1), "#EF4444")
        + divider
        + stat_cell("Season Avg", round(avg_score, 1))
        + f'</div></div>',
        unsafe_allow_html=True,
    )


def player_card_boom(player_name: str, position: str, player_icon_url: str, boom_score: float, avg_score: float, week: int, rank: int = 0):
    pos_color = POSITION_COLORS.get(position, "#888888")
    medal_gradients = {
        1: "linear-gradient(135deg, #B8860B, #FFD700, #FFFACD, #FFD700, #B8860B)",
        2: "linear-gradient(135deg, #707070, #C0C0C0, #FFFFFF, #C0C0C0, #707070)",
        3: "linear-gradient(135deg, #7C3F00, #CD7F32, #F4C07A, #CD7F32, #7C3F00)",
        4: "linear-gradient(135deg, #1e3a5f, #0EA5E9, #BAE6FD, #0EA5E9, #1e3a5f)",
    }
    if rank in medal_gradients:
        ring_open  = f'<div style="padding:3px;border-radius:50%;background:{medal_gradients[rank]};">'
        ring_close = "</div>"
    else:
        ring_open  = '<div style="padding:3px;border-radius:50%;background:rgba(255,255,255,0.1);">'
        ring_close = "</div>"
    img_style = (
        "width:78%;height:78%;margin:11%;object-fit:contain;"
        if position == "DST" else
        "width:100%;height:100%;object-fit:cover;"
    )
    divider = f'<div style="width:1px;background:{_BORDER};margin:8px 0;"></div>'
    def stat_cell(lbl, val, val_color="#ffffff"):
        return (
            f'<div style="flex:1;text-align:center;padding:10px 8px;">'
            f'<div style="font-size:10px;color:{_MUTED};letter-spacing:0.08em;text-transform:uppercase;margin-bottom:2px;">{lbl}</div>'
            f'<div style="font-size:18px;font-weight:700;color:{val_color};">{val}</div>'
            f'</div>'
        )
    st.markdown(
        f'<div style="width:100%;border-radius:18px;overflow:hidden;border:1px solid #e0e0e0;font-family:sans-serif;">'
        f'<div style="background:{pos_color};height:12px;"></div>'
        f'<div style="background:{_BG1};text-align:center;padding:12px 12px 0;font-size:11px;font-weight:600;color:{_MUTED};letter-spacing:0.08em;text-transform:uppercase;">Week {week}</div>'
        f'<div style="background:{_BG1};display:flex;align-items:center;justify-content:center;padding:12px 0 8px;">'
        f'{ring_open}<div style="width:96px;height:96px;border-radius:50%;overflow:hidden;background:#2a2a3e;">'
        f'<img src="{player_icon_url}" style="{img_style}" /></div>{ring_close}</div>'
        f'<div style="background:{_BG1};text-align:center;padding:4px 12px 4px;font-size:14px;font-weight:600;color:{_TC};letter-spacing:0.02em;">{player_name}</div>'
        f'<div style="background:{_BG1};text-align:center;padding:0 12px 10px;">'
        f'<span style="display:inline-block;background:rgba(34,197,94,0.18);border:1px solid rgba(34,197,94,0.4);border-radius:20px;padding:2px 10px;font-size:11px;color:#22C55E;font-weight:600;letter-spacing:0.04em;">↑ {round(boom_score - avg_score, 1)} pts above avg</span>'
        f'</div>'
        f'<div style="background:{_BG2};display:flex;border-top:1px solid {_BORDER};">'
        + stat_cell("Boom Score", round(boom_score, 1), "#22C55E")
        + divider
        + stat_cell("Season Avg", round(avg_score, 1))
        + f'</div></div>',
        unsafe_allow_html=True,
    )


def player_card_with_games(player_name: str, position: str, player_icon_url: str, points, games: int, title: str = "", rank: int = 0, label: str = "Total PPR", avg=None):
    pos_color = POSITION_COLORS.get(position, "#888888")
    title_html = (
        f'<div style="background:{_BG1};text-align:center;padding:12px 12px 0;font-size:11px;font-weight:600;color:{_MUTED};letter-spacing:0.08em;text-transform:uppercase;">{title}</div>'
        if title else ""
    )
    medal_gradients = {
        1: "linear-gradient(135deg, #B8860B, #FFD700, #FFFACD, #FFD700, #B8860B)",
        2: "linear-gradient(135deg, #707070, #C0C0C0, #FFFFFF, #C0C0C0, #707070)",
        3: "linear-gradient(135deg, #7C3F00, #CD7F32, #F4C07A, #CD7F32, #7C3F00)",
        4: "linear-gradient(135deg, #1e3a5f, #0EA5E9, #BAE6FD, #0EA5E9, #1e3a5f)",
    }
    if rank in medal_gradients:
        ring_open  = f'<div style="padding:3px;border-radius:50%;background:{medal_gradients[rank]};">'
        ring_close = "</div>"
        icon_border = "border:none;"
    else:
        ring_open  = '<div style="padding:3px;border-radius:50%;background:rgba(255,255,255,0.1);">'
        ring_close = "</div>"
        icon_border = "border:none;"
    img_style = (
        "width:78%;height:78%;margin:11%;object-fit:contain;"
        if position == "DST" else
        "width:100%;height:100%;object-fit:cover;"
    )
    val_size = "16px" if avg is not None else "20px"
    stat_cell = (
        '<div style="flex:1;text-align:center;padding:12px 8px;">'
        '<div style="font-size:10px;color:{muted};letter-spacing:0.08em;text-transform:uppercase;margin-bottom:2px;">{lbl}</div>'
        f'<div style="font-size:{val_size};font-weight:700;color:{{clr}};">{{val}}</div>'
        '</div>'
    )
    divider = f'<div style="width:1px;background:{_BORDER};margin:8px 0;"></div>'
    avg_cell = (
        divider + stat_cell.format(muted=_MUTED, lbl="Avg Per Game", val=avg, clr="#ffffff")
        if avg is not None else ""
    )
    st.markdown(
        f'<div style="width:100%;border-radius:18px;overflow:hidden;border:1px solid #e0e0e0;font-family:sans-serif;">'
        f'<div style="background:{pos_color};height:12px;display:flex;align-items:center;justify-content:space-between;padding:0 10px;"></div>'
        f'{title_html}'
        f'<div style="background:{_BG1};display:flex;align-items:center;justify-content:center;padding:12px 0 8px;">'
        f'{ring_open}<div style="width:96px;height:96px;border-radius:50%;overflow:hidden;{icon_border}background:#2a2a3e;">'
        f'<img src="{player_icon_url}" style="{img_style}" />'
        f'</div>{ring_close}</div>'
        f'<div style="background:{_BG1};text-align:center;padding:4px 12px 10px;font-size:14px;font-weight:600;color:{_TC};letter-spacing:0.02em;">{player_name}</div>'
        f'<div style="background:{_BG2};display:flex;border-top:1px solid {_BORDER};">'
        + stat_cell.format(muted=_MUTED, lbl=label, val=points, clr=_val_color(points))
        + avg_cell
        + divider
        + stat_cell.format(muted=_MUTED, lbl="Games Played", val=games, clr="#ffffff")
        + f'</div></div>',
        unsafe_allow_html=True,
    )


def matchup_card(
    my_name: str, my_total: float, my_win: bool, my_players: list,
    opp_name: str, opp_total: float, opp_players: list,
) -> str:
    def _pos_badge(pos: str) -> str:
        color = POSITION_COLORS.get(pos, "#888")
        return (
            f'<span style="font-size:10px;font-weight:700;color:#fff;background:{color};'
            f'border-radius:3px;width:36px;height:18px;display:inline-flex;align-items:center;'
            f'justify-content:center;flex-shrink:0;">{pos}</span>'
        )

    def _player_cell(p: dict) -> str:
        badge = _pos_badge(p["position"])
        score = f'{p["score"]:.2f}'
        return (
            f'<div style="flex:1;display:flex;align-items:center;padding:8px 14px;">'
            f'{badge}'
            f'<span style="font-size:13px;font-weight:600;color:white;flex:1;margin-left:8px;">{p["name"]}</span>'
            f'<span style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.85);margin-left:12px;">{score}</span>'
            f'</div>'
        )

    my_score_color  = "#22C55E" if my_win else "white"
    opp_score_color = "#22C55E" if not my_win else "white"
    win_tag = (
        '<span style="font-size:9px;font-weight:700;letter-spacing:0.08em;color:#22C55E;'
        'background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.3);'
        'border-radius:3px;padding:1px 6px;">WIN</span>'
    )

    header = (
        f'<div style="display:flex;background:rgba(255,255,255,0.06);border-bottom:1px solid {_BORDER};">'
        f'<div style="flex:1;padding:14px 16px;border-right:1px solid {_BORDER};">'
        f'<div style="font-size:11px;font-weight:700;color:{_MUTED};letter-spacing:0.06em;'
        f'text-transform:uppercase;margin-bottom:4px;">{my_name}</div>'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<span style="font-size:26px;font-weight:800;color:{my_score_color};">{my_total:.2f}</span>'
        f'{win_tag if my_win else ""}'
        f'</div></div>'
        f'<div style="flex:1;padding:14px 16px;text-align:right;">'
        f'<div style="font-size:11px;font-weight:700;color:{_MUTED};letter-spacing:0.06em;'
        f'text-transform:uppercase;margin-bottom:4px;">{opp_name}</div>'
        f'<div style="display:flex;align-items:center;justify-content:flex-end;gap:8px;">'
        f'{win_tag if not my_win else ""}'
        f'<span style="font-size:26px;font-weight:800;color:{opp_score_color};">{opp_total:.2f}</span>'
        f'</div></div>'
        f'</div>'
    )

    rows_html = ""
    for i, (mp, op) in enumerate(zip(my_players, opp_players)):
        bg = "background:rgba(255,255,255,0.02);" if i % 2 == 0 else ""
        rows_html += (
            f'<div style="display:flex;border-top:1px solid rgba(255,255,255,0.05);{bg}">'
            f'{_player_cell(mp)}'
            f'<div style="width:1px;flex-shrink:0;background:{_BORDER};"></div>'
            f'{_player_cell(op)}'
            f'</div>'
        )

    return (
        f'<div style="border-radius:12px;overflow:hidden;border:1px solid {_BORDER};">'
        f'{header}{rows_html}'
        f'</div>'
    )


def _move_chip(player: dict, bg: str, border: str) -> str:
    pos       = player["position"]
    pos_color = POSITION_COLORS.get(pos, "#888888")
    is_dst    = pos == "DST"
    img_style = (
        "width:72%;height:72%;margin:14%;object-fit:contain;"
        if is_dst else
        "width:100%;height:100%;object-fit:cover;"
    )
    img_html = (
        f'<img src="{player["headshot"]}" style="{img_style}" />'
        if player.get("headshot") else
        f'<div style="width:100%;height:100%;display:flex;align-items:center;'
        f'justify-content:center;font-size:12px;font-weight:700;color:{pos_color};">{pos}</div>'
    )
    return (
        f'<div style="display:inline-flex;align-items:center;gap:6px;'
        f'background:{bg};border:1px solid {border};'
        f'border-radius:40px;padding:4px 10px 4px 4px;">'
        f'<div style="width:32px;height:32px;border-radius:50%;overflow:hidden;'
        f'background:#2a2a3e;border:2px solid {pos_color};flex-shrink:0;">'
        f'{img_html}</div>'
        f'<span style="font-size:12px;font-weight:600;color:white;white-space:nowrap;">'
        f'{player["name"]}</span>'
        f'</div>'
    )


def _move_row(week: int, label: str, label_color: str, label_bg: str, label_border: str, body_html: str) -> str:
    return (
        f'<div style="display:flex;align-items:center;gap:14px;padding:12px 16px;'
        f'border-radius:8px;background:rgba(255,255,255,0.04);'
        f'border:1px solid {_BORDER};margin-bottom:8px;flex-wrap:wrap;">'
        f'<div style="font-size:10px;font-weight:700;color:{_MUTED};'
        f'background:rgba(255,255,255,0.07);border-radius:4px;padding:3px 7px;'
        f'white-space:nowrap;flex-shrink:0;">Wk {week}</div>'
        f'<div style="font-size:10px;font-weight:700;color:{label_color};'
        f'background:{label_bg};border:1px solid {label_border};'
        f'border-radius:4px;padding:3px 7px;letter-spacing:0.05em;'
        f'white-space:nowrap;flex-shrink:0;">{label}</div>'
        f'{body_html}'
        f'</div>'
    )


def trade_row(week: int, gave: list, received: list) -> str:
    sent_chips = "".join(
        _move_chip(p, "rgba(239,68,68,0.07)", "rgba(239,68,68,0.3)") for p in gave
    )
    recv_chips = "".join(
        _move_chip(p, "rgba(34,197,94,0.07)", "rgba(34,197,94,0.3)") for p in received
    )
    body = (
        f'<div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">{sent_chips}</div>'
        f'<div style="font-size:16px;color:{_MUTED};flex-shrink:0;">→</div>'
        f'<div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">{recv_chips}</div>'
    )
    return _move_row(week, "TRADE", "#F97316", "rgba(249,115,22,0.1)", "rgba(249,115,22,0.3)", body)


def waiver_row(week: int, pickups: list) -> str:
    chips = "".join(
        _move_chip(p, "rgba(34,197,94,0.07)", "rgba(34,197,94,0.3)") for p in pickups
    )
    body = f'<div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;">{chips}</div>'
    return _move_row(week, "WAIVER", "#22C55E", "rgba(34,197,94,0.1)", "rgba(34,197,94,0.3)", body)


def roster_grid(players: list, new_players: set, original_players: set | None = None) -> str:
    _POS_ORDER = ["QB", "RB", "WR", "TE", "K", "DST"]

    grouped: dict[str, list] = {pos: [] for pos in _POS_ORDER}
    for p in players:
        pos = p["position"]
        if pos in grouped:
            grouped[pos].append(p)

    def _chip(player: dict) -> str:
        pos          = player["position"]
        pos_color    = POSITION_COLORS.get(pos, "#888888")
        is_new       = player["name"] in new_players
        is_original  = original_players is not None and player["name"] in original_players
        is_dst       = pos == "DST"
        img_style = (
            "width:72%;height:72%;margin:14%;object-fit:contain;"
            if is_dst else
            "width:100%;height:100%;object-fit:cover;"
        )
        img_html  = (
            f'<img src="{player["headshot"]}" style="{img_style}" />'
            if player["headshot"] else
            f'<div style="width:100%;height:100%;display:flex;align-items:center;'
            f'justify-content:center;font-size:12px;font-weight:700;color:{pos_color};">{pos}</div>'
        )
        if is_new:
            chip_bg     = "rgba(34,197,94,0.07)"
            chip_border = "rgba(34,197,94,0.35)"
        elif is_original:
            chip_bg     = "rgba(234,179,8,0.07)"
            chip_border = "rgba(234,179,8,0.40)"
        else:
            chip_bg     = "rgba(255,255,255,0.04)"
            chip_border = _BORDER
        new_badge = (
            '<span style="font-size:9px;font-weight:700;color:#22C55E;'
            'background:rgba(34,197,94,0.15);border-radius:3px;'
            'padding:1px 5px;letter-spacing:0.05em;margin-left:4px;">NEW</span>'
            if is_new else
            '<span style="font-size:9px;font-weight:700;color:#EAB308;'
            'background:rgba(234,179,8,0.15);border-radius:3px;'
            'padding:1px 5px;letter-spacing:0.05em;margin-left:4px;">OG</span>'
            if is_original else ""
        )
        return (
            f'<div style="display:inline-flex;align-items:center;gap:8px;'
            f'background:{chip_bg};border:1px solid {chip_border};'
            f'border-radius:40px;padding:5px 12px 5px 5px;">'
            f'<div style="width:36px;height:36px;border-radius:50%;overflow:hidden;'
            f'background:#2a2a3e;border:2px solid {pos_color};flex-shrink:0;">'
            f'{img_html}</div>'
            f'<span style="font-size:13px;font-weight:600;color:white;white-space:nowrap;">'
            f'{player["name"]}</span>'
            f'{new_badge}'
            f'</div>'
        )

    rows_html = ""
    for pos in _POS_ORDER:
        group = grouped.get(pos, [])
        if not group:
            continue
        pos_color = POSITION_COLORS.get(pos, "#888888")
        chips     = "".join(_chip(p) for p in group)
        rows_html += (
            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">'
            f'<div style="min-width:46px;font-size:11px;font-weight:700;color:{pos_color};'
            f'border:1px solid {pos_color};border-radius:4px;padding:4px 6px;'
            f'text-align:center;flex-shrink:0;">{pos}</div>'
            f'<div style="display:flex;gap:8px;flex-wrap:wrap;">{chips}</div>'
            f'</div>'
        )

    return (
        f'<div style="background:rgba(255,255,255,0.02);border:1px solid {_BORDER};'
        f'border-radius:12px;padding:16px 18px;">'
        f'{rows_html}'
        f'</div>'
    )


def draft_card(player: dict) -> str:
    pos       = player["position"]
    pos_color = POSITION_COLORS.get(pos, "#888888")
    is_dst    = pos == "DST"
    img_style = (
        "width:72%;height:72%;margin:14%;object-fit:contain;"
        if is_dst else
        "width:100%;height:100%;object-fit:cover;"
    )
    if player["headshot"]:
        img_html = f'<img src="{player["headshot"]}" style="{img_style}" />'
    else:
        img_html = (
            f'<div style="width:100%;height:100%;display:flex;align-items:center;'
            f'justify-content:center;font-size:14px;font-weight:700;color:{pos_color};">'
            f'{pos}</div>'
        )

    return (
        f'<div style="border-radius:10px;overflow:hidden;border:1px solid {_BORDER};'
        f'background:rgba(255,255,255,0.04);">'
        f'<div style="background:{pos_color};height:6px;"></div>'
        f'<div style="padding:18px 10px 16px;text-align:center;">'
        f'<div style="width:68px;height:68px;border-radius:50%;overflow:hidden;'
        f'background:#2a2a3e;border:2px solid {pos_color};margin:0 auto 10px;">'
        f'{img_html}</div>'
        f'<div style="font-size:13px;font-weight:700;color:white;'
        f'line-height:1.3;margin-bottom:8px;">{player["name"]}</div>'
        f'<div style="display:inline-block;background:{pos_color};color:#fff;'
        f'font-size:10px;font-weight:700;border-radius:4px;padding:2px 8px;'
        f'letter-spacing:0.05em;margin-bottom:10px;">{pos}</div>'
        f'<div style="font-size:12px;color:rgba(255,255,255,0.55);">'
        f'Rd {player["round"]} &nbsp;·&nbsp; #{player["pick"]}</div>'
        f'</div></div>'
    )


def player_card(player_name: str, position: str, player_icon_url: str, points, title: str = "", rank: int = 0, label: str = "PPR Points"):
    pos_color = POSITION_COLORS.get(position, "#888888")
    title_html = (
        f'<div style="background:{_BG1};text-align:center;padding:12px 12px 0;font-size:11px;font-weight:600;color:{_MUTED};letter-spacing:0.08em;text-transform:uppercase;">{title}</div>'
        if title else ""
    )
    medal_gradients = {
        1: "linear-gradient(135deg, #B8860B, #FFD700, #FFFACD, #FFD700, #B8860B)",
        2: "linear-gradient(135deg, #707070, #C0C0C0, #FFFFFF, #C0C0C0, #707070)",
        3: "linear-gradient(135deg, #7C3F00, #CD7F32, #F4C07A, #CD7F32, #7C3F00)",
        4: "linear-gradient(135deg, #1e3a5f, #0EA5E9, #BAE6FD, #0EA5E9, #1e3a5f)",
    }
    if rank in medal_gradients:
        ring_open  = f'<div style="padding:3px;border-radius:50%;background:{medal_gradients[rank]};">'
        ring_close = "</div>"
        icon_border = "border:none;"
    else:
        ring_open  = '<div style="padding:3px;border-radius:50%;background:rgba(255,255,255,0.1);">'
        ring_close = "</div>"
        icon_border = "border:none;"
    img_style = (
        "width:78%;height:78%;margin:11%;object-fit:contain;"
        if position == "DST" else
        "width:100%;height:100%;object-fit:cover;"
    )
    st.markdown(
        f'<div style="width:100%;border-radius:18px;overflow:hidden;border:1px solid #e0e0e0;font-family:sans-serif;">'
        f'<div style="background:{pos_color};height:12px;display:flex;align-items:center;justify-content:space-between;padding:0 10px;"></div>'
        f'{title_html}'
        f'<div style="background:{_BG1};display:flex;align-items:center;justify-content:center;padding:12px 0 8px;">'
        f'{ring_open}<div style="width:96px;height:96px;border-radius:50%;overflow:hidden;{icon_border}background:#2a2a3e;">'
        f'<img src="{player_icon_url}" style="{img_style}" />'
        f'</div>{ring_close}</div>'
        f'<div style="background:{_BG1};text-align:center;padding:4px 12px 10px;font-size:14px;font-weight:600;color:{_TC};letter-spacing:0.02em;">{player_name}</div>'
        f'<div style="background:{_BG2};text-align:center;padding:12px;border-top:1px solid {_BORDER};">'
        f'<div style="font-size:10px;color:{_MUTED};letter-spacing:0.08em;text-transform:uppercase;margin-bottom:2px;">{label}</div>'
        f'<div style="font-size:22px;font-weight:700;color:{_val_color(points)};">{points}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )
