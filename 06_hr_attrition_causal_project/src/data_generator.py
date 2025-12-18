import pandas as pd
import numpy as np
import random
import os

# シード値の固定（再現性確保）
np.random.seed(42)
random.seed(42)

def generate_hr_data(n_employees=1500, n_months=36):
    """
    設計書に基づき、離職予測・因果推論用の人事データを生成する
    """
    print(f"Generating data for {n_employees} employees over {n_months} months...")
    
    # ---------------------------------------------------------
    # 1. 従業員属性 (Time-invariant)
    # ---------------------------------------------------------
    ids = [f'EMP_{i:04d}' for i in range(1, n_employees + 1)]
    
    data_list = []
    
    for emp_id in ids:
        # 基本属性
        gender = np.random.choice(['M', 'F'], p=[0.6, 0.4])
        age_base = int(np.random.normal(35, 8)) # 平均35歳
        age_base = max(22, min(60, age_base))
        
        education = np.random.choice(['HS', 'BA', 'MA', 'PhD'], p=[0.1, 0.6, 0.25, 0.05])
        job_family = np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR', 'Admin'], p=[0.3, 0.3, 0.15, 0.05, 0.2])
        
        # ---------------------------------------------------------
        # 2. パネルデータ生成 (Time-variant)
        # ---------------------------------------------------------
        # 初期状態の設定
        base_salary = np.random.normal(600, 100) if job_family == 'Engineering' else np.random.normal(500, 80)
        tenure_months = np.random.randint(0, 120) # 勤続月数
        
        for month in range(1, n_months + 1):
            current_age = age_base + (month // 12)
            tenure = tenure_months + month
            
            # ランダム要素・季節性の追加
            overtime = max(0, np.random.normal(20, 10)) # 残業時間
            if job_family == 'Engineering': overtime += 10 # エンジニアは残業多め
            
            # 評価スコア (1-5)
            performance = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.1, 0.5, 0.25, 0.1])
            
            # 心理指標 (潜在変数)
            # 残業が多いとBurnoutしやすく、Engagementが下がる
            burnout = (overtime / 100) + np.random.normal(0, 0.05)
            engagement = 0.5 + (0.1 * performance) - (0.2 * burnout) + np.random.normal(0, 0.05)
            
            # 施策介入
            # 研修：ランダムに発生、ただし若手・低パフォーマンスだと受けさせられる確率微増
            training_flag = 0
            if np.random.random() < 0.05: 
                training_flag = 1
            
            # 給与改定：年度末(12の倍数月)に発生可能性
            salary_change = 0
            if month % 12 == 0 and performance >= 4:
                salary_change = 1
                base_salary *= 1.05 # 昇給
            
            # ---------------------------------------------------------
            # 3. 離職フラグ生成 (Outcome)
            # ---------------------------------------------------------
            # ロジスティックな確率生成（ここが因果の正解データになります）
            logit = (
                -4.0 
                + 2.5 * burnout           # 燃え尽きは離職へ
                - 1.5 * engagement        # エンゲージメントは抑制
                - 0.8 * salary_change     # 昇給は抑制
                - 0.5 * training_flag     # 研修も抑制（因果効果）
                + 0.02 * overtime         # 残業過多
            )
            prob_attrition = 1 / (1 + np.exp(-logit))
            
            attrition_flag = 0
            if np.random.random() < prob_attrition:
                attrition_flag = 1
            
            # データ格納
            row = {
                'employee_id': emp_id,
                'month': month,
                'age': current_age,
                'gender': gender,
                'education': education,
                'job_family': job_family,
                'tenure_months': tenure,
                'base_salary': round(base_salary, 1),
                'overtime_hours': round(overtime, 1),
                'performance_score': performance,
                'burnout_index': round(burnout, 2),
                'engagement_score': round(engagement, 2),
                'training_participation': training_flag,
                'salary_change_flag': salary_change,
                'attrition_flag': attrition_flag
            }
            data_list.append(row)
            
            # 離職したらその人のデータは終了
            if attrition_flag == 1:
                break
                
    df = pd.DataFrame(data_list)
    return df

if __name__ == "__main__":
    # 出力先ディレクトリの確認
    output_dir = "../data"
    if not os.path.exists(output_dir):
        # 実行場所によっては ../data が見つからない場合があるのでカレントを見る
        if os.path.exists("data"):
            output_dir = "data"
        else:
            os.makedirs(output_dir, exist_ok=True)

    print("データ生成を開始します...")
    df = generate_hr_data()
    
    output_path = os.path.join(output_dir, "simulated_hr_data.csv")
    df.to_csv(output_path, index=False)
    print(f"完了: {len(df)}行のデータを {output_path} に保存しました。")