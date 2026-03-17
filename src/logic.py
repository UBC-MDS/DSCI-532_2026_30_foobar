from __future__ import annotations

import pandas as pd
import pycountry


def apply_dashboard_filters(
    df: pd.DataFrame,
    gender: str = "All",
    age_range: tuple[int, int] | list[int] = (0, 100),
    academic_level: str = "All",
    countries: list[str] | None = None,
    platforms: list[str] | None = None,
    clicked_country: str | None = None,
) -> pd.DataFrame:
    """
    Filter the dashboard dataset using the same rules as the app.

    Parameters
    ----------
    df : pd.DataFrame
        Full student dataset.
    gender : str, default="All"
        "All", "Male", or "Female".
    age_range : tuple[int, int] | list[int], default=(0, 100)
        Inclusive min/max age filter.
    academic_level : str, default="All"
        "All", "Undergraduate", or "Graduate".
    countries : list[str] | None, default=None
        Countries selected in the sidebar.
    platforms : list[str] | None, default=None
        Platforms selected in the sidebar.
    clicked_country : str | None, default=None
        Country selected by clicking the map.

    Returns
    -------
    pd.DataFrame
        Filtered dataframe.
    """
    result = df.copy()

    result = result[result["Academic_Level"].isin(["Undergraduate", "Graduate"])]

    if gender != "All":
        result = result[result["Gender"] == gender]

    age_low, age_high = age_range
    result = result[result["Age"].between(age_low, age_high)]

    if academic_level != "All":
        result = result[result["Academic_Level"] == academic_level]

    if countries:
        result = result[result["Country"].isin(countries)]

    if platforms:
        result = result[result["Most_Used_Platform"].isin(platforms)]

    if clicked_country is not None:
        result = result[result["Country"] == clicked_country]

    return result


def summarize_country_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate country-level metrics for the map.

    Returns
    -------
    pd.DataFrame
        One row per country with count and averages.
    """
    if df.empty:
        return pd.DataFrame(
            columns=[
                "Country",
                "Student_ID",
                "Avg_Daily_Usage_Hours",
                "Sleep_Hours_Per_Night",
                "Addicted_Score",
            ]
        )

    return (
        df.groupby("Country", as_index=False)
        .agg(
            Student_ID=("Student_ID", "count"),
            Avg_Daily_Usage_Hours=("Avg_Daily_Usage_Hours", "mean"),
            Sleep_Hours_Per_Night=("Sleep_Hours_Per_Night", "mean"),
            Addicted_Score=("Addicted_Score", "mean"),
        )
    )


def group_platforms_for_sunburst(df: pd.DataFrame, top_n: int = 6) -> pd.DataFrame:
    """
    Keep the top-N platforms and group the rest into 'Other'.

    Returns
    -------
    pd.DataFrame
        Aggregated platform counts by gender with Platform_Group column.
    """
    if df.empty:
        return pd.DataFrame(columns=["Gender", "Most_Used_Platform", "Count", "Platform_Group"])

    platform_counts = (
        df.groupby(["Gender", "Most_Used_Platform"])
        .size()
        .reset_index(name="Count")
    )

    top_platforms = (
        platform_counts.groupby("Most_Used_Platform")["Count"]
        .sum()
        .nlargest(top_n)
        .index
    )

    platform_counts["Platform_Group"] = platform_counts["Most_Used_Platform"].apply(
        lambda x: x if x in top_platforms else "Other"
    )

    return platform_counts


def get_iso3(country_name: str) -> str | None:
    """
    Convert a country name to ISO-3 code for the choropleth map.
    Returns None when the country cannot be matched.
    """
    try:
        return pycountry.countries.search_fuzzy(country_name)[0].alpha_3
    except Exception:
        return None