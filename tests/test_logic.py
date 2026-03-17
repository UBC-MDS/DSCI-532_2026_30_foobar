import pandas as pd

from src.logic import (
    apply_dashboard_filters,
    summarize_country_metrics,
    group_platforms_for_sunburst,
    get_iso3,
)


def make_test_df():
    return pd.DataFrame(
        {
            "Student_ID": [1, 2, 3, 4, 5, 6],
            "Gender": ["Male", "Female", "Male", "Female", "Male", "Female"],
            "Age": [18, 19, 20, 21, 22, 23],
            "Academic_Level": [
                "Undergraduate",
                "Graduate",
                "Undergraduate",
                "Graduate",
                "Undergraduate",
                "Graduate",
            ],
            "Country": ["Canada", "Canada", "USA", "USA", "India", "India"],
            "Most_Used_Platform": [
                "Instagram",
                "TikTok",
                "Instagram",
                "YouTube",
                "WhatsApp",
                "Snapchat",
            ],
            "Avg_Daily_Usage_Hours": [4.0, 5.0, 6.0, 3.0, 2.0, 7.0],
            "Sleep_Hours_Per_Night": [7.0, 6.0, 5.0, 8.0, 7.5, 4.5],
            "Addicted_Score": [6, 7, 8, 4, 3, 9],
            "Mental_Health_Score": [5, 6, 4, 7, 8, 3],
            "Affects_Academic_Performance": ["Yes", "Yes", "No", "No", "No", "Yes"],
        }
    )


def test_apply_dashboard_filters_combines_sidebar_filters_correctly():
    """This test verifies that multiple sidebar filters work together so the dashboard does not show rows outside the user's selected slice."""
    df = make_test_df()

    result = apply_dashboard_filters(
        df,
        gender="Male",
        age_range=(18, 20),
        academic_level="Undergraduate",
        countries=["Canada", "USA"],
        platforms=["Instagram"],
    )

    assert len(result) == 2
    assert set(result["Student_ID"]) == {1, 3}


def test_apply_dashboard_filters_clicked_country_overrides_to_single_country():
    """This test verifies that a clicked map country is applied as an additional filter because map interaction is a core dashboard control."""
    df = make_test_df()

    result = apply_dashboard_filters(
        df,
        gender="All",
        age_range=(18, 23),
        academic_level="All",
        clicked_country="India",
    )

    assert len(result) == 2
    assert set(result["Country"]) == {"India"}


def test_summarize_country_metrics_returns_expected_counts_and_means():
    """This test verifies country aggregation correctness so the choropleth uses accurate counts and averages."""
    df = make_test_df()

    summary = summarize_country_metrics(df).sort_values("Country").reset_index(drop=True)

    canada = summary[summary["Country"] == "Canada"].iloc[0]
    usa = summary[summary["Country"] == "USA"].iloc[0]

    assert canada["Student_ID"] == 2
    assert round(canada["Avg_Daily_Usage_Hours"], 2) == 4.5
    assert round(canada["Addicted_Score"], 2) == 6.5

    assert usa["Student_ID"] == 2
    assert round(usa["Sleep_Hours_Per_Night"], 2) == 6.5


def test_group_platforms_for_sunburst_groups_small_categories_into_other():
    """This test verifies that low-frequency platforms are collapsed into 'Other' so the sunburst remains readable and stable."""
    df = make_test_df()

    grouped = group_platforms_for_sunburst(df, top_n=2)

    assert "Platform_Group" in grouped.columns
    assert "Other" in set(grouped["Platform_Group"])


def test_get_iso3_returns_none_for_unknown_country():
    """This test verifies boundary handling for unmapped country names so the map logic fails safely instead of crashing."""
    assert get_iso3("NotARealCountry") is None