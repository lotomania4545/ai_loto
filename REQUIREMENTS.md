# Project Requirements - ai_loto

## Phase 1: 要件確定

### 1. 対象となる宝くじ

**Loto 6** (ロト6)

理由:
- 最も基本的で認知度が高い
- データが豊富
- 規則が単純で実装しやすい
- 抽選頻度が適度 (毎週2回)

### 2. 予測単位

**1回の抽選 = 1単位**

- 1抽選回ごとに6個の数字を予測
- 抽選回番号で管理

### 3. 予測対象

**当選数字 (本数字)**

- Loto 6では、抽選機から6個の数字が本数字として抽出される
- ボーナス数字は対象外 (複雑性増加のため)
- 本数字6個を完全予測することが目標

### 4. データ形式

#### 入力形式

```
Draw Number | Date       | Number1 | Number2 | Number3 | Number4 | Number5 | Number6 | Bonus
1          | YYYY-MM-DD | 1       | 5       | 12      | 23      | 34      | 43      | 25
2          | YYYY-MM-DD | 2       | 8       | 15      | 29      | 38      | 44      | 10
...
```

- 抽選番号: 1から始まる連番
- 日付: ISO 8601形式 (YYYY-MM-DD)
- 数字: 1～43の整数 (昇順)
- ボーナス: 1～43の整数 (本数字と重複しない)

#### 保存形式

**CSV** (単純で処理しやすい)

```
.csv
├── data/raw/loto6_raw.csv (元データ)
└── data/processed/loto6_processed.csv (検証済みデータ)
```

または **JSON** (スキーマ検証が容易)

```
data/raw/loto6_raw.json
```

当面はCSVで統一。

### 5. 更新頻度

**自動更新スケジュール**

- Loto 6抽選日: 毎週月曜日と木曜日 (19:30ごろ)
- GitHub Actions実行タイミング: 抽選翌日 09:00 (日本時間)
  - 最新の抽選結果を取得
  - データ検証
  - データ更新
  - 特徴量再生成
  - モデル再学習
  - 次回予測生成

### 6. 最終出力

#### 予測出力フォーマット

```json
{
  "draw_number": 12345,
  "draw_date": "YYYY-MM-DD (予定日)",
  "prediction_generated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "model_version": "v1.0.2",
  "feature_version": "v1.0.1",
  
  "predictions": [
    {
      "rank": 1,
      "label": "Best",
      "numbers": [5, 12, 18, 28, 35, 42],
      "scores": {
        "5": 0.87,
        "12": 0.85,
        "18": 0.82,
        "28": 0.80,
        "35": 0.78,
        "42": 0.75
      },
      "ensemble_score": 0.81,
      "models": {
        "frequency": {"numbers": [...], "score": 0.75},
        "gap": {"numbers": [...], "score": 0.78},
        "ml_model1": {"numbers": [...], "score": 0.85},
        "ml_model2": {"numbers": [...], "score": 0.83}
      }
    },
    {
      "rank": 2,
      "label": "Alternative",
      "numbers": [...],
      "ensemble_score": 0.79
    },
    ...
  ],
  
  "backtest_summary": {
    "average_hits": 2.34,
    "hit_3_or_more_rate": 0.18,
    "best_model": "ensemble",
    "performance": "Above baseline"
  }
}
```

#### 実績比較出力フォーマット

```json
{
  "draw_number": 12344,
  "actual_numbers": [3, 15, 22, 31, 39, 41],
  "bonus": 18,
  "predictions_submitted": [
    {
      "rank": 1,
      "predicted": [5, 12, 18, 28, 35, 42],
      "hits": [18],
      "hit_count": 1
    },
    {
      "rank": 2,
      "predicted": [3, 14, 22, 30, 38, 41],
      "hits": [3, 22, 41],
      "hit_count": 3
    }
  ],
  "best_hit_count": 3,
  "model_performance": "Above average",
  "comparison_generated_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

### 7. 通知方法

#### GitHub Issues

自動で予測結果をIssueとして記録

```
Title: [Prediction] Draw #12345 - Generated at 2026-08-11

Body:
- 予測数字
- スコア
- 使用モデル
- バックテスト成績
- 前回的中数
```

#### GitHub Discussions

予測と実績の比較をDiscussionに記録

```
Title: [Result] Draw #12344 - 3 hits!

Body:
- 実際の数字
- 予測の数字
- 的中数
- モデル別成績
```

#### Email通知 (オプション)

- GitHub Secretsで通知先を管理
- 重要な結果のみ送信

#### Webhook通知 (オプション)

- Slack/Discord/LINE等への統合
- 後で実装可能な構造

当面は**GitHub Issues & Discussions**で統一。

### 8. 自動実行方法

#### GitHub Actions Workflows

**Workflow 1: data_update (毎日09:00実行)**

```
1. 最新データソースを確認
2. 新規抽選結果があるか判定
3. あれば取得・検証
4. データを更新
5. 処理状況をログ出力
```

**Workflow 2: train_predict (新データ検出時実行)**

```
1. データの検証
2. 特徴量再生成
3. 全モデルを再学習
4. バックテスト実行
5. モデル評価
6. アンサンブル重み決定
7. 次回予測生成
8. 予測をIssueに記録
9. Discussionに投稿
```

**Workflow 3: result_fetch (抽選翌々日10:00実行)**

```
1. 最新の抽選結果を取得
2. 前回の予測と比較
3. 的中数を計算
4. 成績をDiscussionに記録
5. モデル成績を更新
```

**Workflow 4: retrain (結果確定後実行)**

```
1. 新しいデータを学習データに追加
2. 全モデルを再学習
3. バックテスト実行
4. 次回予測を生成
5. 予測を記録
```

---

## 要件サマリー

| 項目 | 仕様 |
|------|------|
| **対象宝くじ** | Loto 6 |
| **予測単位** | 1抽選回 |
| **予測対象** | 本数字6個 |
| **データ形式** | CSV (data/raw/, data/processed/) |
| **更新頻度** | 毎週2回 (月木抽選) |
| **自動更新** | 毎日09:00 (GitHub Actions) |
| **出力形式** | JSON + Issues/Discussions |
| **通知方法** | GitHub Issues/Discussions |
| **自動実行** | 4つのWorkflow |
| **目標** | 継続的な精度向上と完全自動化 |

---

*Last updated: 2026-08-11*
