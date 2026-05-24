# Chapter 5: Model Training

## What happens here?
The transformed data (all numbers, same scale) is fed into 7 different ML algorithms. Each one tries to find patterns. The best one gets saved as `artifacts/model.pkl`.

## Unpacking the Array
After data_transformation, data is stored as: `[feature1, feature2, ..., featureN, math_score]`
- All columns **except last** = features (X)
- **Last column** = target (y = math_score)

We slice them with numpy:
```python
train_array[:, :-1]   # all rows, all cols except last → X_train
train_array[:, -1]    # all rows, only last column → y_train
```

## The 7 Models Tried
| Model | Type |
|-------|------|
| Linear Regression | Simple baseline — draws a straight line |
| Decision Tree | Single tree of if/else rules |
| Random Forest | Many decision trees averaged |
| Gradient Boosting | Trees built sequentially, each fixing previous errors |
| XGBoost | Optimized gradient boosting (fast) |
| CatBoost | Handles categories natively |
| AdaBoost | Combines many weak models |

## GridSearchCV
```python
GridSearchCV(model, param_grid, cv=3)
```
- Tries every combination of hyperparameters
- `cv=3` = 3-fold cross-validation (split into 3, train on 2, validate on 1 — repeat 3 times)
- Picks the combination with best average score

## Hyperparameters (params)
Different knobs for each model:
- `n_estimators`: number of trees (Random Forest, Boosting)
- `learning_rate`: how fast the model learns
- `depth`: how deep the trees grow (CatBoost)
- `criterion`: how the tree measures quality (Decision Tree)

## R² Score
- **1.0** = perfect prediction
- **0.0** = as good as guessing the average
- **< 0** = worse than guessing
- Threshold: reject any model scoring below 0.6

## Saving the Model
```python
save_object('artifacts/model.pkl', best_model)
```
Pickles the best trained model so we can load it later for web predictions.

## Full Training Flow
```
data_ingestion.py  →  train.csv, test.csv
         ↓
data_transformation.py  →  train_arr, test_arr + preprocessor.pkl
         ↓
model_trainer.py  →  model.pkl (best of 7)
```
