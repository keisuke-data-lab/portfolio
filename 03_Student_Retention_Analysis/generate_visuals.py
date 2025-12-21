import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# フォルダ作成
os.makedirs('images', exist_ok=True)

# 日本語フォント設定（英語で統一してグローバル対応）
plt.rcParams['font.family'] = 'sans-serif'

# --- 1. データ生成 (Synthetic Data Generation) ---
np.random.seed(42)
n_students = 1000

# 変数生成
# 経済状況 (1: 余裕あり, 5: 困窮)
economic_distress = np.random.randint(1, 6, n_students)
# アルバイト時間 (週) - 経済状況が悪いほど長くなる傾向
work_hours = economic_distress * 5 + np.random.normal(0, 5, n_students)
work_hours = np.clip(work_hours, 0, 40)
# 自習時間 (週) - アルバイト時間が長いほど短くなる (時間貧困)
study_time = 40 - work_hours * 0.8 + np.random.normal(0, 5, n_students)
study_time = np.clip(study_time, 0, 50)
# GPA - 自習時間に比例
gpa = study_time * 0.08 + np.random.normal(1.5, 0.5, n_students)
gpa = np.clip(gpa, 0.0, 4.0)

# データフレーム化
df = pd.DataFrame({
    'Economic_Distress': economic_distress,
    'Work_Hours': work_hours,
    'Study_Time': study_time,
    'GPA': gpa
})

# --- 2. 可視化: "時間貧困"の構造 (Time Poverty Structure) ---
plt.figure(figsize=(10, 6))
sns.regplot(x='Work_Hours', y='GPA', data=df, scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
plt.title('Impact of "Time Poverty": Work Hours vs. GPA', fontsize=14)
plt.xlabel('Part-time Work Hours (per week)', fontsize=12)
plt.ylabel('GPA (Academic Performance)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('images/time_poverty_analysis.png', dpi=300)
print("Saved: images/time_poverty_analysis.png")

# --- 3. 可視化: 経済困窮度別のドロップアウト・リスク (Risk Heatmap) ---
# リスクスコア算出 (GPAが低く、労働時間が長いほど高リスク)
df['Dropout_Risk'] = (df['Work_Hours'] / 40) * 0.5 + (4.0 - df['GPA']) / 4.0 * 0.5

pivot_table = df.pivot_table(index='Economic_Distress', columns=pd.cut(df['Work_Hours'], bins=5), values='Dropout_Risk')

plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, cmap='RdYlGn_r', fmt=".2f")
plt.title('Dropout Risk Heatmap: Economic Distress vs. Work Hours', fontsize=14)
plt.xlabel('Weekly Work Hours Range', fontsize=12)
plt.ylabel('Economic Distress Level (1=Low, 5=High)', fontsize=12)
plt.tight_layout()
plt.savefig('images/dropout_risk_heatmap.png', dpi=300)
print("Saved: images/dropout_risk_heatmap.png")

print("All visualizations generated successfully.")