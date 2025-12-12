import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import warnings
import platform # OS判定用に追加

warnings.filterwarnings('ignore')

# ==========================================
# 0. 初期設定 (日本語フォント対応版)
# ==========================================
# 再現性確保のためのシード固定
np.random.seed(42)
random.seed(42)

# 日本語フォント設定の強化
# japanize_matplotlibがあれば使い、なければOSに合わせて標準フォントを指定する
try:
    import japanize_matplotlib
except ImportError:
    system_name = platform.system()
    if system_name == 'Windows':
        plt.rcParams['font.family'] = 'MS Gothic' # Windows標準
    elif system_name == 'Darwin':
        plt.rcParams['font.family'] = 'AppleGothic' # Mac標準
    else:
        # Linux/Google Colab等の場合、フォントがないと豆腐になる可能性があります
        plt.rcParams['font.family'] = 'sans-serif'

# ==========================================
# 1. パラメータ設定 (レポート前提条件と一致)
# ==========================================
NUM_EMPLOYEES = 1000
MONTHS = 24
BASE_WORK_HOURS = 160
MAX_OVERTIME_CAP = 100.0
N_TRIALS = 50 # 試行回数

# 労働分配率 (機会損失計算用: 年収の2倍稼ぐと仮定)
LABOR_SHARE = 0.50

RECRUIT_LEAD_TIME = {'Urban': 5, 'Rural': 10}
REPLACEMENT_PREMIUM = {'S': 1.30, 'A': 1.25, 'B': 1.15, 'C': 1.10, 'D': 1.05}
HIRING_COST_RATE = 0.35 
SPILLOVER_RATE = 0.6 

RANK_PARAMS = {
    'S':  {'Absorption': 1.6, 'Perf_Mult': 1.40},
    'A+': {'Absorption': 1.4, 'Perf_Mult': 1.25},
    'A':  {'Absorption': 1.3, 'Perf_Mult': 1.20},
    'A-': {'Absorption': 1.2, 'Perf_Mult': 1.15},
    'B+': {'Absorption': 1.1, 'Perf_Mult': 1.08},
    'B':  {'Absorption': 1.0, 'Perf_Mult': 1.00},
    'B-': {'Absorption': 0.9, 'Perf_Mult': 0.95},
    'C':  {'Absorption': 0.7, 'Perf_Mult': 0.85},
    'D':  {'Absorption': 0.5, 'Perf_Mult': 0.70}
}
HP_RANKS = ['S', 'A+', 'A', 'A-']

