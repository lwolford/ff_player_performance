relevant_positions = [
    "QB", 
    "RB", 
    "WR", 
    "TE"
]

weekly_data_columns_general = [
    "player_id",
    "player_display_name",
    "headshot_url",
    "position",
    "team",
    "opponent_team",
    "season",
    "week"
]

weekly_data_columns_passing = ["passing_yards", "passing_tds", "passing_2pt_conversions"]
weekly_data_columns_rushing = ["rushing_yards", "rushing_tds", "carries", "rushing_2pt_conversions"]
weekly_data_columns_receiving = ["targets", "receptions", "receiving_yards", "receiving_tds"]
weekly_data_columns_turnovers = ["passing_interceptions", "sack_fumbles_lost", "rushing_fumbles_lost", "receiving_fumbles_lost"]
weekly_data_columns_fantasy = ["fantasy_points", "fantasy_points_ppr"]

boom_thresholds_map = {
    "QB": 20,
    "RB": 15,
    "WR": 15,
    "TE": 10
}