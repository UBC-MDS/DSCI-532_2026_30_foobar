# Changelog

All notable changes to this project will be documented in this file.

---

## [0.4.0] - 2026-03-16

### Added

- Implemented Parquet + DuckDB Integration, switched data loading to .parquet format using ibis for database-level filtering [PR](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/issues/62)
	- Replaced eager pd.read_csv() data loading with a lazy loading stack using parquet, DuckDB, and ibis
	- Created prep_data.py to convert the raw CSV to parquet format as a one-time step
	- Rewrote filtered_df() so all filtering happens in DuckDB before any data enters RAM.
	- Added DuckDB connection cleanup on session end to prevent resource leaks
	- Error Fixed: resolved Affects_Academic_Performance boolean/string mismatch introduced by parquet conversion
	- Updated requirements and environment.yml for duckdb/ibis package
- Implemented Playwright behavioural tests and pytest unit test for core filtering logic [PR](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/pull/82)
- Implemented Option D: Component click event interaction to the map [PR](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/pull/75)

### Changed

- Added a prominent disclaimer regarding limited sample sizes in the map view to prevent misleading interpretations [PR](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/pull/70)
- Updated App Specification to reflect AI implementation from M3 and added advanced feature from M4 [PR](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/pull/76)
- Updated via contributing.md with the M3 retrospective and established M4 collaboration norms [issue](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/issues/65), [PR](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/pull/71)
- Updated the conda environment name from 532 to 532-social-media-addiction to avoid local naming conflicts [PR](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/pull/79)
- Updated "No data available" messaging for all charts to handle empty filter combinations [PR](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/pull/84)

### Fixed

