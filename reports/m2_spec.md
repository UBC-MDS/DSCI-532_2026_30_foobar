### 1 Updated Job Stories

| \# | Job Story | Status | Notes |
|----------------|---------------------|----------------|-------------------|
| 1 | When I am a wellness coordinator, I want to filter and compare addiction scores across demographic groups so I can identify which student populations are most at risk and prioritize them for targeted intervention. | ✅ Implemented |  |
| 2 | When I am a wellness coordinator, I want to visualize the relationship between addiction scores and key outcome variables. In a single view I want to look at sleep duration, mental health scores, and academic performance so I can build a comprehensive case for why digital well-being programs. | ✅ Implemented |  |
| 3 | When I am a wellness coordinator, I want to compare average addiction scores across different social media platforms so I can determine whether certain platforms warrant platform-specific awareness messaging in my campaigns. | ✅ Implemented |  |
| 4 | When I am a wellness coordinator, I want to identify countries whose student populations show addiction profiles similar to my university’s so I can research the intervention strategies their universities are using and adapt best practices for my own institution. | ✅ Implemented (partial) | The functionality is implimented, but the data we currently have is not sufficient to achieve this goal.  |

### 2 Component Inventory

| ID | Type | Shiny widget / renderer | Depends on | Job story |
|---------------|---------------|---------------|---------------|---------------|
| `f_gender` | Input | `ui.input_radio_buttons()` | — | 1 |
| `f_age` | Input | `ui.input_slider()` | — | 1 |
| `f_academiclvl` | Input | `ui.input_select()` | — | 1 |
| `f_country` | Input | `ui.input_selectize()` | — | 4 |
| `f_platform` | Input | `ui.input_selectize()` | — | 3 |
| `qc_sidebar` | Input/Output | `qc_sidebar()` | — | 1,2,3,4 |
| `reset` | Input | `ui.input_action_button()` | — | — |
| `filtered_df` | Reactive calc | `@reactive.calc` | `f_gender`, `f_age`, `f_country`, `f_academiclvl`, `f_platform` | 1,2,3,4 |
| `qc_data` | Reactive component via querychat | `qc.server()` | `qc_sidebar` | 1,2,3,4 |
| `chat_df` | Output | `@render.data_frame` | `qc_data` | 1,2,3,4 |
| `plot_AAP_bot` | Output | `@render_altair` | `qc_data` | 2 |
| `plot_academiclvldist_bot` | Output | `@render_altair` | `qc_data` | 1 |
| `scatter_chart_bot` | Output | `@render_altair` | `qc_data` | 2 |
| `download_csv` | Output | `@render.download` | `qc_data` | 1,2,3,4 |
| `plot_AAP` | Output | `@render_altair` | `filtered_df` | 2 |
| `donut_academic_level` | Output | `@render_plotly` | `filtered_df` | 1 |
| `plot_platformdist` | Output | `@render_altair` | `filtered_df` | 3 |
| `sunburst_platform` | Output | `@render_plotly` | `filtered_df` | 1 |
| `tile_students` | Output | `@render_altair` | `filtered_df` | 1 |
| `tile_usage` | Output | `@render_altair` | `filtered_df` | 2 |
| `tile_sleep` | Output | `@render_altair` | `filtered_df` | 2 |
| `tile_addiction` | Output | `@render_altair` | `filtered_df` | 1,2,3,4 |
| `scatter_chart` | Output | `@render_altair` | `filtered_df` | 2 |
| `map_chart` | Input/Output | `@render_plotly` | `filtered_df` | 4 |

### 3 Reactivity Diagram

-   `[/Input/]` (Parallelogram) (or `[Input]` Rectangle) = reactive input

-   Hexagon `{{Name}}` = `@reactive.calc` expression

-   Stadium `([Name])` (or Circle) = rendered output

``` mermaid
flowchart TD
  A[/f_gender/] --> F{{filtered_df}}
  B[/f_age/] --> F
  C[/f_academiclvl/] --> F
  D[/f_country/] --> F
  E[/f_platform/] --> F
  P10i[/map_chart/] --> F
  F --> P1([plot_AAP])
  F --> P2([donut_academic_level])
  F --> P3([plot_platformdist])
  F --> P4([donut_platform])
  F --> P5([tile_students])
  F --> P6([tile_usage])
  F --> P7([tile_sleep])
  F --> P8([tile_addiction])
  F --> P9([scatter_chart])
  F --> P10([map_chart])
```

``` mermaid
flowchart TD
  G[/qc_sidebar/] --> I{{qc_data}}
  H[/reset/] --> I
  I --> J1([chat_df])
  I --> J2([plot_AAP_bot])
  I --> J3([plot_academiclvldist_bot])
  I --> J4([scatter_chart_bot])
  I --> J5([download_csv])
```

### 4 Calculation Details

For each `@reactive.calc` in your diagram, briefly describe:

`filered_df` depends on all five inputs (`f_gender`, `f_age`, `f_academiclvl`, `f_country`, `f_platform`). Then `@reactive.calc` dynamically filters rows based on the selected inputs the user provided with each input acts as an optional filter. For instance, `f_gender` and `f_academiclvl` inputs are provided, it filters rows based on the selected gender and academic level(s). All outputs consumes it and recompute in reponse to the changes in `filtered_df`.

`qc_data` depends on both the chat box component `qc_sidebar` and the reset button `reset`. It contains the filtered data returned by querychat when the chat box executes a filter, and `reset` sets it to the full dataset. All outputs use it to display the data, and `download_csv` saves `qc_data` as a csv file named `social_media_data.csv`.

### 5 Addressed Feedbacks
A list of addressed feedbacks and a bief discription of each can be found below.
- [CRITICAL] Filter combinations resulting in no results will result in empty plots, which might look like they are broken. They now have a fallback state stating there are no data avaliable.
- [CRITICAL] The map highlight all countries as equals, while some countries have too few data to be representitive of the addition level of the country. We added a disclaimer stating due to the lack of data please interpret the map with caution.
- [CRITICAL] Our current name for our conda environemnt (`532`) is too generic and may cause conflicts for other users. We renamed it to `532-social-media-addiction` to be specific to our project.
- [CRITICAL] Given the limited data some of our original job story are not really achieveable. We have changed the status of that job story to be partially compleated, adding a statement that while the functionality is implimented, we need more data to sufficiently support this task.
- [Non-critical] Our `dev` branch allows merging without review, and the PRs are not linked to their respective issues. We have changed the branch protextion rules for the `dev` branch and we will keep this feedback in mind when proceeding to milestone 4.
