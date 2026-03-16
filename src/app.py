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
import ibis
from shiny import App, render, ui, reactive
from shinywidgets import render_plotly, render_altair, output_widget
from pathlib import Path
from querychat import QueryChat
from dotenv import load_dotenv
import plotly.graph_objects as go

# ── DATA ─────────────────────────────────────────────────────────────

# Build a robust path (works locally + on Connect Cloud)
HERE = Path(__file__).resolve().parent        # src/
ROOT = HERE.parent                            # project root
DATA_PATH = ROOT / "data" / "processed" / "Students-Social-Media-Addiction.parquet"

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Parquet file not found at {DATA_PATH}. "
        "Run prep_data.py first to convert the CSV to parquet."
    )

# ── ibis + DuckDB connection (lazy — no data loaded yet) ──────────────
con = ibis.duckdb.connect()
students = con.read_parquet(str(DATA_PATH))

# ── One-time helper queries for filter components ─────────────────────
# Single aggregation query — pulls min/max values for slider bounds
_meta = students.aggregate(
    age_min=students.Age.min(),
    age_max=students.Age.max(),
    score_min=students.Addicted_Score.min(),
    score_max=students.Addicted_Score.max(),
).execute().iloc[0]

AGE_MIN   = int(_meta["age_min"])
AGE_MAX   = int(_meta["age_max"])
MIN_SCORE = float(_meta["score_min"])
MAX_SCORE = float(_meta["score_max"])

# Distinct values for sidebar dropdowns — queried once at startup
_countries = sorted(students.select(students.Country).distinct().execute()["Country"].tolist())
_platforms = sorted(students.select(students.Most_Used_Platform).distinct().execute()["Most_Used_Platform"].tolist())

# ── LLM setup ────────────────────────────────────────────────────────
load_dotenv()
greeting = "Hello! Welcome to your Social Media Addiction data dashboard. I'm here to help you filter, sort, and analyze the data."
_df_for_qc = students.execute()
qc = QueryChat(_df_for_qc, "df", greeting=greeting, client="anthropic/claude-3-haiku-20240307")


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


