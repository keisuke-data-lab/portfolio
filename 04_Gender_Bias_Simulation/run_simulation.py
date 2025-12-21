import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# フォルダ作成
os.makedirs('images', exist_ok=True)

# 日本語フォント設定（英語で統一）
plt.rcParams['font.family'] = 'sans-serif'

# --- シミュレーション設定 (Martell-Lane Model inspired) ---
n_levels = 8          # 組織の階層数 (L1:新人 -> L8:役員)
n_employees = 500     # 各階層の人数 (ピラミッドではなく簡略化のため同数と仮定)
promotion_rate = 0.15 # 昇進率
bias_effect = 0.05    # バイアス効果 (男性の評価スコアに +5% のゲタを履かせる)

# 初期状態: 全階層で男女比 50:50python run_simulation.py
levels = np.repeat(range(1, n_levels + 1), n_employees)
gender = np.tile(['Male', 'Female'], int(len(levels)/2))
df = pd.DataFrame({'Level': levels, 'Gender': gender})

# シミュレーション実行 (20サイクル = 約20年経過)
history_female_ratio = []

for cycle in range(20):
    # 1. 評価スコア生成 (正規分布)
    df['Score'] = np.random.normal(0, 1, len(df))
    
    # 2. バイアスの適用 (男性に少しだけ有利な評価)
    # 男性(Male)のスコアに bias_effect を加算
    df.loc[df['Gender'] == 'Male', 'Score'] += bias_effect
    
    # 3. 昇進プロセス (上位N%が昇進)
    # 各レベルごとに上位者を抽出して、ひとつ上のレベルへ
    # (簡易シミュレーションのため、ここでは「レベルごとの女性比率」の変化だけを計算)
    
    # 仮想的な昇進: 各レベルの上位15%の男女比を計算し、次のサイクルのそのレベルの男女比とする
    new_ratios = []
    for lvl in range(1, n_levels + 1):
        level_df = df[df['Level'] == lvl]
        # 上位15%を抽出
        n_promoted = int(len(level_df) * promotion_rate)
        top_performers = level_df.nlargest(n_promoted, 'Score')
        
        # 女性比率を計算
        female_ratio = (top_performers['Gender'] == 'Female').mean()
        new_ratios.append(female_ratio)
    
    history_female_ratio.append(new_ratios)

# 結果の集計
final_ratios = history_female_ratio[-1]
levels_label = [f'L{i}' for i in range(1, n_levels + 1)]

# --- 可視化 1: 「ガラスの天井」 (Glass Ceiling Effect) ---
plt.figure(figsize=(10, 6))
colors = ['#1f77b4' if r < 0.3 else '#2ca02c' for r in final_ratios] # 30%未満は青(警告色代わり)、以上は緑

sns.barplot(x=levels_label, y=final_ratios, palette="Blues_r")
plt.axhline(0.5, color='red', linestyle='--', label='Target (50%)')
plt.axhline(0.3, color='orange', linestyle=':', label='Critical Line (30%)')

plt.title(f'The "Glass Ceiling": Female Ratio by Level after 20 Cycles\n(Bias Effect: +{bias_effect*100}%)', fontsize=14)
plt.ylabel('Female Ratio', fontsize=12)
plt.xlabel('Organizational Level (L1=Entry -> L8=Executive)', fontsize=12)
plt.ylim(0, 0.6)
plt.legend()
plt.tight_layout()
plt.savefig('images/glass_ceiling_effect.png', dpi=300)
print("Saved: images/glass_ceiling_effect.png")

# --- 可視化 2: 時系列変化 (Time Evolution at Top Level) ---
top_level_history = [cycle[-1] for cycle in history_female_ratio] # L8の推移

plt.figure(figsize=(10, 6))
plt.plot(range(1, 21), top_level_history, marker='o', color='purple', linewidth=2)
plt.title('Disappearance of Diversity: Female Ratio in Executives (L8) over Time', fontsize=14)
plt.xlabel('Simulation Cycles (Years)', fontsize=12)
plt.ylabel('Female Ratio in Executives', fontsize=12)
plt.axhline(0.5, color='grey', linestyle='--', alpha=0.5)
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(0, 0.6)
plt.tight_layout()
plt.savefig('images/time_evolution.png', dpi=300)
print("Saved: images/time_evolution.png")