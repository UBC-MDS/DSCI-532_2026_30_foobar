### 1 Updated Job Stories

| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | When I am a wellness coordinator, I want to filter and compare addiction scores across demographic groups so I can identify which student populations are most at risk and prioritize them for targeted intervention. | ✅ Implemented |                               |
| 2   | When I am a wellness coordinator, I want to visualize the relationship between addiction scores and key outcome variables. In a single view I want to look at sleep duration, mental health scores, and academic performance so I can build a comprehensive case for why digital well-being programs. |   ✅ Implemented  | |
| 3   | When I am a wellness coordinator, I want to compare average addiction scores across different social media platforms so I can determine whether certain platforms warrant platform-specific awareness messaging in my campaigns. | ✅ Implemented |                               |
| 4   | When I am a wellness coordinator, I want to identify countries whose student populations show addiction profiles similar to my university’s so I can research the intervention strategies their universities are using and adapt best practices for my own institution. | ✅ Implemented |

### 2 Component Inventory

| ID            | Type          | Shiny widget / renderer | Depends on                   | Job story  |
| ------------- | ------------- | ----------------------- | ---------------------------- | ---------- |
| `f_gender`| Input         | `ui.input_radio_buttons()`     | —                            |   1  |
| `f_age`   | Input         | `ui.input_slider()`     | —                            |  1  |
| `f_academiclvl`  | Input   | `ui.input_select()`     | —                            |  1   |
| `f_country`  | Input         | `ui.input_selectize()`     | —                            |  4   |
| `f_platform`  | Input         | `ui.input_selectize()`     | —                            |  3  |
| `filtered_df` | Reactive calc | `@reactive.calc`        | `f_gender`, `f_age`, `f_country`, `f_academiclvl`, `f_platform` | 1,2,3,4 | 
| `plot_AAP`  | Output        | `@render_altair`          | `filtered_df`                |    2     |
| `donut_academic_level`  | Output        | `@render_altair`          | `filtered_df`                |     1    |
| `plot_platformdist`  | Output        | `@render_altair`          | `filtered_df`                |     3    |
| `donut_platform`  | Output        | `@render_altair`          | `filtered_df`                |    1     |
| `tile_students`  | Output        | `@render_altair`          | `filtered_df`                |     1    |
| `tile_usage`  | Output        | `@render_altair`          | `filtered_df`                |    2     |
| `tile_sleep`  | Output        | `@render_altair`          | `filtered_df`                |     2    |
| `tile_addiction`  | Output        | `@render_altair`          | `filtered_df`                |    1,2,3,4     |
| `scatter_chart`  | Output        | `@render_altair`          | `filtered_df`                |    2     |
| `get_iso3`  | Output        | `@render_widget`          | `filtered_df`                |    4     |

### 3 Reactivity Diagram
- `[/Input/]` (Parallelogram) (or `[Input]` Rectangle) = reactive input
- Hexagon `{{Name}}` = `@reactive.calc` expression
- Stadium `([Name])` (or Circle) = rendered output

Example:

```mermaid
flowchart TD
  A[/f_gender/] --> F{{filtered_df}}
  B[/f_age/] --> F
  C[/f_academiclvl/] --> F
  D[/f_country/] --> F
  E[/f_platform/] --> F
  F --> P1([plot_AAP])
  F --> P2([donut_academic_level])
  F --> P3([plot_platformdist])
  F --> P4([donut_platform])
  F --> P5([tile_students])
  F --> P6([tile_usage])
  F --> P7([tile_sleep])
  F --> P8([tile_addiction])
  F --> P9([scatter_chart])
  F --> P10([get_iso3])
```

### 4 Calculation Details

For each `@reactive.calc` in your diagram, briefly describe:

`filered_df` depends on all five inputs (`f_gender`, `f_age`, `f_academiclvl`, `f_country`, `f_platform`). Then `@reactive.calc` dynamically filters rows based on the selected inputs the user provided with each input acts as an optional filter. For instance, `f_gender` and `f_academiclvl` inputs are provided, it filters rows based on the selected gender and academic level(s). All outputs consumes it and recompute in reponse to the changes in `filtered_df`.
