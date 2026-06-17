import streamlit as st
from utils import DST_LOGO_URLS
from html_elements import draft_card, roster_grid, trade_row, waiver_row, matchup_card

st.title("📖 My Fantasy Story")

st.markdown("""
This page goes over the story of my first time playing Fantasy Football in 2025, and finding a surpising amount 
of fun competing. Now, I want to do multiple Fanytasy Leagues this year.
""")

st.markdown("---")

# ── Section 1: The Draft ──────────────────────────────────────────────────────
st.markdown("## 📋 The Drafted Team")

st.markdown("""
This was my first time playing fantasy football. I say that not as an excuse. I say it as the only plausible explanation for what you're about to see.

The league was mostly first-timers too — only 2 of the 10 managers had actually played before. It showed. C.J. Stroud went as a first-round pick. Jaylen Waddle went before Tyreek Hill. The concept of ADP was, collectively, lost on us. It was lost on me specifically. That did not stop me from drafting like I understood it.
""")

DRAFT = [
    {"pick": 5,   "round": 1,  "name": "J.Allen",          "position": "QB",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/servs1fpsynfxep4rz2z"},
    {"pick": 16,  "round": 2,  "name": "D.Achane",          "position": "RB",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/xk1xwio0bryfxo1ylweu"},
    {"pick": 25,  "round": 3,  "name": "N.Collins",         "position": "WR",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/osmqyvmib3pssxi6cyic"},
    {"pick": 36,  "round": 4,  "name": "X.Worthy",          "position": "WR",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/ue6fp8xwnyo7ftvabbb8"},
    {"pick": 45,  "round": 5,  "name": "T.Henderson",       "position": "RB",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/cfcux3dnfmbmz3qzrnco"},
    {"pick": 56,  "round": 6,  "name": "M.Andrews",         "position": "TE",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/wzx3p0hzm3qyqsrfqznb"},
    {"pick": 65,  "round": 7,  "name": "J.Conner",          "position": "RB",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/g5yjordcmt76j0saytzb"},
    {"pick": 76,  "round": 8,  "name": "C.McLaughlin",      "position": "K",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/vwefhtevyn2qxauchan5"},
    {"pick": 85,  "round": 9,  "name": "DEN DST",           "position": "DST",
     "headshot": DST_LOGO_URLS["DEN"]},
    {"pick": 96,  "round": 10, "name": "D.Prescott",        "position": "QB",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/blixemm3s9sa4gmqk5yn"},
    {"pick": 105, "round": 11, "name": "D.Adams",           "position": "WR",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/qtonvcqpixixqhc6lhnc"},
    {"pick": 116, "round": 12, "name": "J.Mason",           "position": "RB",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/ixykwytfrfz1cdxlhj5w"},
    {"pick": 125, "round": 13, "name": "T.Kraft",           "position": "TE",
     "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/yr6nj1zqaqg6nbdnxu3q"},
    {"pick": 136, "round": 14, "name": "HOU DST",           "position": "DST",
     "headshot": DST_LOGO_URLS["HOU"]},
    {"pick": 145, "round": 15, "name": "T.Bass",            "position": "K",
     "headshot": ""},
]


COLS_PER_ROW = 5
rows = [DRAFT[i:i + COLS_PER_ROW] for i in range(0, len(DRAFT), COLS_PER_ROW)]

grid_rows_html = ""
for row in rows:
    cards = "".join(
        f'<div style="flex:1;min-width:0;">{draft_card(p)}</div>'
        for p in row
    )
    grid_rows_html += (
        f'<div style="display:flex;gap:8px;margin-bottom:8px;">{cards}</div>'
    )

st.markdown(grid_rows_html, unsafe_allow_html=True)

st.markdown("""
With limited knowledge, most of my picks were — to put it charitably — questionable (ADP sourced from Fantasy Pros):

- **Josh Allen** was a great player, but I took him at **#5** when his ADP was **20.2**. That's 15 spots early. On purpose.
- **Xavier Worthy** went at **#36** when his ADP was **54.8**, and he immediately got injured. By his own teammate. By. His. Own. Teammate.
- **Mark Andrews** at **#56** when his ADP was **74.3** — another reach, another lesson, another line on this list.

That said, I wasn't *completely* lost:

- **De'Von Achane** was drafted right at his ADP and proceeded to be an absolute monster all season. Fins Up! I only picked him because I casually liked the Dolphins.
- **Nico Collins** had an ADP of **13.2** and somehow fell to **#25**. I didn't know he was such a steal at the time.
- **Davante Adams** dropped to **#105** despite an ADP of **40.3**. This decision was made thanks to pure luck, and managers lacking in knowledge.
""")

st.markdown("---")

# ── Section 2: The 2-5 Start ─────────────────────────────────────────────────
st.markdown("## 📉 The 2–5 Start")

st.markdown("""
Before the season, I did some research. I made some moves. I added Austin Ekeler. I added Jerry Jeudy.

We'll get to that.

My Week 1 roster looked like this — players highlighted in green were pre-season additions:
""")

WEEK1 = [
    {"name": "J.Allen",       "position": "QB",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/servs1fpsynfxep4rz2z"},
    {"name": "D.Prescott",    "position": "QB",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/blixemm3s9sa4gmqk5yn"},
    {"name": "D.Achane",      "position": "RB",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/xk1xwio0bryfxo1ylweu"},
    {"name": "J.Conner",      "position": "RB",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/g5yjordcmt76j0saytzb"},
    {"name": "T.Henderson",   "position": "RB",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/cfcux3dnfmbmz3qzrnco"},
    {"name": "A.Ekeler",      "position": "RB",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/sldndpn2zwt4uhkj2zks"},
    {"name": "N.Collins",     "position": "WR",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/osmqyvmib3pssxi6cyic"},
    {"name": "X.Worthy",      "position": "WR",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/ue6fp8xwnyo7ftvabbb8"},
    {"name": "D.Adams",       "position": "WR",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/qtonvcqpixixqhc6lhnc"},
    {"name": "J.Jeudy",       "position": "WR",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/szca1v9butuqkjs7ekpm"},
    {"name": "M.Andrews",     "position": "TE",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/wzx3p0hzm3qyqsrfqznb"},
    {"name": "T.Kraft",       "position": "TE",  "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/yr6nj1zqaqg6nbdnxu3q"},
    {"name": "C.McLaughlin",  "position": "K",   "headshot": "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/vwefhtevyn2qxauchan5"},
    {"name": "DEN DST",       "position": "DST", "headshot": DST_LOGO_URLS["DEN"]},
    {"name": "HOU DST",       "position": "DST", "headshot": DST_LOGO_URLS["HOU"]},
]

WEEK1_NEW = {"A.Ekeler", "J.Jeudy"}

st.markdown(roster_grid(WEEK1, WEEK1_NEW), unsafe_allow_html=True)

st.markdown("""
This team led me to the incredible record of ... 2–5. I was in **9th place**. Out of 10.

**James Conner**: season-ending injury. **Austin Ekeler**: season-ending injury. **Xavier Worthy**: hurt early, and never really performed anyway. **TreVeyon Henderson**: reached for him and he was not worth it in the first half of the season. And **Jerry Jeudy** (I said we'd get to Jerry Jeudy). Jerry Jeudy was one of the worst waiver pickups I've ever made in my life, and I made some bad waiver pickups this season. **Mark Andrews**, who I reached for in Round 6, was somehow outperformed by the tight end I grabbed two rounds from the very end of the draft. Honestly, Jake Tonges would have been a better pick, and Jake Tonges is a backup on a team that already has George f-ing Kittle.

I tried to fix it:

- **Week 3** — Picked up **Quinshon Judkins** off waivers
- **Week 4** — Grabbed **Courtland Sutton** after another team dropped him (inexplicably)
- **Week 5** — Added **Rico Dowdle** following Chuba Hubbard's injury
- **Week 6** — Traded away Xavier Worthy and Mark Andrews for an IR'd **George Kittle** and a banged-up **Jaylen Warren**

None of it worked. But something else was happening in the background — the more I lost, the more
I watched. Flock Fantasy videos between games. Sal Vetri breaking down the waiver wire every week.
FantasyLand Football giving me their starts and sits for the week. A Twitter feed that had quietly 
become half fantasy analysis without me really noticing. And when that still wasn't enough, I started 
pulling the actual data myself, which is where I actually began to love playing Fantasy Football. 
Somewhere between Weeks 5 and 8, I continued making gut calls, but started making gut
calls I could somewhat explain. Week 8 was when that started to show.
""")

st.markdown("---")

# ── Section 3: The Rebuild ────────────────────────────────────────────────────
st.markdown("## 🔄 The Rebuild Rampage")

st.markdown("""
Week 8, I was matched up against **Brian's B1tch** — the best team in the league at 6–1. On paper, this was a loss. I did not have paper.

**151.82 – 97.16**. Josh Allen dropped 23 points, De'Von Achane added 20, and then Tucker Kraft — my Round 13 tight end dart throw — put up 33. A kicker named Chase McLaughlin scored 17. I beat the best team in the league by 54 points. I have no notes.

After this win, I felt confidence in myself. I no longer felt like a Jake Tonges, but a George Kittle. I knew I could come back and win this, starting with blowing up current roster:
""")

_HS = "https://static.www.nfl.com/image/upload/f_auto,q_auto,w_128,h_128,c_fill,g_face/league/"

st.markdown(
    trade_row(
        week=8,
        gave=[
            {"name": "D.Prescott", "position": "QB", "headshot": _HS + "blixemm3s9sa4gmqk5yn"},
        ],
        received=[
            {"name": "T.Higgins", "position": "WR", "headshot": _HS + "flr9f8oqigbyroeaubxb"},
        ],
    ),
    unsafe_allow_html=True,
)

st.markdown(
    trade_row(
        week=9,
        gave=[
            {"name": "R.Dowdle", "position": "RB", "headshot": _HS + "cvnrzndsiaojvvxz8vo5"},
            {"name": "D.Adams",  "position": "WR", "headshot": _HS + "qtonvcqpixixqhc6lhnc"},
        ],
        received=[
            {"name": "D.London", "position": "WR", "headshot": _HS + "np91pvk7mczra1iyjkmo"},
        ],
    ),
    unsafe_allow_html=True,
)

st.markdown(
    waiver_row(
        week=9,
        pickups=[
            {"name": "A.Brown", "position": "WR", "headshot": "https://static.www.nfl.com/image/private/f_auto,q_auto/league/a014sgzctarbvhwb35lw"},
            {"name": "T.Tracy", "position": "RB", "headshot": _HS + "b9nje50lohbprf06xoom"},
        ],
    ),
    unsafe_allow_html=True,
)

st.markdown(
    trade_row(
        week=13,
        gave=[
            {"name": "Q.Judkins", "position": "RB", "headshot": _HS + "ojtce2im0wp2ltyel0vc"},
            {"name": "J.Warren",  "position": "RB", "headshot": _HS + "f3txbqdarbabqtq4sx98"},
        ],
        received=[
            {"name": "C.Brown",  "position": "RB", "headshot": _HS + "pv3sq3uzosixxexbznq5"},
            {"name": "K.Walker", "position": "RB", "headshot": _HS + "mnzsnemdzbey5hbahdhk"},
        ],
    ),
    unsafe_allow_html=True,
)

st.markdown("""
The Week 8 trade was a bet-it-all on Superman move. I shipped out Dak Prescott and committed to Josh Allen
as my only quarterback for the rest of the year. For any reasonable person, this is risky, as the QBs
left on the waiver were less than desirable. For me, it was worth the risk.

The Week 9 trade worked out better than I had any right to expect: Drake London immediately went on
a tear from Weeks 9–11, starting the moment I acquired him. A.J. Brown's owner had completely given
up on him after a rough first half, so I grabbed him off waivers, and he made quite the comeback. 
Tyrone Tracy came in after Cam Skattebo's season-ending injury opened up carries for the Giants,
and I happened to be paying attention that week (although he didn't stick around for long).

Week 10: **172.98 points**. The 3rd highest single-week score in the entire league all season.
Only Brian's B1tch had scored higher — and she had to do it twice just to beat my one week.

The Week 13 deadline trade swapped Judkins and Warren for Chase Brown and Kenneth Walker, unknowingly
giving me an absolute monster in the fantasy playoffs.

I won out the rest of the regular season. Finished **10–5**, the **2nd highest scoring team** in
the league — only 30 points behind Brian's B1tch on the year. I had started this thing in 9th
place. The data helped. The more I dug in, the better the decisions got.
""")

st.markdown("---")

# ── Section 4: The Playoff Team ───────────────────────────────────────────────
st.markdown("## 🏆 The Playoff Team")

st.markdown("""
Quick note: this app treats Weeks 15–17 as the fantasy playoffs, but our league actually started
playoffs in Week 16 (*we were all new, we were figuring it out*).

By Week 16, my roster looked almost nothing like what I had drafted. Players highlighted in green
were late-season waiver additions, as I grew addicted to waivers and the joy they brought:
""")

PLAYOFFS = [
    {"name": "J.Allen",      "position": "QB",  "headshot": _HS + "servs1fpsynfxep4rz2z"},
    {"name": "D.Achane",     "position": "RB",  "headshot": _HS + "xk1xwio0bryfxo1ylweu"},
    {"name": "C.Brown",      "position": "RB",  "headshot": _HS + "pv3sq3uzosixxexbznq5"},
    {"name": "K.Walker",     "position": "RB",  "headshot": _HS + "mnzsnemdzbey5hbahdhk"},
    {"name": "K.Gainwell",   "position": "RB",  "headshot": _HS + "f74x1ywy7oo5kq81vblh"},
    {"name": "N.Collins",    "position": "WR",  "headshot": _HS + "osmqyvmib3pssxi6cyic"},
    {"name": "C.Sutton",     "position": "WR",  "headshot": _HS + "r2sr6cbma4c7wc3isejj"},
    {"name": "T.Higgins",    "position": "WR",  "headshot": _HS + "flr9f8oqigbyroeaubxb"},
    {"name": "D.London",     "position": "WR",  "headshot": _HS + "np91pvk7mczra1iyjkmo"},
    {"name": "A.Brown",      "position": "WR",  "headshot": "https://static.www.nfl.com/image/private/f_auto,q_auto/league/a014sgzctarbvhwb35lw"},
    {"name": "T.McLaurin",   "position": "WR",  "headshot": _HS + "wokz1etv1wj1vhbmvxgs"},
    {"name": "G.Kittle",     "position": "TE",  "headshot": _HS + "ztz3xqjaqgok9m4nylgs"},
    {"name": "C.McLaughlin", "position": "K",   "headshot": _HS + "vwefhtevyn2qxauchan5"},
    {"name": "HOU DST",      "position": "DST", "headshot": DST_LOGO_URLS["HOU"]},
    {"name": "NE DST",       "position": "DST", "headshot": DST_LOGO_URLS["NE"]},
]

PLAYOFFS_NEW = {"K.Gainwell", "T.McLaurin", "NE DST"}
PLAYOFFS_OG  = {"J.Allen", "D.Achane", "N.Collins", "C.McLaughlin", "HOU DST"}

st.markdown(roster_grid(PLAYOFFS, PLAYOFFS_NEW, PLAYOFFS_OG), unsafe_allow_html=True)

st.markdown("""
Drake London was back from the injury he picked up in overtime in Week 11. Tee Higgins was back
after missing time with a concussion in Week 14. Three legitimate RBs. Five WR options. Josh Allen
at quarterback.

I felt, for the first time all season, like I actually knew what I was doing.
""")

st.markdown("---")

# ── Section 5: The Run ────────────────────────────────────────────────────────
st.markdown("## 🏈 Week 16 vs Football Fetish")

st.markdown("""
Week 16 was messy, and to make it worse I was facing the team I had traded with
at the deadline — meaning **Quinshon Judkins** and **Jaylen Warren**, both of whom I shipped away,
were now lining up against me. I knew if I lost because of the trade, I'd feel like a moron.

But no thanks to Josh Allen, I still got it done.
""")

st.markdown(
    matchup_card(
        my_name="Me", my_total=137.40, my_win=True,
        my_players=[
            {"name": "J.Allen",       "position": "QB",  "score": 6.90},
            {"name": "C.Brown",       "position": "RB",  "score": 32.90},
            {"name": "D.Achane",      "position": "RB",  "score": 18.00},
            {"name": "A.Brown",       "position": "WR",  "score": 18.50},
            {"name": "N.Collins",     "position": "WR",  "score": 9.90},
            {"name": "G.Kittle",      "position": "TE",  "score": 24.50},
            {"name": "D.London",      "position": "WR",  "score": 5.70},
            {"name": "C.McLaughlin",  "position": "K",   "score": 10.00},
            {"name": "HOU DST",       "position": "DST", "score": 11.00},
        ],
        opp_name="Football Fetish", opp_total=126.00,
        opp_players=[
            {"name": "B.Mayfield",   "position": "QB",  "score": 12.70},
            {"name": "J.Taylor",     "position": "RB",  "score": 16.90},
            {"name": "Q.Judkins",    "position": "RB",  "score": 10.10},
            {"name": "C.Lamb",       "position": "WR",  "score": 11.10},
            {"name": "Q.Johnston",   "position": "WR",  "score": 20.40},
            {"name": "K.Pitts",      "position": "TE",  "score": 18.70},
            {"name": "J.Warren",     "position": "RB",  "score": 29.10},
            {"name": "J.Myers",      "position": "K",   "score": 2.00},
            {"name": "ATL DST",      "position": "DST", "score": 5.00},
        ],
    ),
    unsafe_allow_html=True,
)

st.markdown("""
The win came with a cost. George Kittle went for 24.50 points and then got hurt, leaving me with
no tight end heading into the championship. I went to waivers and picked up his backup — a guy
named Jake Tonges — and hoped for the best.
""")

st.markdown("---")

# ── Section 6: The Championship ───────────────────────────────────────────────
st.markdown("## 🏆 Week 17 vs Brian's B1tch")

st.markdown("""
All season long, **Brian's B1tch** had been the best team in the league. Dominant from Week 1.
**Never** seriously threatened. **Never** in doubt. 

I was the underdog here. I had climbed from 9th place to the **#2 seed**. My all-star wide receiver room
was fully healthy. My backfield was deep. Josh Allen was my quarterback. And my starting tight end was *the* **Jake Tonges**.
            
I set my roster, including Jake Tonges, and it all came down to this one moment. I beat her once before,
but could I truly take down the Queen of this league once again?
""")

with st.expander("🏆 Click to reveal the result..."):
    st.markdown(
        matchup_card(
            my_name="Me", my_total=117.48, my_win=False,
            my_players=[
                {"name": "J.Allen",      "position": "QB",  "score": 23.18},
                {"name": "C.Brown",      "position": "RB",  "score": 29.10},
                {"name": "D.Achane",     "position": "RB",  "score": 14.20},
                {"name": "T.Higgins",    "position": "WR",  "score": 9.90},
                {"name": "N.Collins",    "position": "WR",  "score": 8.70},
                {"name": "J.Tonges",     "position": "TE",  "score": 19.00},
                {"name": "D.London",     "position": "WR",  "score": 1.40},
                {"name": "C.McLaughlin", "position": "K",   "score": 5.00},
                {"name": "NE DST",       "position": "DST", "score": 7.00},
            ],
            opp_name="Brian's B1tch", opp_total=157.10,
            opp_players=[
                {"name": "C.Williams",   "position": "QB",  "score": 23.00},
                {"name": "B.Hall",       "position": "RB",  "score": 20.90},
                {"name": "B.Robinson",   "position": "RB",  "score": 39.90},
                {"name": "A.St.Brown",   "position": "WR",  "score": 14.80},
                {"name": "P.Nacua",      "position": "WR",  "score": 15.70},
                {"name": "T.McBride",    "position": "TE",  "score": 23.60},
                {"name": "T.Henderson",  "position": "RB",  "score": 8.20},
                {"name": "J.Bates",      "position": "K",   "score": 4.00},
                {"name": "DET DST",      "position": "DST", "score": 7.00},
            ],
        ),
        unsafe_allow_html=True,
    )

    st.markdown("""
Josh Allen went for 23. Chase Brown went for 29. I scored 117, which on most weeks would have
been enough.

**Bijan Robinson** posted his season-high on championship night. The **overall WR #1 in Puka Nacua**
showed up. The **overall WR #3 in Amon-Ra St. Brown** showed up. The **overall TE #1 in Trey McBride**
dropped 23 points against me. All in the same week. It was that kind of night.

157–117. Not particularly close.

For the record: **Jake Tonges scored 19 points**. My three wide receivers — Tee Higgins, Nico Collins,
and Drake London — combined for 20. Jake Tonges, a backup tight end on a team that already had George
Kittle, came within one point of matching every wide receiver on my roster put together. At the end of the
day, a part of Fantasy Football also comes down to luck. If the data was a perfect science, Fantasy Football
wouldn't be as fun. Rooting for Tonges passing his projected point total of 4.10 is part of the fun. My wide 
receivers not showing up is also part of the fun, even if it feels terrible in the moment.

I'm not going to tell you I deserved to win. But I went from 9th place to the championship, rebuilt
the whole roster from scratch, and lost to the best team in the league on a night where nothing was
going to be enough. I watched more film than I expected to. Pulled more data than I expected to.
And somewhere along the way, I got genuinely good at this — or at least good enough. I'll take it.
    """)
