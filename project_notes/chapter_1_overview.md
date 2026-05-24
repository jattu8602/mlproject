# Chapter 1: Project Overview — The Big Picture

## What Are We Building?
A **Math Score Predictor** — given 7 inputs about a student, predict their math score.

```
Inputs: [gender, race, parental_edu, lunch, test_prep, reading, writing]
                                                      ↓
                                              [MATH SCORE]
```

## The 4-Stage Pipeline

```
Raw CSV → Data Ingestion → Data Transformation → Model Training → Web App
```

### Stage 1: Data Ingestion
- Read the CSV file
- Split data into **80% training** (for learning) and **20% testing** (for evaluation)
- Save all copies to `artifacts/` folder

### Stage 2: Data Transformation
- Convert text categories to numbers (One-Hot Encoding)
- Fill missing values (Imputer)
- Scale all numbers to similar ranges (StandardScaler)
- Save the preprocessor as `preprocessor.pkl` for reuse

### Stage 3: Model Training
- Try 7 different ML algorithms
- Pick the one with the best R² score
- Save the best model as `model.pkl`

### Stage 4: Prediction Pipeline + Web App
- Load saved model and preprocessor
- Accept user input from a web form
- Return predicted math score

## Why This Modular Structure?
Each piece is a separate file. If you need to change how data is cleaned, you only touch `data_transformation.py` — NOT the model trainer or the web app. This is **Separation of Concerns**.

## Key Concepts Learned

| Concept | Explanation |
|---------|-------------|
| **Train/Test Split** | 80% for learning, 20% for testing generalization |
| **Overfitting** | Model memorizes instead of learns (high train score, low test score) |
| **One-Hot Encoding** | Converting categories to 0s and 1s (not an ML algorithm!) |
| **Modularity** | Each component is independent and swappable |
