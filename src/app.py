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
from shiny import App, render, ui, reactive
from shinywidgets import render_plotly, output_widget
from pathlib import Path


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

app_ui = ui.page_fluid(

    ui.panel_title("Social Media Addiction Dashboard"),

    ui.layout_sidebar(

        # ── SIDEBAR: filters go here ──────────────────────────────────
        ui.sidebar(

            ui.h6("Filters"),

            # TODO: Add filter controls here
            # Examples:
            #   ui.input_radio_buttons(...)   → Gender
            #   ui.input_slider(...)          → Age range
            #   ui.input_select(...)          → Academic level
            #   ui.input_selectize(...)       → Country, Platform
            #   ui.input_action_button(...)   → Reset button

            ui.p("[ Filters go here ]", style="color: gray; font-style: italic;"),

            open="desktop",
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
                ui.p(
                    "[ Horizontal bar: % Yes vs No ]",
                    style="color: gray; font-style: italic; padding: 40px; text-align: center;",
                ),
                full_screen=True,
            ),

            ui.card(
                ui.card_header("Academic Level"),
                ui.p(
                    "[ Donut chart: Undergraduate vs Graduate ]",
                    style="color: gray; font-style: italic; padding: 40px; text-align: center;",
                ),
                full_screen=True,
            ),

            ui.card(
                ui.card_header("Sleep Distribution"),
                ui.p(
                    "[ Bar chart: students per sleep bucket (<5h, 5-6h, ...) ]",
                    style="color: gray; font-style: italic; padding: 40px; text-align: center;",
                ),
                full_screen=True,
            ),

            ui.card(
                ui.card_header("Platform Distribution"),
                ui.p(
                    "[ Donut chart: share by most-used platform ]",
                    style="color: gray; font-style: italic; padding: 40px; text-align: center;",
                ),
                full_screen=True,
            ),

            col_widths=[3, 3, 3, 3],
        ),

        # Row 3: map and more
        ui.layout_columns(
            ui.card(
                ui.card_header("foobar"),
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

    # ── Filtered data ─────────────────────────────────────────────────
    # TODO: Add filter logic here once sidebar inputs are wired up.
    # For now, filtered() just returns the full dataset.

    @reactive.calc
    def filtered():
        return df.copy()

    # ── Stat tiles ────────────────────────────────────────────────────
    # TODO: Uncomment and wire up once value_box uses output_text(...)

    @render.text
    def tile_students():
        return str(len(filtered()))

    @render.text
    def tile_usage():
        d = filtered()
        return f"{d['Avg_Daily_Usage_Hours'].mean():.1f}h" if len(d) else "—"

    @render.text
    def tile_sleep():
        d = filtered()
        return f"{d['Sleep_Hours_Per_Night'].mean():.1f}h" if len(d) else "—"

    @render.text
    def tile_addiction():
        d = filtered()
        return f"{d['Addicted_Score'].mean():.1f}" if len(d) else "—"

    # ── Map ───────────────────────────────────────────────────────────
    # TODO: Implement and uncomment when the UI card uses output_widget("map_chart")

    @render_plotly
    def map_chart():
        d = filtered().copy()
        d = d[d['Country'].isin(['Canada', 'Mexico'])]
        
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
        
        fig = px.choropleth(
            df_selected,
            locations='iso_alpha',
            locationmode='ISO-3',
            color='Addicted_Score',
            color_continuous_scale='Reds',
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

        #fig.add_trace(fig_unselected.data[0])
        fig.update_geos(fitbounds="locations", showframe=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        
        return fig

    # ── Chart 1: Affects Academic Performance ─────────────────────────
    # TODO: Implement and uncomment when the UI card uses output_widget("chart_affects")

    # @render_plotly
    # def chart_affects():
    #     ...

    # ── Chart 2: Academic Level ───────────────────────────────────────
    # TODO: Implement and uncomment when the UI card uses output_widget("chart_level")

    # @render_plotly
    # def chart_level():
    #     ...

    # ── Chart 3: Sleep Distribution ───────────────────────────────────
    # TODO: Implement and uncomment when the UI card uses output_widget("chart_sleep")

    # @render_plotly
    # def chart_sleep():
    #     ...

    # ── Chart 4: Platform Distribution ───────────────────────────────
    # TODO: Implement and uncomment when the UI card uses output_widget("chart_platform")

    # @render_plotly
    # def chart_platform():
    #     ...

    pass 

# ── APP ───────────────────────────────────────────────────────────────

app = App(app_ui, server)
