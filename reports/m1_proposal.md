# Proposal Examples

These examples are provided to help you understand the expected depth and style of your proposal. You do not need to follow them exactly, but your sections should cover similar ground. Use the lecture materials to better motivate your proposal.

## Section 1: Motivation and Purpose

> **Our role:** Data scientists. We translate survey responses into meaningful insights that support student well-being.
>
> **Target audience:** School administrators, counselors, undergraduate students, and graduate students who are affected by or responsible for understanding social medis addicition among students.

> It is no suprise that social media is apart of most people's life, especially undergraduate and graduate students, but how much is too much and how does it affect their well-being and grades? Many undergraduate and graduate students don't realize how the use of social media might affect their mental state and/or academic performance. While students may be struggling with the effect of social media use, school administrators and counselors also need a clear way to explore this information so they can understand what's happening and offer support accordingly. To address this challenge, we propose building a data visualization app that helps our target audience explore patterns/relationships across academic performance, sleep hours, daily social media usage, country, and most used platforms. This allow students to reflect on their own habits while giving school administrators and counselors a clearer picture of which groups may need additional support.

## Section 2: Description of the Data

> We will be visualizing a dataset of approximately 300,000 missed patient appointments. Each appointment has 15 associated variables that describe the following characteristics, which we hypothesize could be helpful in determining why patient's miss their appointments:
>
> - Patient demographics (`patient_id`, `gender`, `age`, etc)
> - The health status of the patient (`general_health_status`, `existing_conditions` e.g. "Hypertension", "Physical disability")
> - Information about the appointment itself (`appointment_id`, `appointment_date`)
>
> Using this data we will also derive new variables, such as the time since the patient's last appointment (`days_since_last_appointment`) and which weekday the appointment was on (`appointment_weekday`), as it would be interesting to explore if these could be linked to the patient missing their appointment.

## Section 3: Research Questions & Usage Scenarios

### Usage Scenario
> Mary is a policy maker with the Canadian Ministry of Health and she wants to understand what factors lead to missed appointments in order to devise an intervention that improves attendance numbers. She wants to be able to [explore] a dataset in order to [compare] the effect of different variables on absenteeism and [identify] the most relevant variables around which to frame her intervention policy.
>
> When Mary logs on to our "Missed Appointments app", she will see an overview of all the available variables in her dataset, according to the number of people that did or did not show up to their medical appointment. She can filter out variables for head-to-head comparisons, and explore which variables are most important in determining whether a patient will show up to their appointment. When she does so, Mary may e.g. notice that "physical disability" appears to be a strong predictor missing appointments, and in fact patients with a physical disability also have the largest number of missed appointments.
>
> Based on her findings from using our app, Mary hypothesizes that patients with a physical disability could be having a hard time finding transportation to their appointments, and decides she needs to conduct a follow-on study since transportation information is not captured in her current dataset.

### User Stories
*You can choose to frame your detailed requirements as User Stories...*

> **User Story 1:**
> As a **policy maker**, I want to **filter appointments by specific demographics (e.g., age, gender)** in order to **determine if specific population groups are disproportionately missing appointments**.
>
> **User Story 2:**
> As a **policy maker**, I want to **compare no-show rates between patients with and without specific conditions (e.g., hypertension)** in order to **identify if medical conditions are high-risk factors**.
>
> **User Story 3:**
> As a **policy maker**, I want to **visualize no-shows across days of the week** in order to **decide if specific days need scheduling interventions**.

### Jobs to Be Done
*...or as Jobs to Be Done:*

> **JTBD 1:**
> **Situation:** When I am reviewing monthly attendance reports...
> **Motivation:** ...I want to separate routine absences from systemic issues...
> **Outcome:** ...so I can allocate intervention budget to the right patient groups.
>
> **JTBD 2:**
> **Situation:** When investigating a spike in no-shows...
> **Motivation:** ...I want to see if specific physical disabilities correlate with absenteeism...
> **Outcome:** ...so I can propose targeted transportation support services.
>
> **JTBD 3:**
> **Situation:** When planning clinic hours...
> **Motivation:** ...I want to see if appointments on Mondays or Fridays are missed more often...
> **Outcome:** ...so I can optimize the scheduling grid.

## Section 4: Exploratory Data Analysis

> *To address User Story 1 (Demographics), we analyzed the no-show rate across different age groups.*
>
> **Analysis:** The bar chart in `notebooks/eda_analysis.ipynb` reveals that patients in the 20-30 age bracket have a 15% higher no-show rate than the average.
>
> **Reflection:** This finding supports the need for a targeted filter in the dashboard. By allowing the policy maker to isolate "Young Adults," they can investigate if this high trend holds true across different clinic locations, helping them decide if age-specific text message reminders are needed.

## Section 5: App Sketch & Description

![Dashboard Sketch](../img/dash_sketch.png "App Sketch")

> The dashboard contains a landing page that shows the key summary metrics at the top such as total students, average daily usage, average sleep hours, average addiction score, and most-used platform. This gives users an immediate overview of the dataset. On the left side, an "About" section is included to explain the purpose of the dashboard. Directly below it, an interactive filter panel allows users to refine the display by selecting specific social media platforms, adjusting age ranges, gender, academic level, or country. All charts on the page update dynamically as the filters are modified. The main interface displays a series of visual components, including bar chats, pie charts, histograms, and scatter plots that show academic impact, sleeping distribution, the relationship between addictive and mental health scores with sleep hours, and the relationship between mental health score and conflicts over social media with family, friends, or partners. Users can compare patterns/distributions across wellbeing indicators and usage behaviour by scrolling down through the app interface. 
>
>**Disclaimer:** At least eight components will be implemented with the possibility of adding more if we have capacity to build more features. 
