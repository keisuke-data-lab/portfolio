# GPA決定要因と教育付加価値の分析
### Quantitative Analysis of GPA Factors: Value-Added Approach

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Focus](https://img.shields.io/badge/Focus-Learning%20Analytics%20%2F%20Student%20Success-green.svg)

---

## 🇯🇵 日本語概要 (Executive Summary)

本プロジェクトは、大学教育の成果指標である **GPA (Grade Point Average)** が、どのような要因によって決定されるかを定量的に検証したものです。

重回帰分析（OLS）を用いたシミュレーションの結果、GPA向上には単なる「学習時間の確保」だけでは不十分であり、**「学習方略（質）」** や **「経済的背景（アルバイト時間）」** が強く影響していることを明らかにしました。

👉 **[詳細レポート全文を読む (PDF)](docs/Value_Added_in_Higher_Education_Factors_GPA_StudyHabits_PartTimeWork.pdf)**

---

## 📘 Project Overview

This project analyzes the determinants of GPA using the **I-E-O (Input-Environment-Output) model**.
By simulating student data (N=3500) based on Japanese higher education trends, we identified that **"Learning Strategies"** and **"Economic Constraints (Time Poverty)"** are critical factors for academic success.

### 📊 Key Findings (from Python Simulation)

Based on OLS Regression analysis:
1.  **Quality over Quantity:** "Deep Learning Strategy" (t-value: 38.1) has a significantly higher impact on GPA than mere "Study Hours" (t-value: 18.7).
2.  **Impact of Part-time Work:** Working hours show a clear negative correlation (t-value: -22.1), confirming the "Time Poverty" hypothesis.

---

## 🛠 Methodology & Code

* **Simulation:** Generated dataset (N=3500) reflecting real-world distributions (JASSO surveys).
* **Analysis:** Hierarchical Multiple Regression Analysis.
* **Tools:** Python (`statsmodels`, `pandas`, `numpy`)

### 📂 Repository Structure
* `value_added_analysis.ipynb`: Python code for data generation and regression analysis.
* `docs/`: Full report in PDF format.

---

## 👤 Author
**Keisuke Nakamura (keisuke-data-lab)**
*Data Analyst / University IR Specialist*

---
> © 2025 Keisuke Nakamura