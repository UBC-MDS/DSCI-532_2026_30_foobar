# Changelog

All notable changes to this project will be documented in this file.

---

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