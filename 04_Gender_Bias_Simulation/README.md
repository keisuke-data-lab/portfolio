## 🔒 この研究の位置づけ（必読）
本プロジェクトは、特定の企業・団体・個人を批判する意図はありません。
日本の労働市場に存在するとされる構造的課題を、数理モデルと社会科学の枠組みを用いて中立的に可視化するための、個人的な学術研究です。
記述される内容は仮想シミュレーションであり、実際の組織の実データを扱うものではありません。

---

# Quantitative Modeling of Gender Bias and Productivity Loss in Japanese Organizations
### — Statistical Discrimination Simulation using Python —

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Analysis](https://img.shields.io/badge/Focus-Gender%20Bias%20Simulation-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 🎯 Project Purpose — Why This Analysis Matters
This project visualizes **how statistical discrimination (性別による期待値差別)**  
impacts:

- Productivity  
- Talent selection efficiency  
- Organizational human capital  
- Long-term promotion pipelines  

using mathematical models + Python simulation.

Objective:  
➡ **Transform a social issue into a quantifiable decision-making framework.**

---

## 📄 Main Output (PDF Report)
**📘 structural_analysis_gender_imbalance.pdf**  
(*/docs に配置予定*)

The PDF combines:

- 経済学（Arrow, Goldin）  
- 社会学（Goffman, Kanter）  
- 数理モデル（三つのモデル）  
- Python シミュレーション  

into a single coherent theoretical framework.

---

## 🧪 Python Simulation — Core Notebook
**`/notebooks/gender_bias_simulation.ipynb`**

Simulates the effect of **Bias γ** (男性だけ合格基準を下げる優遇度合い) on:

- Accepted applicant ability  
- Gender ability gap  
- Organizational productivity loss  

Mathematically modeled via:

- Truncated normal distributions  
- Threshold manipulation  
- Expected value analysis  

---

## 📊 Key Findings — What the Simulation Reveals

| Bias (γ) | 男性合格ライン | 男性平均能力 | 女性平均能力 | Productivity Gap |
|---------|---------------|--------------|--------------|------------------|
| 0.00 | 0.65 | 0.724 | 0.789 | 0.065 |
| 0.10 | 0.55 | 0.670 | 0.789 | 0.119 |
| 0.20 | 0.45 | 0.627 | 0.789 | 0.162 |

### ✔ 結論：優遇すると組織の平均能力は “確実に” 下がる  
モデルは、日本企業の  
「逆選抜（Negative Selection）」  
を数学的に説明します。

---

## 🧩 Methodology Overview

### **1. Selection Efficiency Model**  
採用時の期待値損失を確率密度関数で計算。

### **2. Human Capital Depreciation Model**  
Time Poverty を差分方程式でモデル化。

### **3. Markov Chain Model of Broken Rung**  
初期昇進確率の差 → 上位ポストで指数的な格差。

---

## 🔮 Roadmap
- 医学部不正入試データでの再現検証  
- 大学 IR 向け「昇進確率シミュレーション」作成  
- Bias Stress Test（人事部門向けツール）化  
- Power BI / Tableau ダッシュボード化  

---

## 👤 Author
**Keisuke Nakamura  
University IR / Data Analysis**

- 組織・人事データの分析  
- ガバナンス & 経営視点  
- Python による意思決定モデル構築  

---

This theoretical simulation provides IR offices and university leaders with a framework to evaluate talent pipeline risks and organizational productivity losses even in the absence of complete institutional data.
In university IR practice, this model serves as a diagnostic tool to evaluate structural risks in promotion pipelines and to simulate productivity impacts when internal data is incomplete or unavailable.

© 2025 Keisuke Nakamura (keisuke-data-lab)
