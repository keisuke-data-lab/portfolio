import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import font_manager

# 保存用フォルダ作成
os.makedirs('report', exist_ok=True)

# ==========================================
# 0. 日本語フォント設定（あなたのコードを維持）
# ==========================================
FONT_PATHS = [
    "C:/Windows/Fonts/meiryo.ttc",
    "C:/Windows/Fonts/msgothic.ttc",
    "/usr/share/fonts/truetype/ipafont-gothic/ipag.ttf"
]
JP_FONT = None
for path in FONT_PATHS:
    if os.path.exists(path):
        JP_FONT = font_manager.FontProperties(fname=path)
        break

# フォントが見つからない場合の安全策
if JP_FONT is None:
    print("⚠️ 日本語フォントが見つかりません。デフォルトフォントを使用します。")
    plt.rcParams['font.family'] = 'sans-serif'
else:
    plt.rcParams['font.family'] = JP_FONT.get_name()

plt.rcParams["axes.unicode_minus"] = False

# ==========================================
# 1. 感度分析ヒートマップ（描画のみに簡略化して統合）
# ==========================================
# ※今回はREADME用の「シナリオ分析」画像を優先するため、下の関数をメインで動かします

# ==========================================
# 2. リードタイム・シナリオ分析 (あなたのコード + 保存処理)
# ==========================================
def plot_leadtime_scenarios_v2():
    deltas = [-2, -1, 0, 1, 2, 3]
    base_loss = 1077

    urban = [base_loss * (1 + d * 0.05) for d in deltas]
    rural = [base_loss * (1 + d * 0.15) if d > 0 else base_loss * (1 + d * 0.08) for d in deltas]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.axvspan(-2.5, 0, alpha=0.08, color="green", label="改善機会（Opportunity）")
    ax.axvspan(0, 3.5, alpha=0.08, color="red", label="悪化リスク（Risk）")
    ax.axvline(0, linestyle=":", color="gray", label="現状（Base）")
    ax.axhline(base_loss, linestyle=":", color="gray", alpha=0.3)

    # プロット
    ax.plot(deltas, urban, marker="o", label="都市拠点（基準：5ヶ月）", linewidth=2)
    ax.plot(deltas, rural, marker="x", label="地方拠点（基準：10ヶ月）", linewidth=2)

    # フォントプロパティの適用
    title_font = JP_FONT if JP_FONT else None
    
    ax.set_title("【シナリオ分析】採用リードタイム短縮・遅延の財務影響", fontproperties=title_font, fontsize=14)
    ax.set_xlabel("リードタイム増減（月）", fontproperties=title_font)
    ax.set_ylabel("推定損失額（百万円）", fontproperties=title_font)
    ax.set_xticks(deltas)
    ax.set_xticklabels([f"{d:+d}ヶ月" for d in deltas], fontproperties=title_font)
    
    # 凡例のフォント設定
    legend = ax.legend()
    if title_font:
        for text in legend.get_texts():
            text.set_fontproperties(title_font)

    plt.grid(True)
    plt.tight_layout()
    
    # 【追加】画像を保存
    plt.savefig('report/sensitivity_analysis.png')
    print("✅ sensitivity_analysis.png generated.")
    
# ==========================================
# 実行
# ==========================================
if __name__ == "__main__":
    plot_leadtime_scenarios_v2()