# ==========================================
# 2. クラス定義
# ==========================================
class EmployeeGenerator:
    def __init__(self, n_employees):
        self.n = n_employees

    def generate(self):
        ids = range(self.n)
        ages = np.random.randint(22, 60, self.n)
        tenures = [max(0, age - 22 - np.random.randint(0, 5)) for age in ages]
        
        job_levels = []
        for age in ages:
            base_lvl = min(5, max(1, int((age - 20) / 8)))
            noise = np.random.choice([-1, 0, 1], p=[0.2, 0.6, 0.2])
            job_levels.append(min(5, max(1, base_lvl + noise)))
            
        rating_labels = ['S', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C', 'D']
        probs = [0.03, 0.05, 0.08, 0.10, 0.15, 0.25, 0.15, 0.12, 0.07]
        ratings = np.random.choice(rating_labels, self.n, p=probs)
        branches = np.random.choice(['Urban', 'Rural'], self.n, p=[0.6, 0.4])

        df = pd.DataFrame({
            'Employee_ID': ids,
            'Age': ages,
            'Tenure_Years': tenures,
            'Job_Level': job_levels,
            'Performance_Rating': ratings,
            'Branch_Type': branches,
            'Status': 'Active',
            'Overtime_Hours': 20.0,
        })
        
        df['Current_Salary'] = df.apply(self._calc_internal_salary, axis=1) * 10000 
        df['Compa_Ratio'] = df.apply(self._calculate_gap, axis=1)
        df['Is_HP'] = df['Performance_Rating'].isin(HP_RANKS)
        df['Absorb_Factor'] = df['Performance_Rating'].map(lambda x: RANK_PARAMS[x]['Absorption'])
        return df

    def _calc_internal_salary(self, row):
        return 300 + (row['Age'] * 6) + (row['Tenure_Years'] * 4) + (row['Job_Level'] * 40)

    def _calculate_gap(self, row):
        internal = self._calc_internal_salary(row)
        market_base = {1: 350, 2: 500, 3: 700, 4: 900, 5: 1200}
        market = market_base[row['Job_Level']] * RANK_PARAMS[row['Performance_Rating']]['Perf_Mult']
        return internal / market

# ==========================================
# 3. シミュレーション関数
# ==========================================
def run_single_simulation(initial_df, spillover_rate=SPILLOVER_RATE):
    history = []
    vacancies = []
    cumulative_cash_out = 0 
    cumulative_opp_loss = 0
    current_df = initial_df.copy()
    
    for month in range(MONTHS):
        # --- Step 1: 補充 ---
        new_vacancies = []
        hired_count = 0
        for v in vacancies:
            lead_time = RECRUIT_LEAD_TIME[v['Branch']]
            if v['Months_Open'] >= lead_time:
                hired_count += 1
                old_salary = v['Old_Salary']
                base_rating = v['Rating_Base'][0] 
                premium_rate = REPLACEMENT_PREMIUM.get(base_rating, 1.1)
                new_salary = old_salary * premium_rate
                
                # キャッシュアウト (採用費 + 賃金増分)
                cumulative_cash_out += (new_salary * HIRING_COST_RATE) + (new_salary - old_salary)
            else:
                # 機会損失 (給与 ÷ 労働分配率 ÷ 12ヶ月)
                monthly_value_added = (v['Old_Salary'] / LABOR_SHARE) / 12
                cumulative_opp_loss += monthly_value_added
                
                v['Months_Open'] += 1
                new_vacancies.append(v)
        vacancies = new_vacancies
        
        # --- Step 2: 退職判定 (平時12% -> 負荷時急増モデル) ---
        active_mask = current_df['Status'] == 'Active'
        active_df = current_df[active_mask]
        
        total_spillover = 0
        if len(active_df) > 0:
            risk_financial = np.maximum(0, 1.2 - active_df['Compa_Ratio'])
            sensitivity = np.where(active_df['Is_HP'], 1.5, 1.0)
            calc_ot = np.minimum(active_df['Overtime_Hours'], MAX_OVERTIME_CAP)
            risk_workload = (calc_ot / 80.0) * sensitivity
            
            # 月次離職確率
            monthly_prob = 0.008 + (risk_financial * 0.02) + (risk_workload * 0.02)
            
            random_vals = np.random.rand(len(active_df))
            will_resign = random_vals < monthly_prob
            
            leavers_indices = active_df[will_resign].index
            
            if len(leavers_indices) > 0:
                leavers = current_df.loc[leavers_indices]
                for _, row in leavers.iterrows():
                    vacancies.append({
                        'Branch': row['Branch_Type'], 
                        'Months_Open': 0, 
                        'Old_Salary': row['Current_Salary'],
                        'Rating_Base': row['Performance_Rating']
                    })
                total_spillover = ((BASE_WORK_HOURS + np.minimum(leavers['Overtime_Hours'], MAX_OVERTIME_CAP)) * spillover_rate).sum()
                current_df.loc[leavers_indices, 'Status'] = 'Resigned'

        # --- Step 3: 負の連鎖 ---
        active_mask = current_df['Status'] == 'Active'
        if active_mask.sum() > 0 and total_spillover > 0:
            total_absorb = current_df.loc[active_mask, 'Absorb_Factor'].sum()
            if total_absorb > 0:
                factors = current_df.loc[active_mask, 'Absorb_Factor']
                added = (factors / total_absorb) * total_spillover
                current_df.loc[active_mask, 'Overtime_Hours'] += added
        
        if active_mask.sum() > 0 and hired_count > 0:
            relief = (hired_count * 120.0) / active_mask.sum()
            current_df.loc[active_mask, 'Overtime_Hours'] = np.maximum(
                20.0, current_df.loc[active_mask, 'Overtime_Hours'] - relief
            )

        current_df.loc[active_mask, 'Overtime_Hours'] = np.minimum(
            current_df.loc[active_mask, 'Overtime_Hours'], MAX_OVERTIME_CAP + 20
        )

        # 記録（グラフ用データ）
        active_hp = current_df[(current_df['Status'] == 'Active') & (current_df['Is_HP'])]
        hp_ot = active_hp['Overtime_Hours'].mean() if len(active_hp) > 0 else 0
        urban_surv = len(current_df[(current_df['Status'] == 'Active') & (current_df['Branch_Type'] == 'Urban')])
        rural_surv = len(current_df[(current_df['Status'] == 'Active') & (current_df['Branch_Type'] == 'Rural')])

        history.append({
            'Month': month,
            'HP_Overtime_Avg': hp_ot,
            'Urban_Count': urban_surv,
            'Rural_Count': rural_surv,
            'Cumulative_Cash_Out': cumulative_cash_out / 1000000,
            'Cumulative_Opp_Loss': cumulative_opp_loss / 1000000
        })
        
    return pd.DataFrame(history)

# ==========================================
# 4. 実行と可視化
# ==========================================
print(f"🚀 シミュレーション実行中 (N={N_TRIALS})...")

all_results_cash = []
all_results_opp = []
all_results_hp_ot = []
all_results_urban = []
all_results_rural = []

gen = EmployeeGenerator(NUM_EMPLOYEES)
base_df = gen.generate()

for i in range(N_TRIALS):
    res = run_single_simulation(base_df.copy())
    all_results_cash.append(res['Cumulative_Cash_Out'].values)
    all_results_opp.append(res['Cumulative_Opp_Loss'].values)
    all_results_hp_ot.append(res['HP_Overtime_Avg'].values)
    all_results_urban.append(res['Urban_Count'].values)
    all_results_rural.append(res['Rural_Count'].values)

# 中央値の算出
median_cash = np.median(np.array(all_results_cash), axis=0)
median_opp = np.median(np.array(all_results_opp), axis=0)
median_hp_ot = np.median(np.array(all_results_hp_ot), axis=0)
median_urban = np.median(np.array(all_results_urban), axis=0)
median_rural = np.median(np.array(all_results_rural), axis=0)

# 初期人数（正規化用）
urban_init = median_urban[0]
rural_init = median_rural[0]

# --- グラフ描画 ---
plt.figure(figsize=(18, 5))

# Graph 1: 負の連鎖 (HP残業時間)
plt.subplot(1, 3, 1)
plt.plot(range(MONTHS), median_hp_ot, color='#c0392b', linewidth=2.5, label='HP平均残業時間')
plt.title('負の連鎖: HP層の残業時間推移', fontsize=12)
plt.ylabel('平均残業時間 (h/月)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(y=80, color='orange', linestyle='--', label='過労死ライン(80h)')
plt.legend()

# Graph 2: 組織縮小推移
plt.subplot(1, 3, 2)
plt.plot(range(MONTHS), median_urban / urban_init * 100, label='都市', marker='o', color='#2980b9')
plt.plot(range(MONTHS), median_rural / rural_init * 100, label='地方', marker='x', color='#c0392b')
plt.title('補充遅延による人員維持率', fontsize=12)
plt.ylabel('維持率 (%)')
plt.ylim(0, 110)
plt.legend()
plt.grid(True)

# Graph 3: 財務損失
plt.subplot(1, 3, 3)
plt.fill_between(range(MONTHS), 0, median_cash, color='black', alpha=0.7, label='直接流出額(採用費+賃金増)')
plt.fill_between(range(MONTHS), median_cash, median_cash + median_opp, color='gray', alpha=0.3, label='機会損失(参考)')
plt.plot(range(MONTHS), median_cash, color='black', linewidth=3)

plt.title('累積財務損失 (直接流出額 vs 機会損失)', fontsize=12)
plt.ylabel('損失額 (百万円)')
plt.xlabel('経過月数')
plt.legend(loc='upper left')
plt.grid(True)

plt.tight_layout()
plt.show()

# 最終数値の出力（レポート記載用）
print(f"【最終シミュレーション結果】")
print(f"・直接キャッシュアウト損失: {median_cash[-1]:.0f} 百万円 (現実的なPLヒット)")
print(f"・(参考) 機会損失を含めた総額: {median_cash[-1] + median_opp[-1]:.0f} 百万円")