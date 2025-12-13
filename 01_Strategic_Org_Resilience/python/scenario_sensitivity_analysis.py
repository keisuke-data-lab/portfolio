import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import font_manager

# ==========================================
# 0. 日本語フォントを「強制指定」
# ==========================================

FONT_PATHS = [
    # Windows（最優先）
    "C:/Windows/Fonts/meiryo.ttc",
    "C:/Windows/Fonts/msgothic.ttc",
    # Linux / Colab
    "/usr/share/fonts/truetype/ipafont-gothic/ipag.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
]

JP_FONT = None
for path in FONT_PATHS:
    if os.path.exists(path):
        JP_FONT = font_manager.FontProperties(fname=path)
        print(f"✅ 日本語フォント使用: {path}")
        break

if JP_FONT is None:
    raise RuntimeError("❌ 日本語フォントが見つかりません")

# Matplotlib 基本設定
plt.rcParams["axes.unicode_minus"] = False

# ==========================================
# 1. 感度分析ヒートマップ
# ==========================================
def plot_sensitivity_heatmap_conservative():

    turnover_labels = ["7%\n(改善)", "12%\n(基準)", "17%\n(悪化)", "22%\n(危機)"]
    premiums = [0.10, 0.20, 0.30, 0.40]

    avg_salary = 600
    n_employees = 1000

    data = []
    for t in [0.07, 0.12, 0.17, 0.22]:
        row = []
        for p in premiums:
            n_leavers = n_employees * t * 2
            cost = avg_salary * 0.35 + avg_salary * p
            row.append(n_leavers * cost)
        data.append(row)

    df = pd.DataFrame(
        data,
        index=turnover_labels,
        columns=[f"+{int(p*100)}%" for p in premiums]
    )

    fig, ax = plt.subplots(figsize=(9, 7))

    sns.heatmap(
        df,
        annot=True,
        fmt=".0f",
        cmap="RdYlGn_r",
        ax=ax,
        cbar_kws={"label": "推定キャッシュアウト損失（百万円）"}
    )

    ax.set_title(
        "【感度分析】離職率変動（改善／悪化）による財務インパクト",
        fontproperties=JP_FONT,
        fontsize=14
    )
    ax.set_xlabel("採用プレミアム（年収上乗せ率）", fontproperties=JP_FONT)
    ax.set_ylabel("年間離職率シナリオ", fontproperties=JP_FONT)

    # カラーバーの日本語
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.label.set_fontproperties(JP_FONT)

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(JP_FONT)

    plt.tight_layout()
    plt.show()

# ==========================================
# 2. リードタイム・シナリオ分析
# ==========================================
def plot_leadtime_scenarios_v2():

    deltas = [-2, -1, 0, 1, 2, 3]
    base_loss = 1077

    urban = [base_loss * (1 + d * 0.05) for d in deltas]
    rural = [
        base_loss * (1 + d * 0.15) if d > 0 else base_loss * (1 + d * 0.08)
        for d in deltas
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.axvspan(-2.5, 0, alpha=0.08, color="green", label="改善機会（Opportunity）")
    ax.axvspan(0, 3.5, alpha=0.08, color="red", label="悪化リスク（Risk）")

    ax.axvline(0, linestyle=":", color="gray", label="現状（Base）")
    ax.axhline(base_loss, linestyle=":", color="gray", alpha=0.3)

    ax.plot(deltas, urban, marker="o", label="都市拠点（基準：5ヶ月）", linewidth=2)
    ax.plot(deltas, rural, marker="x", label="地方拠点（基準：10ヶ月）", linewidth=2)

    ax.set_title(
        "【シナリオ分析】採用リードタイム短縮・遅延の財務影響",
        fontproperties=JP_FONT,
        fontsize=14
    )
    ax.set_xlabel("リードタイム増減（月）", fontproperties=JP_FONT)
    ax.set_ylabel("推定損失額（百万円）", fontproperties=JP_FONT)

    ax.set_xticks(deltas)
    ax.set_xticklabels([f"{d:+d}ヶ月" for d in deltas], fontproperties=JP_FONT)

    legend = ax.legend()
    for text in legend.get_texts():
        text.set_fontproperties(JP_FONT)

    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ==========================================
# 実行
# ==========================================
if __name__ == "__main__":
    plot_sensitivity_heatmap_conservative()
    plot_leadtime_scenarios_v2()
