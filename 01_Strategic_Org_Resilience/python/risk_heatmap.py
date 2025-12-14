import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# フォルダが存在しない場合は作成
os.makedirs('report', exist_ok=True)
plt.rcParams['font.family'] = 'Meiryo'

# データの生成
def generate_risk_data():
    branches = ['東京本社', '大阪支社', '名古屋支社', '福岡支社', '札幌支社']
    jobs = ['営業', 'エンジニア', '企画', '事務', '人事']
    
    data = []
    for b in branches:
        row = []
        for j in jobs:
            score = np.random.randint(20, 60)
            if b in ['福岡支社', '札幌支社'] and j in ['営業', 'エンジニア']:
                score = np.random.randint(80, 95)
            if b == '東京本社' and j == 'エンジニア':
                score = np.random.randint(70, 90)
            row.append(score / 100)
        data.append(row)
        
    return pd.DataFrame(data, index=branches, columns=jobs)

# 描画
df = generate_risk_data()

plt.figure(figsize=(10, 6))
sns.heatmap(df, annot=True, fmt=".0%", cmap='RdYlGn_r', vmin=0, vmax=1)
plt.title('【添付B】拠点別・職種別 退職リスクヒートマップ', fontsize=14)
plt.xlabel('職種 (Job Function)')
plt.ylabel('拠点 (Branch)')

plt.tight_layout()
plt.savefig('report/risk_heatmap.png')
print("✅ risk_heatmap.png generated.")