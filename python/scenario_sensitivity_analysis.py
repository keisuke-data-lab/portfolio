import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 0. 初期設定
# ==========================================
# Google Colabなどでグラフを表示させるコマンド
# (ローカル環境の場合は不要ですが念のため残します)
try:
    from IPython import get_ipython
    get_ipython().run_line_magic('matplotlib', 'inline')
except:
    pass

# 日本語フォント設定
try:
    import japanize_matplotlib
    print("✅ 日本語フォント(japanize_matplotlib)を読み込みました。")
except ImportError:
    print("⚠️ japanize_matplotlibが見つかりませんでした。")
    # フォールバック: 英語フォント
    plt.rcParams['font.family'] = 'sans-serif'

# ==========================================
# 1. 感度分析 (Sensitivity Heatmap)
# ==========================================
def plot_sensitivity_heatmap_conservative():
    # パラメータ範囲（基準12%を中心に設定）
    turnover_rates = [0.07, 0.12, 0.17, 0.22]
    turnover_labels = ["7%\n(改善)", "12%\n(基準)", "17%\n(悪化)", "22%\n(危機)"]
    premiums = [0.10, 0.20, 0.30, 0.40]
    
    data = []
    # 保守的モデルの前提（HP/MP混合 1000名）
    # 平均年収600万、採用費35%
    avg_salary = 600 
    n_employees = 1000
    
    for t in turnover_rates:
        row = []
        for p in premiums:
            # 24ヶ月分の離職数
            n_leavers = n_employees * t * 2 
            # 1人あたりコスト (採用費 + プレミアム差額)
            cost_per_hire = avg_salary * 0.35 + (avg_salary * p * 1.0)
            total_loss = n_leavers * cost_per_hire
            row.append(total_loss)
        data.append(row)
    
    # データフレーム作成
    df_sens = pd.DataFrame(data, index=turnover_labels, columns=[f"+{x:.0%}" for x in premiums])
    
    # 描画
    plt.figure(figsize=(9, 7))
    sns.heatmap(df_sens, annot=True, fmt=".0f", cmap="RdYlGn_r", 
                cbar_kws={'label': '推定キャッシュアウト損失 (百万円)'})
    
    plt.title("【感度分析】 離職率変動(改善/悪化) による財務インパクト", fontsize=14)
    plt.ylabel("年間離職率シナリオ")
    plt.xlabel("採用プレミアム (年収上乗せ率)")
    plt.tight_layout()
    plt.show()

# ==========================================
# 2. シナリオ・マトリクス (Lead Time Impact)
# ==========================================
def plot_leadtime_scenarios_v2():
    # 変動幅 (-2ヶ月の改善 〜 +3ヶ月の遅延)
    deltas = [-2, -1, 0, 1, 2, 3]
    
    # 基準損失額（保守シナリオの約11億円ベース）
    base_loss = 1077 # 百万円
    
    results_urban = []
    results_rural = []
    
    for d in deltas:
        # 都市部の変動 (改善すれば損失減、遅延すれば損失増)
        loss_u = base_loss * (1 + (d * 0.05)) 
        results_urban.append(loss_u)
        
        # 地方部の変動 (感度大: 崩壊リスクにより係数高め)
        if d > 0:
            loss_r = base_loss * (1 + (d * 0.15)) # 遅延ダメージ大
        else:
            loss_r = base_loss * (1 + (d * 0.08)) # 改善効果
            
        results_rural.append(loss_r)

    # グラフ化
    plt.figure(figsize=(10, 6))
    
    # 背景色分け
    plt.axvspan(-2.5, 0, color='green', alpha=0.05, label='改善機会 (Opportunity)')
    plt.axvspan(0, 3.5, color='red', alpha=0.05, label='悪化リスク (Risk)')
    
    # 基準線
    plt.axvline(x=0, color='gray', linestyle=':', label='現状(Base)')
    plt.axhline(y=base_loss, color='gray', linestyle=':', alpha=0.3)
    
    # プロット
    plt.plot(deltas, results_urban, marker='o', label='都市拠点 (基準:5ヶ月)', linewidth=2, color='#2980b9')
    plt.plot(deltas, results_rural, marker='x', label='地方拠点 (基準:10ヶ月)', linewidth=2, color='#c0392b')
    
    plt.title("【シナリオ分析】 採用リードタイムの「短縮(改善)」と「遅延(悪化)」の影響", fontsize=14)
    plt.xlabel("リードタイムの増減 (月数)")
    plt.ylabel("推定損失額 (百万円)")
    plt.xticks(deltas, [f"{d:+d}ヶ月" for d in deltas])
    plt.legend()
    plt.grid(True)
    plt.show()

# ==========================================
# 実行
# ==========================================
if __name__ == "__main__":
    print("グラフ生成中...")
    plot_sensitivity_heatmap_conservative()
    plot_leadtime_scenarios_v2()
    print("完了。")