- **Feedback prioritization issue link:** [#67](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/issues/67)

### Known Issues

- **Sunburst chart label visibility**: Plotly's sunburst chart does not support placing labels outside of segments. This is a known library limitation rather than a design oversight.

### Release Highlight: Component click event interaction

We implemented an interactive map that allows users to filter the country by clicking on the map. When a user clicks on a country on the map, the dashboard updates all visualizations to reflect only the data from that selected country. This allows users to explore social media addiction patterns without the risk of selecting a country with no available data.

- **Option chosen:** D
- **PR:** [#75](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/pull/75)
- **Why this option over the others:** We chose this option over others because our M3 feedback highlighted issues with empty data states and misleading geographic scales. By making the map charts interactive filters, we reduce the risk of users selecting invalid data combinations and can provide targeted disclaimers for specific countries when they are clicked.
- **Feature prioritization issue link:** [#73](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/issues/73)

### Collaboration

- **CONTRIBUTING.md:** [#71](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/pull/71)
- **M3 retrospective:** PRs were occasionally merged without review approval, feature branches were not consistently deleted after merging, and branched sometimes drifted from main branch with unrelated commits accumulated over time. These gaps made codebase harder to manage cleanly,
- **M4:** We aimed to improve our workflow by adding branch protection rule so no PR merges without at least one teammate review approval regardless of the size of LoC. We start to tag specific reviewer(s) when opening PRs and tried avoid PRs to stay open for too long to prevent dirty merges. Cleaned up unused branch other they are merged to main.

### Reflection

#### **Test Plan**

Test Function | Test Type | Behaviour verified | What breaks if it changes |
|------|------|--------|-------------------|--------------------------|
| `test_apply_dashboard_filters_combines_sidebar_filters_correctly` | unit test | Multiple sidebar filters correctly narrow the dataset | Dashboard may show incorrect subsets of students |
| `test_apply_dashboard_filters_clicked_country_overrides_to_single_country` | unit test | Clicking a country on the map correctly filters the dataset| Map interaction stops affecting dashboard results|
| `test_summarize_country_metrics_returns_expected_counts_and_means` | unit test | Country-level aggregation produces correct counts and averages |Choropleth map statistics become incorrect |
| `test_group_platforms_for_sunburst_groups_small_categories_into_other`| unit test | Low-frequency platforms are grouped into "Other" | Sunburst visualization becomes cluttered or misleading |
| `test_get_iso3_returns_none_for_unknown_country` | unit test | Handles unknown country names and return None | Map rendering could crash when ISO codes cannot be resolved |
| `test_dashboard_loads_and_shows_initial_clicked_country` | Playwright end-to-end tests |Dashboard loads and starts with no clicked-country filter | Initial app state or reactive outputs may fail |
| `test_gender_filter_changes_total_students_tile` | Playwright end-to-end tests | Changing the gender filter updates KPI outputs| Filter reactivity breaks|
| `test_academic_level_filter_changes_total_students_tile` | Playwright end-to-end tests |Changing academic level updates KPI values |Aggregations stop reflecting filter state |
| `test_country_filter_changes_total_students_tile` | Playwright end-to-end tests |Selecting a country updates dashboard totals | Country filtering stops affecting results |



Our dashboard presents a clean, well-organized layout that guides users through the data in a logical way. It allows the user to explore the relationship between students (specifically undergraduate and graduate students) and social media usage, mental health, sleep, and academic performance. Starting from the top of the dashboard, summarized statistics are presented for quick overview, and support any granular exploration across many countries and platforms. Then various charts are presented for a more detailed analysis. Current limitations is the size of the dataset. Our dataset is relatively small and the charts generated may not generalized broadly so user needs to proceed with caution. Additionally, with current limitation on Plotly sunburst labels layout, we are unable to fix the tiny labels on the chart. However, if user hover on top of the each section of the chart, they will be able to see the details. 

**Trade-offs**: We prioritized implementing clickable components over AI-enchancements due to the dashboard feedback. Please click [here](https://github.com/UBC-MDS/DSCI-532_2026_30_social-media-addiction/issues/73) for details.

**Most useful**: Peers, TA, and instructor feedback was the most influential input throughout this project. They were helpful in surfacing edge cases and usability gaps we hadn't initially considered which helped us improve our dashboard. While not all feedback was implemented, every point raised was valid and worth considering when building our own dashboards in the future. The feedback also shaped our decision to implement click event interactions and other decisions in earlier milestones. One area we wish had been covered more is dashboard design (CSS, colour selection, layout principles, and effective use of headers). They may seem like small details in a bigger picture but when done effectively, they can change the entire user experience. Moreover, we wish that this course had covered more in Plotly charts and maps as we were used to Altair but Plotly is more flexible.

## [0.3.0] - 2026-03-07

### Added
- AI-powered chatbot tab with querychat interface for filtering and interacting with the dataset
- Dataframe output component on the AI tab displaying the querychat-filtered results
- Interactive plot visualization on the AI tab using the querychat-filtered dataframe
- Data download button to export the filtered dataframe as a CSV
- `dotenv`, `querychat`, and related dependencies to `environment.yml` and `requirements.txt`
- Black border and tooltip on the choropleth map for countries with no data, so boundaries are still visible
- Subtitle to the dashboard
- Clickable GitHub icon in the upper-right corner of the dashboard
- Icons for the summary statistic cards
- Percentage labels to the Academic Level donut chart

### Changed
- Replaced Social Media Platform Distribution donut chart with a sunburst chart; top 6 platforms are labelled individually and remaining platforms are collapsed into "Other"
- Gender radio buttons are now aligned vertically
- Filter label renamed: "Platform" → "Social Media Platform"
- Chart titles updated: "Avg Addiction Score by Country" → "Average Addiction Score by Country", "Affects on Academic Performance" → "Impact on Academic Performance"
- Updated `m2_spec.md`: renamed `donut_platform` → `sunburst_platform` and corrected renderer references
- Fixed CSS compatibility issues with Chrome

### Fixed
- Countries with no data now render with a visible boundary on the map instead of being invisible

### Deployment
- Application redeployed on Connect Cloud with environment variables configured for the AI/querychat component


## [0.2.0] - 2026-02-28

### Added
- `f_gender` radio button filter for demographic filtering (Job Story 1)
- `f_age` slider filter for age range selection (Job Story 1)
- `f_academiclvl` dropdown filter for academic level (Job Story 1)
- `f_country` selectize input for country-based filtering (Job Story 4)
- `f_platform` selectize input for platform-based filtering (Job Story 3)
- `filtered_df` reactive calculation that applies all five filters dynamically; each filter is optional and composes with the others
- `plot_AAP` Altair chart visualizing addiction scores against academic performance (Job Story 2)
- `donut_academic_level` donut chart breaking down students by academic level (Job Story 1)
- `plot_platformdist` bar chart comparing addiction scores across social media platforms (Job Story 3)
- `donut_platform` donut chart showing platform distribution among filtered students (Job Story 1)
- `tile_students`, `tile_usage`, `tile_sleep`, `tile_addiction` summary metric tiles (Job Stories 1, 2)
- `scatter_chart` scatter plot relating addiction score to sleep duration and mental health (Job Story 2)
- `get_iso3` interactive choropleth map widget highlighting countries with similar addiction profiles (Job Story 4)

### Changed
- Dashboard layout updated to incorporate the new map component (`get_iso3`) for geographic comparison, which was not present in the M1 sketch; the spec component inventory has been updated to reflect this addition under `get_iso3`.

### Fixed
- No bug fixes in this milestone.

### Known Issues
- Color scheme for the pie chart has to be reviewed

---

### Reflection

**Job Story Implementation Status**

All four job stories defined in the M2 spec are fully implemented in this milestone. Job Story 1 (filter and compare addiction scores across demographics) is covered by the five filter inputs and the donut/tile outputs. Job Story 2 (visualize addiction vs. sleep, mental health, and academic performance) is addressed by `plot_AAP`, `scatter_chart`, and the metric tiles. Job Story 3 (compare scores across platforms) is handled by `plot_platformdist` and `donut_platform`. Job Story 4 (identify countries with similar profiles) is fulfilled by `get_iso3`. Additional work on theme is deferred to M3.

**Layout on M2 Spec vs M1 Sketch**

The final layout is largely consistent with the M2 spec. The one meaningful departure from both the M1 sketch and the original spec was the addition of the interactive choropleth map (`get_iso3`) as a dedicated output component for Job Story 4. The M1 sketch had only implied a tabular or list-based country comparison; the map provides a richer spatial view of similar-profile countries. The component inventory in the spec has been updated above to reflect this. All other panels — filters sidebar, metric tiles row, and the chart grid — match the spec as written.