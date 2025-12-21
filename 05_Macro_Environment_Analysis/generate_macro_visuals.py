import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# フォルダ作成
os.makedirs('images', exist_ok=True)

# 日本語フォント設定（英語で統一）
plt.rcParams['font.family'] = 'sans-serif'

# --- 1. データ生成: 日本の18歳人口予測 (Synthetic Data based on trends) ---
# 2020年から2040年までの予測
years = np.arange(2020, 2041)
n_years = len(years)

# 18歳人口 (万人): 2020年の約118万人から2040年の82万人へ減少トレンド
# ノイズを含ませてリアルにする
trend = np.linspace(118, 82, n_years)
population_18 = trend + np.random.normal(0, 1.0, n_years)

# 大学収容力 (Capacity): 定員割れ対策で微減するが、人口減には追いつかない
capacity = np.linspace(110, 105, n_years) 

# 進学率 (Enrollment Rate): 横ばい〜微増と仮定 (55% -> 57%)
rate = np.linspace(0.55, 0.57, n_years)
applicants = population_18 * rate

# --- 2. 可視化: 「2040年問題」 (The 2040 Problem) ---
plt.figure(figsize=(10, 6))

# 人口と定員のライン
plt.plot(years, population_18, label='18-year-old Population (10k)', color='#1f77b4', linewidth=3)
plt.plot(years, capacity, label='Total University Capacity (10k)', color='#d62728', linestyle='--', linewidth=2)

# 定員割れエリア（供給過剰）の塗りつぶし
plt.fill_between(years, population_18 * rate, capacity, 
                 where=(capacity > population_18 * rate), 
                 color='red', alpha=0.1, label='Supply Excess (Bankruptcy Risk)')

plt.title('The "2040 Problem": Population Decline vs. University Capacity', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Population / Capacity (Ten Thousand)', fontsize=12)
plt.legend(loc='lower left')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('images/macro_population_trend.png', dpi=300)
print("Saved: images/macro_population_trend.png")

# --- 3. 可視化: 架空大学の財務シミュレーション (P&L Impact) ---
# ある地方私立大学のモデルケース
uni_capacity = 1000 # 定員
uni_applicants = (applicants / applicants[0]) * 1000 * 1.05 # 市場縮小に連動
uni_entrants = np.minimum(uni_applicants, uni_capacity) # 定員以上はとれない（定員割れはそのまま）

# 財務データ
tuition = 1.2 # 学費 120万円
revenue = uni_entrants * tuition # 収入
fixed_cost = 1000 # 固定費 10億円
variable_cost = uni_entrants * 0.1 # 変動費 10万円/人
total_cost = fixed_cost + variable_cost
profit = revenue - total_cost

plt.figure(figsize=(10, 6))

# 棒グラフ（利益/赤字）
colors = ['red' if p < 0 else 'blue' for p in profit]
plt.bar(years, profit, color=colors, alpha=0.6, label='Net Income')

# 折れ線（収入とコスト）
plt.plot(years, revenue, color='green', marker='o', markersize=4, label='Tuition Revenue')
plt.plot(years, total_cost, color='gray', linestyle='--', label='Total Cost (Fixed+Var)')

plt.axhline(0, color='black', linewidth=0.8)
plt.title('Financial Simulation: Impact of Enrollment Decline', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Amount (Million JPY)', fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('images/financial_impact_simulation.png', dpi=300)
print("Saved: images/financial_impact_simulation.png")