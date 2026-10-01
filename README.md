# Mall Customer Segmentation and Recommendation System

A data-driven customer analytics and recommendation project that segments mall shoppers using clustering algorithms and generates business-oriented recommendations based on customer behavior.

This project combines:
- Python-based machine learning pipeline for customer segmentation
- K-Means and DBSCAN clustering analysis
- Customer profiling and recommendation logic
- React + Vite frontend for visual interaction and presentation

## Project Overview

The system analyzes customer data from the mall dataset and groups customers into clusters based on features such as:
- Age
- Annual income
- Spending score
- Gender

It then evaluates clustering quality, profiles each segment, and produces strategic recommendations for marketing, product targeting, and customer engagement.

## Features

- Customer data loading and validation
- Feature selection and standardization
- K-Means clustering
- DBSCAN clustering
- Clustering evaluation metrics
- Customer segment profiling
- Business recommendations by cluster
- Visualization of cluster results
- Interactive frontend dashboard

## Tech Stack

### Backend
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib / visualization modules

### Frontend
- React
- Vite
- JavaScript
- Recharts
- Axios

## Repository Structure

```text
Mall-Customer-Segmentation-and-Recommendation-System/
├── .gitignore
├── app.py
├── requirements.txt
├── backend/
│   ├── database.py
│   ├── error_handler.py
│   ├── logger.py
│   └── main.py
├── data/
│   └── Mall_Customers.csv
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── outputs/
├── src/
│   ├── clustering.py
│   ├── data_load.py
│   ├── dbscan.py
│   ├── evaluation.py
│   ├── preprocessing.py
│   ├── profiling.py
│   ├── recommendation.py
│   ├── recommendations.py
│   ├── visualization.py
│   └── ...
└── README.md
