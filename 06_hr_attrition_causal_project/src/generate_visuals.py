# src/generate_visuals.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

# 設定
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif' 

# 保存先ディレクトリの確保
OUTPUT_DIR = "../images"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("画像生成プロセスを開始します（レイアウト修正版）...")

# 1. データの読み込み
try:
    df = pd.read_csv('../data/simulated_hr_data.csv')
except FileNotFoundError:
    print("Error: '../data/simulated_hr_data.csv' not found.")
    exit()

# ---------------------------------------------------------
# Graph 1: 離職率の推移 (Attrition Curve)
# ---------------------------------------------------------
print("Generating: 01_attrition_curve.png")
tenure_stats = df.groupby('tenure_months').agg(
    total_count=('employee_id', 'count'),
    attrition_count=('attrition_flag', 'sum')
).reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x='tenure_months', y='attrition_count', data=tenure_stats, marker='o', color='crimson', linewidth=2.5)
plt.title('Attrition Curve: Risk Peaks at Onboarding & 3 Years', fontsize=14, fontweight='bold')
plt.xlabel('Tenure (Months)', fontsize=12)
plt.ylabel('Count of Attritions', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_attrition_curve.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# Graph 2: ROIシミュレーション比較 (Current Market)
# ---------------------------------------------------------
print("Generating: 02_roi_comparison.png")

strategies = ['A: Train All', 'B: Raise All', 'C: Targeted Mix']
costs = [75, 225, 21.65]  
benefits = [145, 145, 294.4] 
rois = [93.3, -35.6, 1259.8] 

x = np.arange(len(strategies))
width = 0.35

fig, ax1 = plt.subplots(figsize=(10, 7)) # 高さを少し広げました

# 棒グラフ描画
rects1 = ax1.bar(x - width/2, costs, width, label='Cost (M JPY)', color='gray', alpha=0.6)
rects2 = ax1.bar(x + width/2, benefits, width, label='Benefit (M JPY)', color='skyblue', alpha=0.8)

ax1.set_ylabel('Amount (Million JPY)', fontsize=12)
ax1.set_title('Strategy Comparison: Targeting Maximizes ROI (Current Market)', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(strategies, fontsize=11)
ax1.legend(loc='upper left')

# Y軸のマージン確保（テキストが見切れないように上限を高く設定）
max_val = max(max(costs), max(benefits))
ax1.set_ylim(0, max_val * 1.15) 

# ROI数値をグラフ上に表示
for i, roi in enumerate(rois):
    # 棒グラフの高い方に合わせてテキスト配置
    height = max(costs[i], benefits[i])
    color = 'green' if roi > 0 else 'red'
    
    ax1.text(x[i], height + (max_val * 0.02), 
             f"ROI: {roi}%", 
             ha='center', va='bottom', fontweight='bold', color=color, fontsize=12)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_roi_comparison.png", dpi=300)
plt.close()

# ---------------------------------------------------------
# Graph 3: パラダイムシフト (Past vs Current)
# ---------------------------------------------------------
print("Generating: 03_paradigm_shift.png")

markets = ['Past Market\n(Hiring Cost: 800k)', 'Current Market\n(Hiring Cost: 4M)']
rois_paradigm = [172.0, 1259.8] 

plt.figure(figsize=(9, 7)) # 高さを確保
colors = ['#888888', '#d9534f'] 
bars = plt.bar(markets, rois_paradigm, color=colors, width=0.5)

plt.axhline(0, color='black', linewidth=1)
plt.title('Paradigm Shift: Why Retention Matters NOW', fontsize=15, fontweight='bold')
plt.ylabel('ROI of Targeted Retention Strategy (%)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Y軸の上限設定（テキストスペース確保）
plt.ylim(0, max(rois_paradigm) * 1.15)

# 数値ラベル
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 20, 
             f'{height:.1f}%',
             ha='center', va='bottom', fontsize=14, fontweight='bold')

# ★レイアウト修正の肝: 下部に余白を作ってからテキストを配置★
plt.subplots_adjust(bottom=0.2) 

# Insightコメント
plt.figtext(0.5, 0.05, 
            "Insight: In the current market (Right), retention investment is the ONLY profitable option.", 
            ha="center", fontsize=11, 
            bbox={"facecolor":"orange", "alpha":0.1, "pad":8, "edgecolor":"orange"})

plt.savefig(f"{OUTPUT_DIR}/03_paradigm_shift.png", dpi=300)
plt.close()

print(f"完了: レイアウト修正済みの画像が {OUTPUT_DIR} フォルダに保存されました。")