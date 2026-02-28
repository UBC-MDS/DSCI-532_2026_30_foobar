"""
Social Media Addiction Analytics Dashboard — Skeleton
Install:  pip install shiny shinywidgets plotly pandas
Run:      shiny run app.py
Open:     http://127.0.0.1:8000
"""

# ── IMPORTS ───────────────────────────────────────────────────────────

import pandas as pd
import plotly.express as px
import pycountry
import altair as alt
from shiny import App, render, ui, reactive
from shinywidgets import render_plotly, render_altair, output_widget
from pathlib import Path
import altair as alt


# ── DATA ─────────────────────────────────────────────────────────────

# Build a robust path (works locally + on Connect Cloud)
HERE = Path(__file__).resolve().parent        # src/
ROOT = HERE.parent                           # project root
DATA_PATH = ROOT / "data" / "raw" / "Students-Social-Media-Addiction.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at {DATA_PATH}. "
        "Make sure the CSV is committed inside data/raw/."
    )

df = pd.read_csv(DATA_PATH)


AGE_MIN = int(df["Age"].min())
AGE_MAX = int(df["Age"].max())

#df_all_country = df.groupby("Country", as_index=False).agg({
#    "Student_ID": "count",
#    "Avg_Daily_Usage_Hours": "mean",
#    "Sleep_Hours_Per_Night": "mean",
#    "Addicted_Score": "mean",
#})
MIN_SCORE = df["Addicted_Score"].min()
MAX_SCORE = df["Addicted_Score"].max()


# ── UI ───────────────────────────────────────────────────────────────

custom_css = """

h2, .panel-title {
    color: #0F1F3D !important;
}

body {
    background-color: #F4F6F9 !important;
}

.card-header {
    background-color: #c8d2df !important;
    color: #0F1F3D !important;
    font-weight: bold;
}

.card {
    border: none !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
}

.bslib-value-box {
    border: none !important;
    border-left: 5px solid #c8d2df !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    color: #0F1F3D !important;
}

.shiny-text-output {
    color: #0F1F3D !important;
}
"""

