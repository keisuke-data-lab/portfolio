import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform # OS判定用

# ==========================================
# 0. 環境設定
# ==========================================
# Jupyter Notebook用の記述(%matplotlib inline)は削除しました

def set_japanese_font():
    """OS環境に合わせて日本語フォントを自動設定する"""
    try:
        import japanize_matplotlib
    except ImportError:
        system_name = platform.system()
        if system_name == 'Windows':
            plt.rcParams['font.family'] = 'MS Gothic' 
        elif system_name == 'Darwin': # Mac
            plt.rcParams['font.family'] = 'AppleGothic'
        else:
            plt.rcParams['font.family'] = 'sans-serif'

set_japanese_font()
# 警告を見やすく抑制
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 1. 感度分析 (改善・悪化の両面評価)
# ==========================================
def get_sensitivity_data():
    # パラメータ範囲（改善ケースを含める）
    turnover_rates = [0.07, 0.12, 0.17, 0.22]
    turnover_labels = ["7%\n(改善)", "12%\n(基準)", "17%\n(悪化)", "22%\n(危機)"]
    
    # 採用プレミアム変動: 10% 〜 40%
    premiums = [0.10, 0.20, 0.30, 0.40]
    
    data = []
    
    # モデル条件 (HP/MP混合 1000名規模で簡易試算)
    avg_salary = 600 # 万円
    n_employees = 1000
    
    for t in turnover_rates:
        row = []
        for p in premiums:
            # 簡易損失計算 (Cash Out = 採用費 + プレミアム差額)
            n_leavers = n_employees * t * 2 
            
            # 1人あたり入替コスト
            # Agency(35%) + Premium(p) * 雇用期間(平均1年と仮定)
            cost_per_hire = avg_salary * 0.35 + (avg_salary * p * 1.0)
            
            total_loss = n_leavers * cost_per_hire
            row.append(total_loss)
        data.append(row)
    
    return pd.DataFrame(data, index=turnover_labels, columns=[f"+{x:.0%}" for x in premiums])

def plot_sensitivity_heatmap_v2(df_sens):
    plt.figure(figsize=(9, 7))
    
    # 色使い: 損失が小さい(改善)＝緑、大きい(悪化)＝赤
    sns.heatmap(df_sens, annot=True, fmt=".0f", cmap="RdYlGn_r", 
                cbar_kws={'label': '推定キャッシュアウト損失 (百万円)'})
    
    plt.title("【感度分析】 離職率変動(改善/悪化) による財務インパクト", fontsize=14)
    plt.ylabel("年間離職率シナリオ")
    plt.xlabel("採用プレミアム (年収上乗せ率)")
    
    plt.tight_layout()
    plt.show()

# ==========================================
# 2. シナリオ・マトリクス (リードタイム改善の価値)
# ==========================================
def plot_leadtime_scenarios_v2(df_sens, base_loss=3838):
    # 変動幅 (-2ヶ月の改善 〜 +3ヶ月の遅延)
    deltas = [-2, -1, 0, 1, 2, 3]
    
    results_urban = []
    results_rural = []
    
    for d in deltas:
        # 都市部の変動 (改善すれば損失減、遅延すれば損失増)
        # 感度係数: 1ヶ月あたり 5% 変動と仮定
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
    
    # 0ライン（基準）
    plt.axvline(x=0, color='gray', linestyle=':', alpha=0.8)
    plt.axhline(y=base_loss, color='gray', linestyle=':', alpha=0.3)
    
    # プロット
    plt.plot(deltas, results_urban, marker='o', label='都市拠点 (基準:5ヶ月)', linewidth=2, color='#2980b9')
    plt.plot(deltas, results_rural, marker='x', label='地方拠点 (基準:10ヶ月)', linewidth=2, color='#c0392b')
    
    # 背景色分け
    plt.axvspan(-2.5, 0, color='green', alpha=0.05, label='改善機会 (Opportunity)')
    plt.axvspan(0, 3.5, color='red', alpha=0.05, label='悪化リスク (Risk)')

    plt.title("【シナリオ分析】 採用リードタイムの「短縮(改善)」と「遅延(悪化)」の影響", fontsize=14)
    plt.xlabel("リードタイムの増減 (月数)")
    plt.ylabel("推定損失額 (百万円)")
    plt.xticks(deltas, [f"{d:+d}ヶ月" for d in deltas])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # 数値出力
    print("【分析サマリ】")
    print(f"・現状維持(基準): {base_loss} 百万円")
    print(f"・離職率5%改善時(7%): {df_sens.iloc[0,1]:.0f} 百万円 (約{(base_loss - df_sens.iloc[0,1]):.0f}百万円のコスト削減効果)")
    print(f"・リードタイム2ヶ月短縮時(都市): {results_urban[0]:.0f} 百万円")

# ==========================================
# 実行
# ==========================================
if __name__ == "__main__":
    print("感度分析を実行中...")
    
    # データ生成
    df_sensitivity = get_sensitivity_data()
    
    # グラフ描画1: ヒートマップ
    plot_sensitivity_heatmap_v2(df_sensitivity)
    
    # グラフ描画2: シナリオ分析
    # ※グラフ1を閉じた後にグラフ2が表示されます
    plot_leadtime_scenarios_v2(df_sensitivity)
    
    print("完了。")