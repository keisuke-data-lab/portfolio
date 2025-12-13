import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# ==========================================
# 0. 初期設定（フォント・表示設定）
# ==========================================
def set_japanese_font():
    """
    OS環境に合わせて日本語フォントを自動設定する関数
    GitHub等で公開しても他人の環境でエラーになりにくい構成
    """
    try:
        # japanize_matplotlib がインストールされていれば最優先で使用
        import japanize_matplotlib
    except ImportError:
        # インストールされていない場合、OSごとの標準フォントへフォールバック
        system_name = platform.system()
        if system_name == 'Windows':
            plt.rcParams['font.family'] = 'MS Gothic' # Windows標準
        elif system_name == 'Darwin':
            plt.rcParams['font.family'] = 'AppleGothic' # Mac標準
        else:
            plt.rcParams['font.family'] = 'sans-serif' # Linux/その他

# フォント設定の適用
set_japanese_font()

# 警告の抑制（きれいな出力のため）
import warnings
warnings.filterwarnings('ignore')

# ==========================================
# 1. データ生成ロジック
# ==========================================
def generate_heatmap_data(n_employees=1500):
    """
    組織の退職リスクデータを生成する
    """
    np.random.seed(42)
    branches = ['東京本社', '大阪支社', '名古屋支店', '福岡営業所', '仙台営業所', '北海道工場']
    roles = ['営業', 'エンジニア', '企画・マーケ', 'コーポレート', 'オペレーション']
    data = []
    
    for _ in range(n_employees):
        branch = np.random.choice(branches, p=[0.35, 0.2, 0.1, 0.1, 0.15, 0.1])
        role = np.random.choice(roles, p=[0.3, 0.2, 0.15, 0.1, 0.25])
        
        # 1. 地方拠点の崩壊シナリオ（リスク高）
        if branch in ['仙台営業所', '北海道工場', '福岡営業所']:
            if role == '営業':
                overtime = np.random.normal(80, 10)
            elif role == 'オペレーション':
                overtime = np.random.normal(70, 15)
            else:
                overtime = np.random.normal(40, 15)
        else:
            overtime = np.random.normal(25, 10)

        # 2. 都市部エンジニアの流出シナリオ（給与乖離）
        if role == 'エンジニア' and branch in ['東京本社', '大阪支社']:
            compa_ratio = np.random.normal(0.70, 0.05)
        elif role == '企画・マーケ':
            compa_ratio = np.random.normal(0.85, 0.1)
        else:
            compa_ratio = np.random.normal(1.0, 0.1)
            
        # リスクスコア算出ロジック
        risk_financial = max(0, 1.2 - compa_ratio) * 2.0 
        risk_workload = (min(overtime, 100) / 80) * 1.2
        
        if role == 'エンジニア':
            total_risk = (risk_financial * 0.7) + (risk_workload * 0.3)
        else:
            total_risk = (risk_financial * 0.3) + (risk_workload * 0.7)
            
        prob = min(0.98, max(0.05, total_risk))
        data.append({'Branch': branch, 'Role': role, 'Attrition_Risk': prob})
        
    return pd.DataFrame(data)

# ==========================================
# 2. 可視化ロジック
# ==========================================
def plot_risk_heatmap(df):
    """
    リスクヒートマップを描画して表示する
    """
    # ピボットテーブル作成
    pivot_table = df.pivot_table(index='Branch', columns='Role', values='Attrition_Risk', aggfunc='mean')
    
    # 表示順序の指定
    branch_order = ['東京本社', '大阪支社', '名古屋支店', '福岡営業所', '仙台営業所', '北海道工場']
    pivot_table = pivot_table.reindex(branch_order)
    
    # グラフ設定
    plt.figure(figsize=(12, 10))
    plt.subplots_adjust(bottom=0.28)
    
    # ヒートマップ描画
    sns.heatmap(
        pivot_table, 
        annot=True, 
        fmt=".1%", 
        cmap='RdYlGn_r', # 赤が高いリスク、緑が低いリスク
        vmin=0.0, 
        vmax=0.9, 
        linewidths=.5, 
        cbar_kws={'label': '離職予測確率 (AIスコア)'}
    )
    
    # タイトルとラベル
    plt.title('【添付B】拠点別・職種別 退職リスクヒートマップ', fontsize=16, pad=20)
    plt.xlabel('職種カテゴリー', fontsize=12)
    plt.ylabel('拠点', fontsize=12)
    
    # 分析コメントボックス
    text_content = (
        "■ 分析からの示唆\n"
        "1. 地方拠点（仙台/福岡/北海道）の『営業』および『オペレーション』が危険水域(80%超)。\n"
        "   → 採用難による恒常的な欠員と、残業負荷の集中が主因（負の連鎖）。\n\n"
        "2. 東京本社および大阪支社の『エンジニア』のリスクが顕著（約80%超）。\n"
        "   → 残業負荷は低いものの、給与乖離(Compa Ratio)による流出リスクが高まっている。\n"
        "   → 早急な処遇是正（トリアージ施策A）が必要。"
    )
    
    plt.figtext(
        0.5, 0.05, text_content, 
        fontsize=12, 
        ha="center", 
        bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.9)
    )
    
    # 画面表示（これを閉じないとプログラムは終了しません）
    plt.show()

# ==========================================
# 3. メイン実行処理
# ==========================================
if __name__ == "__main__":
    print("ヒートマップ生成中...")
    df_heatmap = generate_heatmap_data(1500)
    plot_risk_heatmap(df_heatmap)
    print("完了。ウィンドウを閉じて終了してください。")