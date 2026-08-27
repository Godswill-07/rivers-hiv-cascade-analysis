# Rivers State HIV Care Cascade Analysis

An end-to-end data analytics project tracking HIV testing, treatment, and viral suppression outcomes in Rivers State, Nigeria — built on real PEPFAR public health data (2016-2025).

**[View the interactive dashboard →](https://app.powerbi.com/view?r=eyJrIjoiN2VkNGZjOGUtN2Q5Ni00ZTNkLTlhZTgtMzdhZGY4NDI5YjUzIiwidCI6ImVmNDcyYTAzLWQ0ZmQtNDBiMi1hOTBjLTUxMGU3NDg1ZDlmNCJ9" frameborder="0" allowFullScreen="true"></iframe>)** *(add your Power BI published link here)*

![Dashboard Overview](HIV_Dashboard1.png)

---

## The Story

While validating this dataset, I found my "Total Tested" figure came out to **12 million people — in a state with a population of roughly 7 million.** That discrepancy led to uncovering a real data structure issue in PEPFAR's reporting: the same population is reported at multiple overlapping age-band granularities, and summing them together silently double- and triple-counts real people.

This repo documents the full pipeline that found, diagnosed, and corrected that issue — along with several other data quality problems (Excel-corrupted values, precision loss, and structural inconsistencies) — before producing final analysis.

## Key Findings

- **Viral suppression rate rose from 72% (2017) to 96% (2023)**, a sustained multi-year improvement, now plateaued just below the UNAIDS 95% target
- **The steepest cascade drop-off occurs between testing positive and starting treatment** — a linkage gap worth targeted intervention
- **Children (ages 1-14) consistently show lower suppression rates than adults** across the full study period — flagged with an explicit small-sample caveat, not overstated as fact

## Pipeline

| Stage | Tool | What happened |
|---|---|---|
| 1. Data validation | Excel | Caught floating-point ID corruption, scientific-notation precision loss, embedded line breaks |
| 2. Reshaping & cleaning | Python (pandas) | Wide→long reshape, Excel date-corruption recovery for age bands, numerator/denominator suppression rate calculation |
| 3. Modeling & visualization | Power BI | Star schema (fact table + 3 dimension tables), DAX measures, 4-page interactive dashboard |

Full write-up of every data quality issue found and how it was fixed: [`docs/DATA_QUALITY_LOG.md`](docs/DATA_QUALITY_LOG.md)

## Repository Structure

```
rivers-hiv-cascade-analysis/
├── data/
│   ├── raw/              # Original PEPFAR MER export (not included — see Data Access below)
│   └── cleaned/          # Final cleaned dataset used in the dashboard
├── notebooks/
│   └── cleaning_pipeline.py   # Full Python cleaning pipeline, documented step by step
├── powerbi/
│   ├── theme.json         # Custom Power BI theme
│   └── dax_measures.md    # All DAX measures with explanations
├── docs/
│   ├── DATA_QUALITY_LOG.md    # Every data issue found and how it was corrected
│   └── METHODOLOGY.md         # Cascade definitions, indicator mapping, known limitations
├── images/                # Dashboard screenshots
└── README.md
```

## Data Access

This project uses PEPFAR's public **Monitoring, Evaluation, and Reporting (MER) Clinical Cascade dataset**, filtered to Rivers State, Nigeria.

- Source: [data.pepfar.gov/datasets](https://data.pepfar.gov/datasets)
- Dataset used: "Clinical Cascade Results by Fine Age and Sex"
- License: Public domain, U.S. Government data

Raw data is not included in this repo due to file size — download instructions are in `data/raw/README.md`.

## Tech Stack

`Python (pandas)` · `Microsoft Excel` · `Power BI` · `DAX` · `Power Query`

## Known Limitations

- 2016-2017 have thin reporting density (fewer than 20 data points per quarter)
- 2025 includes Q4 results only, per PEPFAR's own data release guidance
- TX_RET (standard retention indicator) is not present in current MER guidance; TX_CURR and TX_NET_NEW are used as proxies
- Full limitations documented in [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)

## About Me

Built by **Godswill Ndukachukwu Douglas** — Data Analyst, Microsoft PL-300 certified.
[LinkedIn](#) · [Portfolio](#)