app_ui = ui.page_fluid(

    ui.head_content(
        ui.tags.style(custom_css)
    ),

    ui.panel_title("Social Media Addiction Dashboard"),

    ui.layout_sidebar(

        # ── SIDEBAR: filters go here ──────────────────────────────────
        ui.sidebar(

            ui.h6("Filters"),

            # Filter 1: Gender (radio buttons)
            ui.input_radio_buttons(
                id="f_gender",
                label="Gender",
                choices={"All": "All", "Male": "Male", "Female": "Female"},
                selected="All",
                inline=True,
            ),

            # Filter 2: Age range (slider with two handles)
            ui.input_slider(
                id="f_age",
                label="Age range",
                min=AGE_MIN,
                max=AGE_MAX,
                value=[AGE_MIN, AGE_MAX],
            ),

            # Filter 3: Academic level (single dropdown)
            ui.input_select(
                id="f_level",
                label="Academic level",
                choices={"All": "All", "Undergraduate": "Undergraduate", "Graduate": "Graduate"},
                selected="All",
            ),

            # Filter 4: Country (multi-select)
            ui.input_selectize(
                id="f_country",
                label="Country",
                choices=sorted(df["Country"].unique().tolist()),
                multiple=True,
            ),

            # Filter 5: Platform (multi-select)
            ui.input_selectize(
                id="f_platform",
                label="Platform",
                choices=sorted(df["Most_Used_Platform"].unique().tolist()),
                multiple=True,
            ),


            open="desktop",
            bg = "#EEF1F6",
            fg = "#0F1F3D",
        ),

        # ── MAIN AREA ─────────────────────────────────────────────────

        # Row 1: Summary stat tiles
        ui.layout_columns(
            ui.value_box("Total Students", ui.output_text("tile_students")),
            ui.value_box("Avg Daily Usage", ui.output_text("tile_usage")),
            ui.value_box("Avg Sleep Hours", ui.output_text("tile_sleep")),
            ui.value_box("Avg Addiction Score", ui.output_text("tile_addiction")),
            fill=False,
        ),


        # Row 2: Four chart placeholders in a 2x2 grid
        # TODO: Replace each ui.p with the matching output_widget(...)
        # and implement the corresponding render function in the server
        ui.layout_columns(

            ui.card(
                ui.card_header("Affects Academic Performance"),
                output_widget("plot_AAP"),
                full_screen=True,
            ),

            ui.card(
                ui.card_header("Academic Level"),
                output_widget("donut_academic_level"),
                full_screen=True,
                ),

            ui.card(
                ui.card_header("Academic Level Distribution"),
                output_widget("plot_academiclvldist"),
                full_screen=True,
            ),

            ui.card(
                ui.card_header("Platform Distribution"),
                output_widget("donut_platform"),
                full_screen=True,
                ),

            col_widths=[3, 3, 3, 3],
        ),

        # Row 3: map and more
        ui.layout_columns(
            ui.card(
                ui.card_header("Addiction vs Mental Health & Sleep"),
                output_widget("scatter_chart"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Avg Addiction Score by Country"),
                output_widget("map_chart"),
                full_screen=True,
            ),
        ),
    ),
)

# ── SERVER ───────────────────────────────────────────────────────────

def server(input, output, session):

    custom_ui_scale = alt.Scale(
        range=['#0F1F3D', '#2D6BE4', '#26f7fd'],
        type='linear'
    )
    

    # ── Filtered data ─────────────────────────────────────────────────
    # TODO: Add filter logic here once sidebar inputs are wired up.
    # For now, filtered_df() just returns the full dataset.

    @reactive.calc
    def filtered_df():
        data = df.copy()
        data = data[data["Academic_Level"].isin(["Undergraduate", "Graduate"])]

        if input.f_gender() != "All":
            data = data[data["Gender"] == input.f_gender()]

        age_low, age_high = input.f_age()
        data = data[(data["Age"] >= age_low) & (data["Age"] <= age_high)]

        if input.f_level() != "All":
            data = data[data["Academic_Level"] == input.f_level()]

        if input.f_country():  # empty tuple means "all countries"
            data = data[data["Country"].isin(input.f_country())]

        if input.f_platform():
            data = data[data["Most_Used_Platform"].isin(input.f_platform())]

        return data

    # ── Stat tiles ────────────────────────────────────────────────────
    # TODO: Uncomment and wire up once value_box uses output_text(...)

    @render.text
    def tile_students():
        return str(len(filtered_df()))

    @render.text
    def tile_usage():
        d = filtered_df()
        return f"{d['Avg_Daily_Usage_Hours'].mean():.1f}h" if len(d) else "—"

    @render.text
    def tile_sleep():
        d = filtered_df()
        return f"{d['Sleep_Hours_Per_Night'].mean():.1f}h" if len(d) else "—"

    @render.text
    def tile_addiction():
        d = filtered_df()
        return f"{d['Addicted_Score'].mean():.1f}" if len(d) else "—"

    @render_altair
    def scatter_chart():
        d = filtered_df()
        fig = alt.Chart(d).transform_calculate(
            jitter_addiction="datum.Addicted_Score + 0.4 * (random() + random() - 1)",
            jitter_mental="datum.Mental_Health_Score + 0.4 * (random() + random() - 1)"
        ).mark_circle(size=50, opacity=0.7).encode(
            x=alt.X(
                "jitter_addiction:Q", 
                title="Addiction Score", 
                scale=alt.Scale(zero=False)
            ),
            y=alt.Y(
                "jitter_mental:Q", 
                title="Mental Health Score", 
                scale=alt.Scale(zero=False)
            ),
            color=alt.Color(
                "Sleep_Hours_Per_Night", 
                title="Sleep Time (hrs)", 
                scale=custom_ui_scale#alt.Scale(scheme="viridis")
            ),
            tooltip=["Addicted_Score", "Mental_Health_Score", "Sleep_Hours_Per_Night"]
        ).interactive()
        
        return fig

    # ── Map ───────────────────────────────────────────────────────────

    @render_plotly
    def map_chart():
        d = filtered_df().copy()
        #d = d[d['Country'].isin(['Canada', 'Mexico'])]
        
        #selected_country = d['Country'].unique()
        #df_selected = df_all_country[df_all_country['Country'].isin(selected_country)]
        #df_unselected = df_all_country[~df_all_country['Country'].isin(selected_country)]

        #fig_unselected = px.choropleth(
        #    df_unselected,
        #    locations='Country',
        #    locationmode='country names',
        #    color='Addicted_Score',
        #    color_continuous_scale='Reds',
        #    range_color=[MIN_SCORE, MAX_SCORE]
        #)
        #fig_unselected.update_traces(
        #    marker = dict(opacity=0.2),
        #    hoverinfo = 'skip',
        #    hovertemplate = None,
        #)

        df_selected = d.groupby("Country", as_index=False).agg({
            "Student_ID": "count",
            "Avg_Daily_Usage_Hours": "mean",
            "Sleep_Hours_Per_Night": "mean",
            "Addicted_Score": "mean",
        })

        def get_iso3(country_name):
            try:
                return pycountry.countries.search_fuzzy(country_name)[0].alpha_3
            except:
                return None # Handle unrecognized countries

        df_selected['iso_alpha'] = df_selected['Country'].apply(get_iso3)
        df_selected = df_selected.dropna(subset=['iso_alpha'])
        fig = px.choropleth(
            df_selected,
            locations='iso_alpha',
            locationmode='ISO-3',
            color='Addicted_Score',
            color_continuous_scale=[
                [0.0, '#0F1F3D'],
                [0.3, '#517BD6'],
                [1.0, '#26f7fd']
            ],#'viridis',
            range_color=[MIN_SCORE, MAX_SCORE],
            hover_name='Country',
            labels={
                'Student_ID': 'Total Students',
                'Avg_Daily_Usage_Hours': 'Avg Daily Usage (hrs)',
                'Sleep_Hours_Per_Night': 'Sleep per Night (hrs)',
                'Addicted_Score': 'Addicted Score'
            },
            hover_data={
                'Country': False,
                'iso_alpha': False,
                'Student_ID': True,
                'Avg_Daily_Usage_Hours': ":.1f",
                'Sleep_Hours_Per_Night': ":.1f",
                'Addicted_Score': ":.1f"
            },
        )
        fig.update_coloraxes(reversescale=True)


        #fig.add_trace(fig_unselected.data[0])
        fig.update_geos(fitbounds="locations", showframe=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        
        return fig

    # ── Chart 1: Does social media affect academic performance? ─────────────────────────
    @render_altair
    def plot_AAP():
        df1 = filtered_df()
        #calculate the percentage
        percent = (df1.groupby("Affects_Academic_Performance").size().reset_index(name="Count"))
        percent["Percentage"] = (percent["Count"] / percent["Count"].sum() * 100).round(1)
        percent["label"] = percent["Percentage"].astype(str) + "%"


        chart = alt.Chart(percent).mark_bar().encode(
            alt.Y("Affects_Academic_Performance:N", title = "Impact on Academic Performance"),
            alt.X("Percentage:Q", title = "Percentage of Students"),
            alt.Color("Affects_Academic_Performance:N", scale=alt.Scale(domain=["Yes", "No"],
            range=["#c0392b", "#1e3a6e"]), legend = None),

            tooltip = [alt.Tooltip("Affects_Academic_Performance:N", title = "Affects Academic Performance?"),
            alt.Tooltip("Count:Q", title = "Number of Students"),
            alt.Tooltip("Percentage:Q", title = "Percentage of Students being Affected")]
        )

        return chart + chart.mark_text(align = "left").encode(text = alt.Text("label:N"), color=alt.value('black'))

    # ── Chart 3: Academic Level Distribution ───────────────────────────────────
    @render_altair
    def plot_academiclvldist():
        df = filtered_df()

        group_gender_df = df.groupby(["Academic_Level", "Gender"]).size().reset_index(name="Count")

        chart = alt.Chart(group_gender_df).mark_bar().encode(
            alt.X("Academic_Level:N",
                title = "Academic Level",
                sort = ["Undergraduate", "Graduate"],
                axis=alt.Axis(labelAngle=0)),

            alt.Y("Count:Q",
                title = "Number of Students"),

            alt.Color("Gender:N",
                scale = alt.Scale(
                    domain = ["Male", "Female"], range=["#1e3a6e", "#5ba4cf"]),
                    legend=alt.Legend(title="Gender"),
                    ),

            order = alt.Order("Gender:N", sort="ascending"),
            tooltip = [alt.Tooltip("Academic_Level:N", title="Academic Level"),
            alt.Tooltip("Gender:N", title="Gender"),
            alt.Tooltip("Count:Q", title="Number of Students")
            ])

        return chart

    # ── Chart 4: Platform Distribution ───────────────────────────────

    @render_altair
    def donut_platform():
        d = filtered_df()
        
        platform_counts = (
            d.groupby("Most_Used_Platform")
            .size()
            .reset_index(name="Count")
        )
        
        total = int(platform_counts["Count"].sum()) if len(platform_counts) else 0
        
        if total > 0:
            platform_counts["Percentage"] = (platform_counts["Count"] / total * 100).round(1).astype(str) + "%"
        else:
            platform_counts["Percentage"] = []
            
        donut = alt.Chart(platform_counts).encode(
            theta=alt.Theta("Count:Q", stack=True),
            color=alt.Color("Most_Used_Platform:N", title="Platform",
            scale=alt.Scale(
                domain=["Facebook", "Instagram", "KakaoTalk", "LINE", "LinkedIn",
                        "Snapchat", "TikTok", "Twitter", "VKontakte",
                        "WeChat", "WhatsApp", "YouTube"],
                range=["#1e3a6e", "#2d6be4", "#5ba4cf", "#4f6bed", "#7b8fab",
                       "#a8b8cc", "#0f1f3d", "#3a5a9e", "#6d8fc0", "#b8c8e0", "#d0dff0", "#bfd4e8"],
            )),
            tooltip=[
                alt.Tooltip("Most_Used_Platform:N", title="Platform"),
                alt.Tooltip("Count:Q", title="Students"),
                alt.Tooltip("Percentage:N", title="Percentage"),
            ],
        ).mark_arc(innerRadius=30)
        
        return donut
    
    # ── Chart 2: Academic Level ───────────────────────────────
    @render_altair
    def donut_academic_level():
        d = filtered_df()
        
        level_counts = (
        d.groupby("Academic_Level")
        .size()
        .reset_index(name="Count")
        )
        
        
        
        total = int(level_counts["Count"].sum()) if len(level_counts) else 0

        if total > 0:
            level_counts["Percentage"] = (level_counts["Count"] / total * 100).round(1).astype(str) + "%"
        else:
            level_counts["Percentage"] = []

        donut = (
            alt.Chart(level_counts)
            .encode(
                theta=alt.Theta("Count:Q"),
                color=alt.Color("Academic_Level:N", title="Academic Level",
                scale=alt.Scale(
                domain=["Undergraduate", "Graduate"],
                range=["#1e3a6e", "#5ba4cf"],
            )),
                tooltip=[
                    alt.Tooltip("Academic_Level:N", title="Academic Level"),
                    alt.Tooltip("Count:Q", title="Students"),
                    alt.Tooltip("Percentage:N", title="Percentage"),
                ],
            )
        ).mark_arc(innerRadius=30)
        
        return donut
        
        
    
        

# ── APP ───────────────────────────────────────────────────────────────

app = App(app_ui, server)
