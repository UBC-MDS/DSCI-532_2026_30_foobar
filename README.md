# Social Media Addiction Analytics Dashboard

### Project Summary

This project presents an interactive data visualization dashboard designed to explore patterns in social media usage and addiction among students. The dashboard allows users to explore the correlation between daily usage hours, sleep duration, mental health scores, academic performance, and preferred platforms.

The dashboard is intended for school administrators, counselors, and students seeking to better understand digital behavior and its impact on well-being and academic outcomes. Through interactive filtering and comparative visualizations, users can potentially identify high-risk groups and conduct targeted interventions or self regulation making based on this.

### Demo

![Dashboard Demo](img/demo.gif)

### Setup
First, clone the repository and navigate into the project directory:

```bash
git clone git@github.com:UBC-MDS/DSCI-532_2026_30_social-media-addiction.git
cd DSCI-532_2026_30_social-media-addiction/
```

Then install the development environment:

```bash
conda env create -f environment.yml
conda activate 532
```

Run the below command to download the dataset:

```bash
python src/download_data.py
```
To run the shiny app locally, navigate and run shiny with the following command:
```bash
cd src/
shiny run app.py
```
You will be able to access the app at the link displayed in the command line.

### Live App

#### Stable (main): 
https://019ca108-2c5a-f4a9-1093-cdd4a540d77d.share.connect.posit.cloud/

#### Preview (dev): 
https://019ca127-fdc0-0c6d-1031-e1462c7abb05.share.connect.posit.cloud/

### Contributing

Interested in contributing? Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on filing issues, branch naming, code style (PEP8), and the pull request review process.

## Team Members

- Yin Tiantong  
- Lee Wai Yan  
- Ssemakula Peter Wasswa  
- Fontelera Roganci  