.tab-pane[data-value="Chatbot"] .bslib-sidebar-layout {
    height: calc(100vh - 100px) !important;
    max-height: calc(100vh - 100px) !important;
    overflow: hidden !important;
}
.tab-pane[data-value="Chatbot"] .bslib-sidebar-layout > .main {
    overflow-y: auto !important;
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 1.5rem !important;
    padding: 1rem !important;
}
.tab-pane[data-value="Chatbot"] .bslib-sidebar-layout > .main > * {
    flex-shrink: 0 !important;
}
.tab-pane[data-value="Chatbot"] .bslib-sidebar-layout > aside.sidebar {
    height: 100% !important; 
    min-height: 0 !important;
    overflow-y: auto !important; 
}
#reset:hover {
    background-color: #c0392b !important;
    border-color: #c0392b !important;
    color: white !important;
}
#download_csv:hover {
    background-color: #1e3a6e !important;
    border-color: #1e3a6e !important;
    color: white !important;
}
"""

app_ui = ui.page_fluid(

    ui.tags.head(
        ui.tags.link(
            rel="stylesheet",
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
        )
    ),

    ui.head_content(
        ui.tags.style(custom_css)
    ),

    ui.panel_title("Social Media Addiction Dashboard"),
    ui.HTML('<p style="color:#5a5a7a; font-size:13px; margin-top:-10px;">Explore social media usage patterns among students</p>'),

    ui.div(
    ui.HTML('<a href="https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction" target="_blank" style="position:absolute; top:10px; right:20px;"><i class="fa-brands fa-github" style="font-size:1.5rem; color:#1e3a6e;"></i></a>'),
    style="text-align:right; padding:10px;"
    ),

    ui.navset_tab(
        ui.nav_panel("Dashboard",
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
                        inline=False,
                    ),

                    # Filter 2: Age range (slider with two handles)
                    ui.input_slider(
                        id="f_age",
                        label="Age Range",
                        min=AGE_MIN,
                        max=AGE_MAX,
                        value=[AGE_MIN, AGE_MAX],
                    ),

                    # Filter 3: Academic level (single dropdown)
                    ui.input_select(
                        id="f_level",
                        label="Academic Level",
                        choices={"All": "All", "Undergraduate": "Undergraduate", "Graduate": "Graduate"},
                        selected="All",
                    ),

                    # Filter 4: Country (multi-select)
                    ui.input_selectize(
                        id="f_country",
                        label="Country",
                        choices=_countries,
                        multiple=True,
                    ),

                    # Filter 5: Platform (multi-select)
                    ui.input_selectize(
                        id="f_platform",
                        label="Social Media Platform",
                        choices=_platforms,
                        multiple=True,
                    ),


                    open="desktop",
                    bg = "#EEF1F6",
                    fg = "#0F1F3D",
                ),

                # ── MAIN AREA ─────────────────────────────────────────────────
                # Row 1: Summary stat tiles
                ui.layout_columns(
                    ui.value_box( title = "Total Students", 
                                value = ui.output_text("tile_students"),
                                showcase= ui.HTML('<i class="fa-solid fa-graduation-cap" style="font-size:3rem"></i>')
                                ),
                    ui.value_box(title = "Avg Daily Usage", 
                                value = ui.output_text("tile_usage"),
                                showcase = ui.HTML('<i class="fa-solid fa-display" style="font-size:3rem"></i>')
                                ),
                    ui.value_box(title = "Avg Sleep Hours", 
                                value = ui.output_text("tile_sleep"),
                                showcase = ui.HTML('<i class="fa-solid fa-bed" style="font-size:3rem"></i>')
                                ),
                    ui.value_box(title = "Avg Addiction Score", 
                                value = ui.output_text("tile_addiction"),
                                showcase = ui.HTML('<i class="fa-solid fa-circle-exclamation" style="font-size:3rem"></i>')
                                ),
                    fill=False,
                ),

                # Row 2: Four chart placeholders in a 2x2 grid
                ui.layout_columns(

                    ui.card(
                        ui.card_header("Impact on Academic Performance"),
                        output_widget("plot_AAP"),
                        full_screen=True,
                    ),

                    ui.card(
                        ui.card_header("Academic Level"),
                        output_widget("donut_academic_level"),
                        full_screen=True,
                        ),

                    ui.card(
                        ui.card_header("Academic Level Distribution by Gender"),
                        output_widget("plot_academiclvldist"),
                        full_screen=True,
                    ),

                    ui.card(
                        ui.card_header("Social Media Platform Distribution"),
                        output_widget("sunburst_platform"),
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
                        ui.card_header("Average Addiction Score by Country"),
                        ui.HTML(
                            "<p style='padding: 8px; border-radius: 4px; font-size: 0.85rem;'>"
                            "⚠️ This dataset is small and not representative.<br>"
                            "Student counts per country are minimal compared to actual populations — interpret with caution."
                            "</p>"
                        ),
                        output_widget("map_chart"),
                        full_screen=True,
                    ),
                ),
            )
        ),
        ui.nav_panel("Chatbot",
            ui.layout_sidebar(

                qc.sidebar(
                    open="desktop",
                    bg = "#EEF1F6",
                    fg = "#0F1F3D",
                ),
                ui.layout_columns(
                    ui.input_action_button("reset", "Reset Filters"),
                    ui.download_button("download_csv", "Download CSV")
                ),

                # ── MAIN AREA ─────────────────────────────────────────────────
                ui.card(
                    ui.card_header("Filtered Data"),
                    ui.output_data_frame("chat_df"),
                ),

                ui.layout_columns(
                    ui.card(
                        ui.card_header("Impact on Academic Performance"),
                        output_widget("plot_AAP_bot"),
                        full_screen=True,
                    ),
                   
                    ui.card(
                        ui.card_header("Academic Level Distribution by Gender"),
                        output_widget("plot_academiclvldist_bot"),
                        full_screen=True,
                    ),
                ),
                ui.card(
                    ui.card_header("Addiction vs Mental Health & Sleep"),
                    output_widget("scatter_chart_bot"),
                    full_screen=True,
                ),

            )
        )
    ),
)

# ── SERVER ───────────────────────────────────────────────────────────

def server(input, output, session):

    # Close the DuckDB connection when the user's browser session ends (prevents resource leaks on the server)
    session.on_ended(con.disconnect)

    qc_data = qc.server()

    custom_ui_scale = alt.Scale(
        range=['#0F1F3D', '#2D6BE4', '#26f7fd'],
        type='linear'
    )

    # ── Filtered data ─────────────────────────────────────────────────
    # Builds an ibis expression chain and executes once per input change.
    # All filtering happens in DuckDB before any data enters RAM.

    @reactive.calc
    def filtered_df():
        expr = students.filter(students.Academic_Level.isin(["Undergraduate", "Graduate"]))

        if input.f_gender() != "All":
            expr = expr.filter(expr.Gender == input.f_gender())

        age_low, age_high = input.f_age()
        expr = expr.filter(expr.Age.between(age_low, age_high))

        if input.f_level() != "All":
            expr = expr.filter(expr.Academic_Level == input.f_level())

        if input.f_country():
            expr = expr.filter(expr.Country.isin(list(input.f_country())))

        if input.f_platform():
            expr = expr.filter(expr.Most_Used_Platform.isin(list(input.f_platform())))

        # .execute() sends the query to DuckDB — only matching rows enter RAM
        return expr.execute()


    # ── Stat tiles ────────────────────────────────────────────────────

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
                scale=custom_ui_scale
            ),
            tooltip=["Addicted_Score", "Mental_Health_Score", "Sleep_Hours_Per_Night"]
        ).interactive()
        
        return fig

    # ── Map ───────────────────────────────────────────────────────────

    @render_plotly
    def map_chart():
        d = filtered_df().copy()
        
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

        all_iso = [c.alpha_3 for c in pycountry.countries]
        no_data_iso = [iso for iso in all_iso if iso not in df_selected['iso_alpha'].values]

        fig = px.choropleth(
            df_selected,
            locations='iso_alpha',
            locationmode='ISO-3',
            color='Addicted_Score',
            color_continuous_scale=[
                [0.0, '#0F1F3D'],
                [0.3, '#517BD6'],
                [1.0, '#26f7fd']
            ],
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

        fig.add_trace(
            go.Choropleth(
                locations=no_data_iso,
                z=[0] * len(no_data_iso),
                locationmode='ISO-3',
                colorscale=[[0, '#d3d3d3'], [1, '#d3d3d3']],
                showscale=False,
                marker=dict(line=dict(color='black', width=0.5)),
                hovertemplate="<b>%{location}</b><br>No data available<extra></extra>",
            )
        )
        fig.data = fig.data[::-1]

        fig.update_coloraxes(reversescale=True)
        fig.update_geos(fitbounds="locations", showframe=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        
        return fig

    # ── Chart 1: Does social media affect academic performance? ───────

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

    # ── Chart 2: Academic Level ───────────────────────────────

    @render_plotly
    def donut_academic_level():
        d = filtered_df()

        level_counts = (
            d.groupby("Academic_Level")
            .size()
            .reset_index(name="Count")
        )

        total = int(level_counts["Count"].sum()) if len(level_counts) else 0

        if total > 0:
            level_counts["Percentage"] = (level_counts["Count"] / total * 100).astype(str) + "%"
        else:
            level_counts["Percentage"] = []

        fig = px.pie(
            level_counts,
            names="Academic_Level",
            values="Count",
            color="Academic_Level",
            color_discrete_map={
                "Undergraduate": "#1e3a6e",
                "Graduate":      "#5ba4cf",
            },
            hole=0.4,
            custom_data=["Percentage"],
        )

        fig.update_traces(
            textinfo="percent",
            #textposition="outside",
            #automargin=True,
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Students: %{value}<br>"
                #"Percentage: %{percentEntry:.1%}<extra></extra>"
            ),
            textfont=dict(size=10, color="white"),
            domain=dict(x=[0, 0.6]),
        )

        fig.update_layout(
            legend=dict(
                orientation="v",
                x=0.62,
                y=0.5,
                xanchor="left",
                yanchor="middle"
            ),
        )

        return fig

    # ── Chart 3: Academic Level Distribution ─────────────────────────

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

    @render_plotly
    def sunburst_platform():
        d = filtered_df()
        platform_counts = (
            d.groupby(["Gender", "Most_Used_Platform"])
            .agg(Count=("Gender", "size"))
            .reset_index()
        )

        color_map = {"Facebook":  "#1e3a6e",
                    "Instagram": "#2d6be4",
                    "KakaoTalk": "#5ba4cf",
                    "LINE":      "#4f6bed",
                    "LinkedIn":  "#7b8fab",
                    "Snapchat":  "#a8b8cc",
                    "TikTok":    "#0f1f3d",
                    "Twitter":   "#3a5a9e",
                    "VKontakte": "#6d8fc0",
                    "WeChat":    "#b8c8e0",
                    "WhatsApp":  "#d0dff0",
                    "YouTube":   "#bfd4e8",
                    "Other":     "#4a5a6e",
                    "Female":    "#5ba4cf", 
                    "Male":      "#1e3a6e",
                }
        
        # Find top 6 platforms by total count
        top_platforms = (
            platform_counts.groupby("Most_Used_Platform")["Count"]
            .sum()
            .nlargest(6)
            .index
        )

        # Group smaller platforms into "Other"
        platform_counts["Platform_Group"] = platform_counts["Most_Used_Platform"].apply(
            lambda x: x if x in top_platforms else "Other"
        )

        total = int(platform_counts["Count"].sum())
        platform_counts["Percentage"] = (platform_counts["Count"] / total * 100).astype(str) + "%"

        fig = px.sunburst(
            platform_counts,
            path=["Gender","Platform_Group"],
            values="Count",
            color="Platform_Group",
            color_discrete_map=color_map,
            custom_data=["Percentage"],
        )

        fig.update_traces(
            textinfo="label+percent entry",
            insidetextorientation="horizontal",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Students: %{value}<br>"
                "Percentage: %{percentEntry:.1%}<extra></extra>"
            )
        )
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    
        return fig

    # ── Chatbot tab ───────────────────────────────────────────────────

    @render.data_frame
    def chat_df():
        return qc_data.df()

    @render.download(filename="social_media_data.csv")
    def download_csv():
        yield qc_data.df().to_csv(index=False)

    @reactive.effect
    @reactive.event(input.reset)
    def _():
        qc_data.sql.set("")
        qc_data.title.set(None)

    @render_altair
    def plot_AAP_bot():
        df1 = qc_data.df()
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

    # ── Chart 3: Academic Level Distribution ─────────────────────────

    @render_altair
    def plot_academiclvldist_bot():
        df = qc_data.df()

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

    @render_altair
    def scatter_chart_bot():
        d = qc_data.df()
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
                scale=custom_ui_scale
            ),
            tooltip=["Addicted_Score", "Mental_Health_Score", "Sleep_Hours_Per_Night"]
        ).interactive()
        
        return fig


# ── APP ───────────────────────────────────────────────────────────────

app = App(app_ui, server)
