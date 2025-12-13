import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

# ==============================================================================
# Simulation Configuration
# 目的: 「負の連鎖」と「インフレによる財務損失」を定量化する
# ==============================================================================

NUM_EMPLOYEES = 1000
MONTHS = 24
BASE_WORK_HOURS = 160

# 採用リードタイム（月）：都市5ヶ月、地方10ヶ月（現実的な遅延を反映）
RECRUIT_LEAD_TIME = {'Urban': 5, 'Rural': 10}

# 外部労働市場の賃金インフレ率（Replacement Premium）
# 既存社員が辞めて同等能力者を雇う場合のコスト増
REPLACEMENT_PREMIUM = {
    'S': 1.30, 'A': 1.25, 'B': 1.15, 'C': 1.10, 'D': 1.05
}

# 採用エージェントフィー率
HIRING_COST_RATE = 0.35 

# 業務波及率（退職者の業務が現場に残る割合）
SPILLOVER_RATE = 0.7

# 評価ランク別パラメータ
# Absorption: 業務吸収係数（優秀な人ほど仕事を被る）
# Perf_Mult: 市場価値係数（S評価は市場価値が高い）
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

# ==============================================================================
# Employee Data Generator
# ==============================================================================
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
        return df

    def _calc_internal_salary(self, row):
        return 300 + (row['Age'] * 6) + (row['Tenure_Years'] * 4) + (row['Job_Level'] * 40)

    def _calculate_gap(self, row):
        internal = self._calc_internal_salary(row)
        market_base = {1: 350, 2: 500, 3: 700, 4: 900, 5: 1200}
        market = market_base[row['Job_Level']] * RANK_PARAMS[row['Performance_Rating']]['Perf_Mult']
        return internal / market

# ==============================================================================
# Simulation Engine
# ==============================================================================
def run_simulation(df):
    history = []
    vacancies = []
    financial_loss_total = 0 
    current_df = df.copy()
    
    for month in range(MONTHS):
        # Step 1: Hiring & Cost Calculation
        new_vacancies = []
        hired_count = 0
        for v in vacancies:
            lead_time = RECRUIT_LEAD_TIME[v['Branch']]
            if v['Months_Open'] >= lead_time:
                hired_count += 1
                # Calculate Inflation Impact
                old_salary = v['Old_Salary']
                premium_rate = REPLACEMENT_PREMIUM.get(v['Rating_Base'], 1.1)
                new_salary = old_salary * premium_rate
                
                cost_salary_increase = new_salary - old_salary
                cost_hiring_fee = new_salary * HIRING_COST_RATE
                
                financial_loss_total += cost_hiring_fee + cost_salary_increase
            else:
                # Opportunity Loss
                financial_loss_total += (v['Old_Salary'] / 12) * 1.5
                v['Months_Open'] += 1
                new_vacancies.append(v)
        vacancies = new_vacancies
        
        # Step 2: Attrition Logic
        leavers = []
        spillover_hours_total = 0
        for idx, row in current_df[current_df['Status'] == 'Active'].iterrows():
            risk_financial = max(0, 1.2 - row['Compa_Ratio'])
            sensitivity = 1.5 if row['Is_HP'] else 1.0
            risk_workload = (row['Overtime_Hours'] / 80) * sensitivity
            
            prob = (risk_financial * 0.4) + (risk_workload * 0.6)
            prob = min(0.35, max(0, prob - 0.1))
            
            if random.random() < prob:
                current_df.at[idx, 'Status'] = 'Resigned'
                leavers.append(row)
                load = (BASE_WORK_HOURS + row['Overtime_Hours']) * SPILLOVER_RATE
                spillover_hours_total += load
                vacancies.append({
                    'Branch': row['Branch_Type'], 
                    'Months_Open': 0, 
                    'Old_Salary': row['Current_Salary'],
                    'Rating_Base': row['Performance_Rating'][0] if row['Performance_Rating'] in REPLACEMENT_PREMIUM else 'B'
                })

        # Step 3: Spillover (The Death Spiral)
        active_mask = current_df['Status'] == 'Active'
        if active_mask.sum() > 0 and spillover_hours_total > 0:
            current_df.loc[active_mask, 'Absorb_Score'] = current_df.loc[active_mask, 'Performance_Rating'].apply(
                lambda x: RANK_PARAMS[x]['Absorption']
            )
            total_score = current_df.loc[active_mask, 'Absorb_Score'].sum()
            added_hours = (current_df.loc[active_mask, 'Absorb_Score'] / total_score) * spillover_hours_total
            current_df.loc[active_mask, 'Overtime_Hours'] += added_hours
            
            if hired_count > 0:
                relief = (hired_count * 120) / active_mask.sum()
                current_df.loc[active_mask, 'Overtime_Hours'] = np.maximum(
                    20, current_df.loc[active_mask, 'Overtime_Hours'] - relief
                )

        # Step 4: Recording
        active_df = current_df[current_df['Status'] == 'Active']
        hp_ot = active_df[active_df['Is_HP']]['Overtime_Hours'].mean() if not active_df[active_df['Is_HP']].empty else 0
        urban_surv = len(active_df[active_df['Branch_Type'] == 'Urban'])
        rural_surv = len(active_df[active_df['Branch_Type'] == 'Rural'])
        
        history.append({
            'Month': month,
            'HP_Overtime_Avg': hp_ot,
            'Urban_Count': urban_surv,
            'Rural_Count': rural_surv,
            'Cumulative_Loss_Million': financial_loss_total / 1000000
        })
        
    return pd.DataFrame(history)

# ==============================================================================
# Visualization (Example Output Generation)
# ==============================================================================
gen = EmployeeGenerator(NUM_EMPLOYEES)
initial_df = gen.generate()
hist_df = run_simulation(initial_df)

plt.figure(figsize=(18, 5))

# Graph 1: The Death Spiral
plt.subplot(1, 3, 1)
sns.lineplot(data=hist_df, x='Month', y='HP_Overtime_Avg', color='#c0392b', linewidth=2.5)
plt.title('負の連鎖: HP層の残業時間急増', fontsize=12)
plt.ylabel('平均残業時間 (h/月)')
plt.grid(True, linestyle='--', alpha=0.7)

# Graph 2: Regional Collapse
urban_init = hist_df['Urban_Count'].iloc[0]
rural_init = hist_df['Rural_Count'].iloc[0]
plt.subplot(1, 3, 2)
plt.plot(hist_df['Month'], hist_df['Urban_Count']/urban_init*100, label='都市 (リード5ヶ月)', marker='o', color='#2980b9')
plt.plot(hist_df['Month'], hist_df['Rural_Count']/rural_init*100, label='地方 (リード10ヶ月)', marker='x', color='#c0392b')
plt.title('補充遅延による組織縮小推移', fontsize=12)
plt.ylabel('人員維持率 (%)')
plt.legend()
plt.grid(True)

# Graph 3: Financial Loss (Inflation Impact)
plt.subplot(1, 3, 3)
plt.fill_between(hist_df['Month'], hist_df['Cumulative_Loss_Million'], color='gray', alpha=0.3)
plt.plot(hist_df['Month'], hist_df['Cumulative_Loss_Million'], color='black', linewidth=2)
plt.title('累積損失額 (採用費 + 賃金インフレ差額)', fontsize=12)
plt.ylabel('損失額 (百万円)')
plt.xlabel('経過月数')
plt.grid(True)

plt.tight_layout()
plt.show()