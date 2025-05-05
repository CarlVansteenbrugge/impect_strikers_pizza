import matplotlib.pyplot as plt
from mplsoccer import PyPizza, FontManager
from strikers import load_striker_data

# Fonts ophalen',
font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab[wght].ttf')


params = ['PERCENTILE IMPECT_SCORE_PACKING',
'PERCENTILE PROGRESSION_SCORE_PACKING',
 'PERCENTILE OFFENSIVE_IMPECT_SCORE_PACKING',
 'PERCENTILE SCORER_SCORE',

 'PERCENTILE PXT',
 'PERCENTILE IMPECT_SCORE_PXT',
 'PERCENTILE OFFENSIVE_IMPECT_SCORE_PXT',


'PERCENTILE HOLD_UP_PLAY_SCORE',
 'PERCENTILE RATIO_GROUND_DUELS',

 'PERCENTILE TOTAL_TOUCHES',
 'PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_AM',
  'PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_IBW',
 'PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_IB',


 'PERCENTILE AVAILABILITY_OUT_WIDE_SCORE',
 'PERCENTILE AVAILABILITY_BTL_SCORE',
 'PERCENTILE AVAILABILITY_FDR_SCORE',
 'PERCENTILE AVAILABILITY_IN_THE_BOX_SCORE',

 'PERCENTILE RATIO_MINUTES_PER_SHOT_XG',

 'PERCENTILE RATIO_POSTSHOT_XG_SHOT_XG',
 'PERCENTILE CLOSE_RANGE_SHOT_SCORE',
 'PERCENTILE ONE_VS_ONE_AGAINST_GK_SCORE',
 'PERCENTILE HEADER_SHOT_SCORE',
 'PERCENTILE OFFENSIVE_HEADER_SCORE'
]


param_labels = {
    'PERCENTILE IMPECT_SCORE_PACKING': 'Packing\nScore',
    'PERCENTILE PROGRESSION_SCORE_PACKING': 'Progression\nPacking Score',
    'PERCENTILE OFFENSIVE_IMPECT_SCORE_PACKING': 'Offensive\nPacking Score',
    'PERCENTILE SCORER_SCORE': 'Scorer\nScore',
    
    'PERCENTILE PXT': 'PXT Score',
    'PERCENTILE IMPECT_SCORE_PXT': 'Impect\nPXT Score',
    'PERCENTILE OFFENSIVE_IMPECT_SCORE_PXT': 'Offensive\nPXT Score',
    
    'PERCENTILE HOLD_UP_PLAY_SCORE': 'Hold-up\nPlay',
    'PERCENTILE RATIO_GROUND_DUELS': 'Ground\nDuels',
    
    'PERCENTILE TOTAL_TOUCHES': 'Total\nTouches',
    'PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_AM': 'Touches\nAM Zone',
    'PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_IBW': 'Touches\nIn Behind Wide',
    'PERCENTILE TOTAL_TOUCHES_IN_PACKING_ZONE_IB': 'Touches\nIn Behind Central',
    
    'PERCENTILE AVAILABILITY_OUT_WIDE_SCORE': 'Availability\nOut Wide',
    'PERCENTILE AVAILABILITY_BTL_SCORE': 'Availability\nBetween the Lines',
    'PERCENTILE AVAILABILITY_FDR_SCORE': 'Availability\nDeep Runs',
    'PERCENTILE AVAILABILITY_IN_THE_BOX_SCORE': 'Availability\nIn the Box',
    
    'PERCENTILE RATIO_MINUTES_PER_SHOT_XG': 'Minutes\nper Shot xG',

    'PERCENTILE RATIO_POSTSHOT_XG_SHOT_XG': 'Postshot xG/xG',
    'PERCENTILE CLOSE_RANGE_SHOT_SCORE': 'Close Range\nShots',
    'PERCENTILE ONE_VS_ONE_AGAINST_GK_SCORE': '1v1 vs GK\nScore',
    'PERCENTILE HEADER_SHOT_SCORE': 'Header\nShot Score',
    'PERCENTILE OFFENSIVE_HEADER_SCORE': 'Offensive\nHeader'
}

def Pizza_plot_forwards(player_name,df=None):
    if df is None:
        df = load_striker_data()
    # Zorg ervoor dat de speler in de DataFrame staat   
    row = df[df['playerName'] == player_name].iloc[0]
    values = [row[param] for param in params]
    labels = [param_labels.get(p, p) for p in params]

    slice_colors = ["#43A427"] * 4 + ["#f65252"] *3 + ["#fbc921"] * 2 + ["#20C581"] * 4 + ["#4D6CF8"] * 4 + ["#ceea3d"] * 1+ ["#B45EE3"] * 5
    text_colors = ["#000000"] * len(params)

    baker = PyPizza(
        params=labels, background_color="#F1F1F1", straight_line_color="#F1F1F1",
        straight_line_lw=1, last_circle_lw=0, other_circle_lw=0, inner_circle_size=10)

    fig, ax = baker.make_pizza(
        values, figsize=(8, 8.5), color_blank_space="same",
        slice_colors=slice_colors, value_colors=text_colors, value_bck_colors=slice_colors,
        blank_alpha=0.3,
        kwargs_slices=dict(edgecolor="#000000", zorder=2, linewidth=0.5),
        kwargs_params=dict(color="#000000", fontsize=8, fontproperties=font_normal.prop),
        kwargs_values=dict(color="#000000", fontsize=8, fontproperties=font_normal.prop,
                           bbox=dict(edgecolor="#000000", facecolor="cornflowerblue",
                                     boxstyle="round,pad=0.2", lw=1))
    )

    fig.text(0.515, 0.975, f"{player_name} - {row['squadName']}", size=20,
             ha="center", fontproperties=font_bold.prop, color="#000000")
    fig.text(0.515, 0.953, "Percentile Rank vs Forwards  |  Minimum 500 mins played",
             size=10, ha="center", fontproperties=font_bold.prop, color="#000000")

    return fig

