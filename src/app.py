"""
Social Media Addiction Analytics Dashboard — Skeleton
Install:  pip install shiny shinywidgets plotly pandas
Run:      shiny run app.py
Open:     http://127.0.0.1:8000
"""

# ── IMPORTS ───────────────────────────────────────────────────────────

import pandas as pd
import plotly.graph_objects as go
from shiny import App, render, ui, reactive
from shinywidgets import render_plotly, output_widget, render_altair
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
        # TODO: Update value_box text/icons and wire up to real server output
        ui.layout_columns(
            ui.value_box("Total Students",      "[ count ]"),
            ui.value_box("Avg Daily Usage",     "[ X.X h ]"),
            ui.value_box("Avg Sleep Hours",     "[ X.X h ]"),
            ui.value_box("Avg Addiction Score", "[ X.X ]"),
            fill=False,
        ),

        # Row 2: World map placeholder
        ui.card(
            ui.card_header("Avg Addiction Score by Country"),
            # TODO: Replace ui.p with output_widget("map_chart")
            # and implement map_chart in the server
            ui.p(
                "[ World choropleth map goes here — avg addiction score per country ]",
                style="color: gray; font-style: italic; padding: 60px; text-align: center;",
            ),
            full_screen=True,
        ),

        # Row 3: Four chart placeholders in a 2x2 grid
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
                ui.p(
                    "[ Donut chart: Undergraduate vs Graduate ]",
                    style="color: gray; font-style: italic; padding: 40px; text-align: center;",
                ),
                full_screen=True,
            ),

            ui.card(
                ui.card_header("Academic Level Distribution"),
                output_widget("plot_academiclvldist"),
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
    ),
)

# ── SERVER ───────────────────────────────────────────────────────────

def server(input, output, session):

    # ── Filtered data ─────────────────────────────────────────────────
    # TODO: Add filter logic here once sidebar inputs are wired up.
    # For now, filtered() just returns the full dataset.

    @reactive.calc
    def filtered_df():
        data = df.copy()
        data = data[data["Academic_Level"].isin(["Undergraduate", "Graduate"])]

        if input.academiclvl() != "All":
            data = data[data["Academic_Level"] == input.academiclvl()] 
        
        if input.gender() != "All":
            data = data[data["Gender"] == input.gender()] 
        
        data = data[data["Age"].between(input.age()[0], input.age()[1])]

        return data

    # ── Stat tiles ────────────────────────────────────────────────────
    # TODO: Uncomment and wire up once value_box uses output_text(...)

    # @render.text
    # def tile_students():
    #     return str(len(filtered()))

    # @render.text
    # def tile_usage():
    #     d = filtered()
    #     return f"{d['Avg_Daily_Usage_Hours'].mean():.1f}h" if len(d) else "—"

    # @render.text
    # def tile_sleep():
    #     d = filtered()
    #     return f"{d['Sleep_Hours_Per_Night'].mean():.1f}h" if len(d) else "—"

    # @render.text
    # def tile_score():
    #     d = filtered()
    #     return f"{d['Addicted_Score'].mean():.1f}" if len(d) else "—"

    # ── Map ───────────────────────────────────────────────────────────
    # TODO: Implement and uncomment when the UI card uses output_widget("map_chart")

    # @render_plotly
    # def map_chart():
    #     ...

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
            tooltip = [alt.Tooltip("Affects_Academic_Performance:N", title = "Affects Academic Performance?"),
            alt.Tooltip("Count:Q", title = "Number of Students"),
            alt.Tooltip("Percentage:Q", title = "Percentage of Students being Affected")]
        )

        return chart + chart.mark_text(align = "left").encode(text = alt.Text("label:N"), color=alt.value('black'))

    # ── Chart 2: Academic Level ───────────────────────────────────────
    # TODO: Implement and uncomment when the UI card uses output_widget("chart_level")

    # @render_plotly
    # def chart_level():
    #     ...

    # ── Chart 3: Academic Level Distribution ───────────────────────────────────
    @render_altair
    def plot_academiclvldist():
        df = filtered_df()

        group_gender_df = df.groupby(["Academic_Level", "Gender"]).size().reset_index(name="Count")

        chart = alt.Chart(group_gender_df).mark_bar().encode(
            alt.X("Academic_Level:N",
                title = "Academic Level",
                sort = ["Undergraduate", "Graduate"]),

            alt.Y("Count:Q",
                title = "Number of Students"),

            alt.Color("Gender:N",
                scale = alt.Scale(
                    domain = ["Male", "Female"]),
                    legend=alt.Legend(title="Gender")
                    ),
            order = alt.Order("Gender:N", sort="ascending"),
            tooltip = [alt.Tooltip("Academic_Level:N", title="Academic Level"),
            alt.Tooltip("Gender:N", title="Gender"),
            alt.Tooltip("Count:Q", title="Number of Students")
            ])

        return chart

    # ── Chart 4: Platform Distribution ───────────────────────────────
    # TODO: Implement and uncomment when the UI card uses output_widget("chart_platform")

    # @render_plotly
    # def chart_platform():
    #     ...

    pass 

# ── APP ───────────────────────────────────────────────────────────────

app = App(app_ui, server)
