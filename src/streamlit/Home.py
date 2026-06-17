import streamlit as st

st.set_page_config(page_title="FF Dashboard", page_icon="🏈")

pg = st.navigation({
    "": [
        st.Page("pages/home_page.py",         title="Home",              icon="🏠"),
        st.Page("pages/my_fantasy_story.py",  title="My Fantasy Story",  icon="📖"),
        st.Page("pages/table_of_contents.py", title="Table of Contents", icon="📋"),
    ],
    "The Golden Cleat Awards": [
        st.Page("pages/best_players.py",         title="PPR Royalty",           icon="⭐"),
        st.Page("pages/team_carriers.py",         title="Carrying the Load",     icon="🏈"),
        st.Page("pages/best_games.py",            title="Ceiling Shatterers",    icon="🔥"),
        st.Page("pages/no_td_needed.py",          title="We Need TDs?",          icon="🚫"),
        st.Page("pages/unexpected_booms.py",      title="Lightning in a Bottle", icon="💥"),
        st.Page("pages/glow_ups.py",              title="Late Bloomers",         icon="📈"),
        st.Page("pages/league_winners.py",        title="Set & Forget",          icon="🏆"),
        st.Page("pages/playoff_winners.py",       title="When It Matters Most",  icon="🥇"),
        st.Page("pages/defense_vs_position.py",   title="Position Proof",        icon="🛡️"),
    ],
    "The JaMarcus Awards": [
        st.Page("pages/worst_players.py",              title="They Participated", icon="🔻"),
        st.Page("pages/worst_games.py",                title="Walk of Shame",     icon="🥶"),
        st.Page("pages/biggest_busts.py",              title="You Had One Job",   icon="⬇️"),
        st.Page("pages/fall_offs.py",                  title="Running on Empty",  icon="📉"),
        st.Page("pages/defense_vs_position_worst.py",  title="Position Sieve",    icon="🪣"),
    ],
    "General": [
        st.Page("pages/player_lookup.py",      title="Player Lookup",   icon="🔍"),
        st.Page("pages/player_comparison.py",  title="Compare Players", icon="⚖️"),
        st.Page("pages/team_fantasy_points.py", title="Team Scores",    icon="🏟️"),
    ],
})

pg.run()
