# B2B Cohort Analysis & Lead Generation
End-to-end B2B analytics project for customer cohort segmentation, product recommendation modeling, lead scoring and sales dashboarding.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-green)

## Executive Summary
This project simulates a realistic B2B sales environment and builds a complete analytics pipeline that transforms raw customer, product, sales, and Salesforce activity data into actionable sales intelligence. The final output enables sales teams to understand customer cohorts, identify cross-sell opportunities, prioritize leads, and monitor commercial performance through dashboard-ready outputs.

## Business Context

### Industry
THe project is based on a synthetic B2B company that sells industrial, safety, automation, maintenance, and service-related products to business customers across multiple European regions. 

### Business Challenge
B2B sales teams often manage large customer portfolios with limited time and incomplete visibility into customer behavior. Without a structured analytical approach, it is difficult to know: 
- whioch customers should be prioritized 
- which customers are at risk of inactivity
- which product categories are suitable for cross-sell
- which customer cohorts require different commercial actions

### Stakeholders
- Sales managers
- Account executives
- Customer success teams
- Marketing and campaign managers
- Business intelligence teams
- Commercial leadership

### Business Objectives
- Segment customers into meaningful behavioural cohorts
- Identify product recommendation opportunities
- Prioritize customers using a transparent lead score
- Provide dashboard visuals for executive and sales-team decision making
- Build a reproducible analytics workflow suitable for a portfolio 

## Problem Statement 
The business needs a data-driven way to priroitize sales outreach and recommend relevant product categories to cstomers. The challenge is to combine historical sales behavior, customer activity, product coverage, Salesforce engagement and customer value into a clear lead generation framework.

## Dataset
The dataset is fully synthetic and does not contain real customer data, personal data or confidential company data. It was generated to resemble a realistic B2B commercial dataset.

### Source Tables
| Table | Description |
|---|---|
| `df_fact_sales` | Transaction-level monthly sales data by customer and product|
| `df_dim_customer` | Customer dimension table with segment, size, industry, country and acquisition channel |
| `df_dim_product` | Product dimension table with product hierarchy and unit price|
| `df_fact_sf` | Salesforce activity table with activity count, selling time, activity type, sales rep and opportunity stage|

### Data Dictionary

## Data Quality Assessment
The project includes a structured data quality workflow before feature engineering and modeling. 
- Missing values identified and handled
- Duplicare records checked
- Customer and product ID consistency validated
- Invalid dates converted and reviewed
- Negative sales and unit values checked
- Data types standardized
- Product hierarchy cardinality reviewed
- Feature distributions reviewed before clustering

## Technology Stack
- Python
- pandas
- NumPy
- scikit-learn
- matplotlib
- Random Forest
- Logistic Regression
- Kmeans
- Agglomerative Clustering
- PCA
- Excel / openpyxl
- Power BI for dashboarding
- Jupyter Notebook for exploration

## Architecture
```mermaid
flowchart TD
    A["Synthetic Data Generation"] --> B["Data Cleaning"]
    B --> C["Data Quality Assessment"]
    C --> D["Feature Engineering"]
    D --> E["Cohort Clustering"]
    E --> F["Product Recommendation Modeling"]
    F --> G["Lead Scoring"]
    G --> H["Dashboard Development"]
    H --> I["Business Recommendations"]
```

## Dashboard

## Results
The project produces:

- Customer cohorts such as Power, Core, Emerging, Selective and Occasional customers.
- Top product recommendations per customer for product group 1 and product group 3.
- A combined lead score that considers model probability, customer value, activity, and churn risk.
- A final output table suitable for dashboarding or CRM activation.

## Folder Structure
```text
lead-generation/
│
├── data/
│   ├── synthetic/
│   ├── processed/
│   ├── feature_engineering/
│   ├── cohort_clustering/
│   ├── product_recommendation/
│   └── dashboard_datasets/
│
├── notebooks/
│   ├── 00_generate_synthetic_dataset.ipynb
│   ├── 01_preprocessing.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_cohort_clustering.ipynb
│   ├── 04_product_recommendation_lead_generation.ipynb
│   └── 05_dashboard_datasets.ipynb
│
├── dashboard/
│   └── Lead Generation.pbix
│
├── images/
│   ├── executive_overview.png
│   ├── .png
│   └── .png
│
├── requirements.txt
└── README.md
```

## Installation

## Future Improvements

## Contact


