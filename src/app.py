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
from shinywidgets import render_plotly, output_widget


# ── DATA ─────────────────────────────────────────────────────────────

df = pd.read_csv("../data/raw/Students Social Media Addiction.csv")

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
