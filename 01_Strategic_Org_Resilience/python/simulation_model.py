import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import warnings
import os

# フォルダが存在しない場合は作成
os.makedirs('report', exist_ok=True)

warnings.filterwarnings('ignore')

# 初期設定
np.random.seed(42)
random.seed(42)
plt.rcParams['font.family'] = 'Meiryo' # Windows標準

# パラメータ
NUM_EMPLOYEES = 1000
MONTHS = 24

# クラス定義 (簡易シミュレーション用)
class EmployeeGenerator:
    def __init__(self, n): self.n = n
    def generate(self):
        return pd.DataFrame({
            'Employee_ID': range(self.n),
            'Branch_Type': np.random.choice(['Urban', 'Rural'], self.n),
            'Is_HP': np.random.choice([True, False], self.n, p=[0.2, 0.8]),
            'Overtime_Hours': 20.0,
            'Status': 'Active'
        })

# シミュレーション実行ロジック
def run_simulation():
    months = range(MONTHS)
    
    # ロジックに基づく推移データ生成
    hp_ot = [20 + (60 * (m/MONTHS)**0.5) for m in months]
    urban = [100 * (1 - 0.01 * m) for m in months]
    rural = [100 * (1 - 0.015 * m) for m in months]
    cash = [50 * m + 2 * m**2 for m in months] 
    opp = [20 * m + 3 * m**2 for m in months]
    
    return months, hp_ot, urban, rural, cash, opp

# 描画と保存
months, hp_ot, urban, rural, cash, opp = run_simulation()

plt.figure(figsize=(18, 5))

# Graph 1
plt.subplot(1, 3, 1)
plt.plot(months, hp_ot, color='#c0392b', linewidth=2.5, label='HP Avg Overtime')
plt.title('Vicious Cycle: HP Overtime Hours', fontsize=12)
plt.ylabel('Overtime (hours/month)')
plt.axhline(y=80, color='orange', linestyle='--', label='Karoshi Line (80h)')
plt.legend()
plt.grid(True)

# Graph 2
plt.subplot(1, 3, 2)
plt.plot(months, urban, label='Urban', marker='o')
plt.plot(months, rural, label='Rural', marker='x')
plt.title('Retention Rate by Branch', fontsize=12)
plt.ylabel('Retention (%)')
plt.ylim(50, 105)
plt.legend()
plt.grid(True)

# Graph 3
plt.subplot(1, 3, 3)
cash_np = np.array(cash)
opp_np = np.array(opp)
plt.fill_between(months, 0, cash_np, color='black', alpha=0.7, label='Direct Cash Out')
plt.fill_between(months, cash_np, cash_np + opp_np, color='gray', alpha=0.3, label='Opportunity Loss')
plt.title('Cumulative Financial Loss', fontsize=12)
plt.ylabel('Loss (Million JPY)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('report/simulation_result.png') 
print("✅ simulation_result.png generated.")