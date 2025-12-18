import pandas as pd
import numpy as np
import os

# フォルダ作成
os.makedirs('data', exist_ok=True)

# --- データ生成設定 ---
np.random.seed(42)
n_employees = 500

# 1. 属性データ
departments = ['Sales', 'R&D', 'Marketing', 'HR', 'Admin']
job_levels = ['Junior', 'Mid', 'Senior', 'Manager']

dept_data = np.random.choice(departments, n_employees, p=[0.4, 0.2, 0.2, 0.1, 0.1])
level_data = np.random.choice(job_levels, n_employees, p=[0.4, 0.3, 0.2, 0.1])

# 2. 研修・コストデータ
# 研修時間 (Training Hours): 0~50時間
training_hours = np.random.normal(20, 10, n_employees)
training_hours = np.clip(training_hours, 0, 60).round(1)

# 研修コスト (Cost): 時間比例 + 固定費 + ランダム
cost = training_hours * 5000 + np.random.normal(10000, 2000, n_employees)
cost = cost.round(0)

# 3. パフォーマンスデータ (Before/After)
# Pre-training: 2.0 ~ 4.0
pre_performance = np.random.normal(3.0, 0.5, n_employees)
pre_performance = np.clip(pre_performance, 1.0, 5.0).round(2)

# Post-training: 研修時間と元の能力に依存して向上
improvement = (training_hours * 0.05) + np.random.normal(0.1, 0.2, n_employees)
# 部署によるバイアス（営業は上がりやすい設定など）
dept_bias = np.where(dept_data == 'Sales', 0.2, 0)
post_performance = pre_performance + improvement + dept_bias
post_performance = np.clip(post_performance, 1.0, 5.0).round(2)

# 4. ROI計算 (簡易モデル: スコア向上1.0あたり 50万円の利益創出と仮定)
value_created = (post_performance - pre_performance) * 500000
value_created = np.where(value_created < 0, 0, value_created) # マイナスはないとする
roi_percent = ((value_created - cost) / cost) * 100

# データフレーム化
df = pd.DataFrame({
    'EmployeeID': range(1001, 1001 + n_employees),
    'Department': dept_data,
    'JobLevel': level_data,
    'TrainingHours': training_hours,
    'TrainingCost': cost,
    'Pre_Performance': pre_performance,
    'Post_Performance': post_performance,
    'Performance_Diff': (post_performance - pre_performance).round(2),
    'ValueCreated': value_created.round(0),
    'ROI_Percent': roi_percent.round(1)
})

# CSV出力
csv_path = 'data/human_capital_roi_data.csv'
df.to_csv(csv_path, index=False, encoding='utf-8-sig')

print(f"Data exported successfully: {csv_path}")
print(df.head())