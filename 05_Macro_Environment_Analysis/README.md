  # 📘 日本の大学経営における構造的課題の定量分析
Quantitative Analysis of Structural Issues in University Management

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Analysis](https://img.shields.io/badge/Analysis-University%20IR-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 👤 Author
**Keisuke Nakamura (keisuke-data-lab)** *Data Analyst / University IR Specialist*

現場データの収集・整理から、経営層の意思決定につながるモデル構築までを一貫して担当する実務家です。

* **経歴:** 帝国データバンクおよびJCBにて、大規模データ分析（1,000万件超）や業務改善プロジェクトを主導。
* **分析実績:** 医療・人事領域における人材構造分析、管理職比率シミュレーション等。
* **現在の取り組み:** **Python × BI × 生成AI** を活用した、大学IRのための即応的分析基盤の構築。

➡ **「複雑な現場データを、学内ステークホルダーが理解できる“意思決定モデル”に翻訳する能力」** を強みとしています。

---

## 📌 プロジェクトの目的 (Purpose)
本プロジェクトは、大学経営における**「定員割れリスク」および「ガバナンス不全」**が財務に与える影響を、定量的に評価できるモデルとして再現することを目的としています。

IR担当者や経営層が、以下のリスクを即座に試算できる **Python モデル** を構築しました。
* **定員割れリスク:** 志願倍率や歩留まりの変動が与えるインパクト
* **ガバナンス不全:** 意思決定の遅延が招くブランド毀損
* **財務への影響:** 上記要因による授業料収入の損失額

---

## 📄 レポートの概要（3行まとめ）

| 要素 | 内容 |
| :--- | :--- |
| **課題定義** | ガバナンス不全と定員管理の遅れが生む**財務リスク**を明確化 |
| **分析手法** | 学部ごとの**ブランド毀損率（η）**の変動を中心に感度分析を実施 |
| **成果** | IR担当者が自大学の数字で即試算できる**“数式モデル＋Pythonコード”**を構築 |

---

## 📂 成果物 (Outputs)

### 📄 [詳細分析レポート (PDF)](docs/university_management_report.pdf)
大学のガバナンス構造・組織課題・財務リスクを、PESTEL と 7S フレームワークを用いて論じた包括的レポートです（A4 4ページ）。
👉 **[docs/university_management_report.pdf](docs/university_management_report.pdf)**

### 🐍 [財務損失シミュレーション (Python Notebook)](./university_financial_loss_simulation.ipynb)

* 志願者減少率（η）が授業料収入に与える影響を計算
* 感度分析（Scenario Analysis）をそのまま実行できる構造
* IR担当者が自大学の定員・授業料を入力すれば、そのまま利用可能

---

## 🔍 分析アプローチ (Methodology)

### 1. ガバナンス視点での課題抽出
大学経営において、数値（財務）の悪化は「結果」に過ぎず、真の原因は「組織構造（ガバナンス）」にあります。本分析では以下の視点で課題を定義しました。

* **意思決定の遅延:** 理事会・評議員会の役割不均衡
* **専門職の不在:** データに基づく経営判断（IR）を行う専門人材の不足
* **組織のサイロ化:** 学部ごとの個別最適による全学的戦略の欠如

これらは、**志願倍率の低下**、**歩留まりの悪化**、**入学定着率 (Retention) の低下** を招き、最終的に財務を直撃します。

### 2. 定量評価モデル (Financial Loss Model)
ブランド毀損による影響を「損失額 $L$」として可視化するために、以下の簡易モデルを構築しました。数学的な専門知識がない事務職員・教員でも理解しやすい変数を採用しています。

$$L = N \times T \times \eta$$

この数式は、Python Notebook 内の関数 `loss_simulation()` として実装されています。

| 変数 | 定義 | 意味 (IR的視点) |
| :--- | :--- | :--- |
| **$L$** | **Loss (損失額)** | 経営への直接的な財務インパクト |
| **$N$** | **Number (学生数)** | 定員規模（学部の規模感） |
| **$T$** | **Tuition (授業料)** | 学費単価（収益構造のベース） |
| **$\eta$** | **Eta (減少率)** | ブランド毀損による入学者減少率 |

---

## 🛠 使用技術・ツール (Tech Stack)
大学IRの実務において、再現性と透明性を担保するために以下の技術を選定しました。

* **Analysis & Logic:** PESTEL Framework, McKinsey 7S Framework
* **Simulation:** Python (Pandas, Matplotlib)
* **Tools:** GitHub, VS Code, Generative AI (Co-pilot)

---
© 2025 Keisuke Nakamura | [GitHub Profile](https://github.com/keisuke-data-lab)
