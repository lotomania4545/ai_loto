# ai_loto - AI Lottery Prediction System

Complete automated AI-powered lottery prediction system with:
- Automatic data acquisition
- Data validation & preprocessing
- Feature engineering
- Multiple ML models
- Backtesting with Walk Forward validation
- Ensemble predictions
- Automated retraining & prediction
- GitHub Actions orchestration

## Project Status

🚧 **Under Development** - Phase 1: Requirements Definition

---

## Architecture Overview

```
Data Acquisition
    ↓
Validation & Preprocessing
    ↓
Feature Engineering
    ↓
Model Training (Multiple models)
    ↓
Backtesting & Evaluation
    ↓
Ensemble & Prediction
    ↓
Notification
    ↓
Actual Result Comparison
    ↓
Retrain Loop
```

## Directory Structure

```
ai_loto/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── acquisition.py
│   │   └── validation.py
│   │
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   └── processor.py
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   └── engineering.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── baseline.py
│   │   ├── frequency.py
│   │   ├── gap.py
│   │   ├── ensemble.py
│   │   └── ml/
│   │       ├── __init__.py
│   │       ├── model1.py
│   │       └── model2.py
│   │
│   ├── backtest/
│   │   ├── __init__.py
│   │   └── engine.py
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── metrics.py
│   │
│   ├── prediction/
│   │   ├── __init__.py
│   │   └── predictor.py
│   │
│   ├── notification/
│   │   ├── __init__.py
│   │   └── notifier.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── helpers.py
│
├── tests/
│   ├── __init__.py
│   ├── test_data.py
│   ├── test_validation.py
│   ├── test_features.py
│   ├── test_models.py
│   ├── test_backtest.py
│   └── test_prediction.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── features/
│   ├── predictions/
│   └── results/
│
├── configs/
│   ├── config.yaml
│   └── model_config.yaml
│
├── .github/
│   └── workflows/
│       ├── data_update.yml
│       ├── train_predict.yml
│       ├── evaluate.yml
│       └── result_compare.yml
│
└── notebooks/
    └── (exploratory notebooks - optional)
```

---

## Setup & Installation

```bash
# Clone repository
git clone https://github.com/lotomania4545/ai_loto.git
cd ai_loto

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

---

## Configuration

See `configs/config.yaml` for:
- Target lottery (Loto 6, Loto 7, Mini Loto, etc.)
- Data source URLs
- Feature parameters
- Model configurations
- Backtest settings
- Ensemble weights
- Notification settings

---

## GitHub Actions Workflows

### 1. data_update.yml
- Scheduled data acquisition
- Data validation
- Update historical data

### 2. train_predict.yml
- Feature engineering
- Model training on new data
- Backtesting
- Model evaluation
- Model comparison
- Ensemble weight determination
- Generate next prediction
- Send notification

### 3. evaluate.yml
- Compare prediction with actual result
- Update model performance history
- Model version tracking

### 4. result_compare.yml
- Fetch actual lottery result
- Compare with predictions
- Calculate hit count
- Update model metrics

---

## Development

### Phase Checklist

- [ ] Phase 1: Requirements Definition
- [ ] Phase 2: Architecture Design
- [ ] Phase 3: Directory Structure
- [ ] Phase 4: Dependencies
- [ ] Phase 5-8: Data Acquisition & Storage
- [ ] Phase 9-21: Data Analysis & Features
- [ ] Phase 22-30: Models & Baselines
- [ ] Phase 31-38: Backtesting & Evaluation
- [ ] Phase 39-44: Ensemble & Generation
- [ ] Phase 45-49: Prediction & Retraining
- [ ] Phase 50-67: Automation & Testing
- [ ] Phase 68: Final Report

---

## Running Locally

### Update data
```bash
python -m src.data.acquisition
```

### Validate data
```bash
python -m src.data.validation
```

### Generate features
```bash
python -m src.features.engineering
```

### Train models & generate prediction
```bash
python -m src.models.train_predict
```

### Backtest
```bash
python -m src.backtest.engine
```

### Run tests
```bash
pytest tests/
```

---

## Testing

All components have unit tests:
- Data acquisition & validation
- Feature engineering
- Models
- Backtesting
- Ensemble
- Prediction
- Notification

---

## Data Format

All data files are in consistent format (details in config.yaml).

Data flow:
```
data/raw/ (Original data)
    ↓
data/processed/ (Validated & normalized)
    ↓
data/features/ (Generated features)
    ↓
data/predictions/ (Model predictions)
    ↓
data/results/ (Comparison results)
```

---

## Monitoring & Logs

All operations produce logs for troubleshooting:
- Data updates
- Validation failures
- Training progress
- Model performance
- Prediction generation
- Notification delivery

---

## Security

- No secrets in source code
- GitHub Secrets for sensitive info
- Secure notification channels
- Data validation at every step

---

## License

(To be determined)

---

## Author

lotomania4545

---

*Last updated: 2026-08-11*
