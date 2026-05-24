# ML Project — Interview Questions & Answers

Comprehensive Q&A from basic to advanced with code references.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Structure & Setup](#2-project-structure--setup)
3. [Exception Handling & Logging](#3-exception-handling--logging)
4. [Data Ingestion](#4-data-ingestion)
5. [Data Transformation](#5-data-transformation)
6. [Model Training](#6-model-training)
7. [Prediction Pipeline](#7-prediction-pipeline)
8. [Flask Web App](#8-flask-web-app)
9. [Docker & Deployment](#9-docker--deployment)
10. [ML Theory](#10-ml-theory)

---

## 1. Project Overview

### Q1: What does this project do?

**A:** It predicts a student's math score based on 7 input features (gender, race/ethnicity, parental education level, lunch type, test preparation course, reading score, writing score). It's a regression problem using scikit-learn, XGBoost, and CatBoost.

### Q2: What is the overall architecture?

**A:** Modular pipeline with 4 stages:
1. **Data Ingestion** — load CSV, train/test split
2. **Data Transformation** — encode categories, scale numbers, handle missing values
3. **Model Training** — try 7 algorithms with GridSearchCV, pick best
4. **Prediction Pipeline** — load saved model + preprocessor for inference

Wrapped in a Flask web app for user interaction.

### Q3: What type of ML problem is this?

**A:** Supervised regression — the target `math_score` is a continuous numerical value.

---

## 2. Project Structure & Setup

### Q4: What is `setup.py` and why is it needed?

**A:** It makes the project installable as a Python package using `find_packages()`. When `pip install -e .` runs, all folders with `__init__.py` become importable. This allows `from src.components.data_ingestion import DataIngestion` to work from anywhere.

**Reference:** `setup.py:16-22`

### Q5: How does `setup.py` read requirements?

**A:** The `get_requirements()` function reads `requirements.txt`, strips newlines, and removes `-e .` (which only exists for editable install, not actual pip dependency).

**Reference:** `setup.py:6-13`

### Q6: What does `-e .` in requirements.txt do?

**A:** It triggers the `setup.py` to install the project in editable/development mode. It's removed from the actual list of dependencies before passing to `install_requires`.

**Reference:** `setup.py:4,11-12`

---

## 3. Exception Handling & Logging

### Q7: How does the custom exception handler work?

**A:** `CustomException` extends Python's `Exception`. It uses `sys.exc_info()` to extract the traceback, then gets the filename and line number where the error occurred. The error message format: `"Error in [filename] line [number] message [error]"`.

**Reference:** `src/exception.py:5-21`

### Q8: How does the logger work?

**A:** It creates a timestamped log file (format: `MM_DD_YYYY_HH_MM_SS.log`) inside a `logs/` directory. Uses `logging.basicConfig` with format `[time] line_no name - LEVEL - message`. Every call to `logging.info()`, `logging.error()`, etc. writes to this file.

**Reference:** `src/logger.py:1-16`

### Q9: Why both exception handling and logging?

**A:** Logging tells you what happened and when (traceability). Exception handling tells you where it broke and why (debugging). They work together — exceptions are logged, and logs include exception context.

---

## 4. Data Ingestion

### Q10: What is the `@dataclass` decorator used for in `DataIngestionConfig`?

**A:** It auto-generates `__init__()`, `__repr__()`, and `__eq__()` methods. Instead of writing a full class with constructor, you just declare variables with type hints. It stores file paths for artifacts.

**Reference:** `src/components/data_ingestion.py:9-13`

### Q11: Why separate Config class from the main class?

**A:** **Separation of concerns.** Config stores "what" (paths, parameters). Main class handles "how" (the logic). If paths change, you edit only the Config without touching the logic.

**Reference:** `src/components/data_ingestion.py:9-17`

### Q12: What does `os.makedirs(..., exist_ok=True)` do?

**A:** Creates a directory. `exist_ok=True` means no error if it already exists. Without it, trying to create an existing directory would raise `FileExistsError`.

**Reference:** `src/components/data_ingestion.py:25`

### Q13: Why `random_state=42` in train_test_split?

**A:** Ensures reproducibility. Without a fixed seed, every run produces a different random split. `42` is the "Answer to the Ultimate Question of Life, the Universe, and Everything" (convention).

**Reference:** `src/components/data_ingestion.py:30`

### Q14: Why separate train and test sets?

**A:** To evaluate **generalization**. The model learns from train data (80%), then we test on unseen test data (20%). If performance is similar on both, the model generalizes well. High train + low test = **overfitting**.

**Reference:** `src/components/data_ingestion.py:30`

### Q15: What does `initiate_data_ingestion` return and why?

**A:** It returns the file paths of train.csv and test.csv. These paths are passed to the next stage (data_transformation) so it knows where to find the data. This enables the modular pipeline.

**Reference:** `src/components/data_ingestion.py:37-40`

---

## 5. Data Transformation

### Q16: Why can't we feed raw data directly to ML models?

**A:** ML algorithms only understand **numbers**, not text. Raw data has:
- Categorical text (gender, race) → needs encoding
- Missing values → needs imputation
- Different scales (scores 0-100 vs binary categories) → needs scaling

**Reference:** `src/components/data_transformation.py:29-50`

### Q17: What is OneHotEncoder?

**A:** It converts categorical values into binary columns. For `gender: ["male", "female"]`, it creates two columns: `gender_male` (1 or 0) and `gender_female` (1 or 0). After encoding, our 5 categorical columns expand into ~20 binary columns.

**Reference:** `src/components/data_transformation.py:48`

### Q18: What does StandardScaler do?

**A:** Standardizes features by removing the mean and scaling to unit variance. Formula: `(x - mean) / std`. Ensures all features have comparable ranges so models don't unfairly weight larger numbers.

**Reference:** `src/components/data_transformation.py:43,49`

### Q19: Why use `SimpleImputer(strategy="median")` for numerical and `"most_frequent"` for categorical?

**A:** 
- **Median** — robust to outliers (unlike mean). Suitable for scores.
- **Most_frequent** — for categories, the most common value is the best guess. You can't take "median" of "male"/"female".

**Reference:** `src/components/data_transformation.py:42,47`

### Q20: What is scikit-learn Pipeline?

**A:** Chains multiple transformers into a single unit. Steps execute sequentially — output of step 1 feeds into step 2. Ensures consistent application order and reduces code duplication.

**Reference:** `src/components/data_transformation.py:41-50`

### Q21: What is ColumnTransformer?

**A:** Applies different transformations to different columns. In our project:
- Numerical columns → Imputer + Scaler
- Categorical columns → Imputer + OneHot + Scaler

**Reference:** `src/components/data_transformation.py:52-55`

### Q22: What is the difference between `fit_transform` and `transform`?

**A:** 
- **`fit_transform(train)`** — LEARNS parameters (median, scale, category mappings) AND transforms the data
- **`transform(test)`** — ONLY applies previously learned parameters. Test data never influences training — prevents **data leakage**.

**Reference:** `src/components/data_transformation.py:83-84`

### Q23: What is data leakage and why must we avoid it?

**A:** Data leakage happens when test data influences training. For example, if the scaler learns mean/scale from both train AND test, the model gets an unrealistic advantage. The test set must remain completely unseen during training — it simulates future real-world data.

**Reference:** `src/components/data_transformation.py:83-84`

### Q24: What does `np.c_` do?

**A:** Concatenates arrays column-wise. After transformation, features are one array and target (math_score) is another. `np.c_[features, target]` stacks them side-by-side into one combined array for the model trainer.

**Reference:** `src/components/data_transformation.py:86-91`

### Q25: Why save `preprocessor.pkl`?

**A:** For inference. When a user submits form data on the website, we need to apply the EXACT same transformations (same categories, same scaling parameters) to their single row. The pickle file locks in all learned parameters.

**Reference:** `src/components/data_transformation.py:93-96`

---

## 6. Model Training

### Q26: How does the model trainer split the transformed array?

**A:** Using numpy slicing:
```python
X_train = train_array[:, :-1]   # all rows, all columns except last (features)
y_train = train_array[:, -1]    # all rows, only last column (target)
```

**Reference:** `src/components/model_trainer.py:33-38`

### Q27: What 7 models are tried?

**A:** Random Forest, Decision Tree, Gradient Boosting, Linear Regression, XGBoost, CatBoost, AdaBoost. This covers simple (Linear) to complex (boosting), bagging (Random Forest) to boosting (XGBoost).

**Reference:** `src/components/model_trainer.py:40-48`

### Q28: What is GridSearchCV and how is it used here?

**A:** `GridSearchCV(model, param_grid, cv=3)` tries every combination of hyperparameters in `param_grid`. `cv=3` means 3-fold cross-validation (data split into 3, train on 2 folds, validate on 1 — repeated 3 times). It picks the combination with the best average score.

**Reference:** `src/utils.py:28-29`

### Q29: How is the best model selected?

**A:** `evaluate_models()` returns a dict of `{model_name: R²_score}`. The code finds the model with maximum R² score. If the best score is below 0.6, it raises an exception (model not good enough).

**Reference:** `src/components/model_trainer.py:84-91`

### Q30: What is R² score?

**A:** Coefficient of determination. Measures how well the model explains variance in the target:
- **1.0** = perfect prediction
- **0.0** = as good as predicting the mean
- **< 0** = worse than predicting the mean

**Reference:** `src/utils.py:37-38`

### Q31: Why a minimum R² threshold of 0.6?

**A:** Quality gate. If even the best model can't reach 0.6, something is fundamentally wrong — bad data, wrong features, or preprocessing issues. Better to fail early than deploy a useless model.

**Reference:** `src/components/model_trainer.py:90-91`

### Q32: What does `verbose=False` in CatBoost do?

**A:** Suppresses training output. Without it, CatBoost prints thousands of lines of progress per iteration. `verbose=False` means: "train silently — don't print anything to console."

**Reference:** `src/components/model_trainer.py:46`

### Q33: What is `model.set_params(**gs.best_params_)`?

**A:** The `**` unpacks the dictionary of best hyperparameters from GridSearchCV. It sets those optimal parameters on the model before final training. For example, `{"n_estimators": 128}` becomes `model.set_params(n_estimators=128)`.

**Reference:** `src/utils.py:31`

### Q34: Why train the model again after GridSearchCV?

**A:** GridSearchCV trains on cross-validation folds internally. After finding the best params, we re-train on the FULL training dataset using those params. This gives the model maximum data to learn from.

**Reference:** `src/utils.py:32`

### Q35: How are hyperparameter grids designed?

**A:** Each model has different tunable parameters:
- Tree-based: `n_estimators`, `criterion`, `max_depth`
- Boosting: `learning_rate`, `subsample`, `iterations`
- Linear Regression: empty grid (no hyperparameters to tune)

GridSearch tries every combination to find optimal values.

**Reference:** `src/components/model_trainer.py:50-76`

---

## 7. Prediction Pipeline

### Q36: What is the purpose of `CustomData` class?

**A:** It acts as a data transfer object. It receives 7 raw form inputs (gender, race, scores, etc.) from the Flask request, stores them, and provides `get_data_as_data_frame()` to convert them into a pandas DataFrame (1 row, 7 columns) that the preprocessor can transform.

**Reference:** `src/pipeline/predict_pipeline.py:8-40`

### Q37: Why convert form data into a DataFrame instead of using raw variables?

**A:** The preprocessor (`preprocessor.pkl`) expects a DataFrame with specific column names matching the training data. A raw dict or list wouldn't have column names, and the ColumnTransformer uses column names to route data to the right pipeline.

**Reference:** `src/pipeline/predict_pipeline.py:29-38`

### Q38: What does `PredictPipeline.predict()` do step by step?

**A:**
1. Load `model.pkl` (trained best model)
2. Load `preprocessor.pkl` (transformation rules)
3. `preprocessor.transform(features)` — apply same transformations as training
4. `model.predict(scaled)` — get math score prediction
5. Return the prediction

**Reference:** `src/pipeline/predict_pipeline.py:47-57`

### Q39: Why load both model.pkl and preprocessor.pkl?

**A:** They serve different purposes:
- **preprocessor.pkl** — converts raw input (text categories, raw scores) into the numerical format the model understands
- **model.pkl** — takes the numerical data and predicts the math score

Both are needed for inference. One transforms, one predicts.

**Reference:** `src/pipeline/predict_pipeline.py:49-56`

### Q40: Where is `load_object` defined and how does it work?

**A:** In `src/utils.py:48-53`. It opens a file in read-binary mode (`"rb"`) and uses `pickle.load()` to deserialize the Python object back into memory. Returns the original object (model or preprocessor).

**Reference:** `src/utils.py:48-53`

---

## 8. Flask Web App

### Q41: How does the Flask app handle GET vs POST?

**A:** 
- **GET** (first visit to `/predictdata`) → shows the empty form (`home.html`)
- **POST** (user clicks submit) → collects form data, runs prediction, shows result on the same page

**Reference:** `app.py:16-33`

### Q42: How are form fields extracted in Flask?

**A:** `request.form.get('field_name')` — Flask stores POST data in `request.form` (a dictionary-like object). The `name` attribute in HTML `<input>` and `<select>` tags must match the string passed to `.get()`.

**Reference:** `app.py:21-28`

### Q43: How does Flask pass the prediction result to HTML?

**A:** `render_template('home.html', results=results[0])` — the second argument passes a variable to the template. In HTML, `{{results}}` renders this value.

**Reference:** `app.py:33`

### Q44: What is the `action` attribute in the HTML form?

**A:** `action="{{ url_for('predict_datapoint') }}"` — tells the browser which URL to send the POST request to. `url_for()` generates the URL from the Python function name, so changes in routing are reflected automatically.

**Reference:** `templates/home.html`

### Q45: Why create both `app` and `application` variables?

**A:** `application` is the name that AWS Elastic Beanstalk's WSGI server looks for by convention. `app` is a shorter alias used in the code. Both point to the same Flask object.

**Reference:** `app.py:7-8`

### Q46: What does `if __name__ == "__main__"` do?

**A:** Ensures `app.run()` only executes when the script is run directly (not when imported). When deployed via WSGI server (gunicorn/Elastic Beanstalk), the server manages the Flask app — `app.run()` should NOT be called.

**Reference:** `app.py:36-37`

### Q47: What does `app.run(host="0.0.0.0")` mean?

**A:** Makes the server accessible from any network interface, not just localhost. Required for Docker and cloud deployment. Without it, the app is only accessible from the same machine.

**Reference:** `app.py:37`

---

## 9. Docker & Deployment

### Q48: Why is `application.py` needed?

**A:** AWS Elastic Beanstalk's WSGIPath setting (`application:application`) expects a file named `application.py` containing the `application` callable. This wrapper file imports the Flask app from `app.py` so EB can find it.

**Reference:** `application.py:1-4`

### Q49: Why use gunicorn instead of app.run() in production?

**A:** Flask's built-in server is single-threaded and development-only. Gunicorn is a production WSGI server that handles multiple requests concurrently via worker processes, has proper load handling, and is more secure.

**Reference:** `Dockerfile:10`

### Q50: What does the Docker WORKDIR command do?

**A:** Sets the working directory inside the container. All subsequent commands (COPY, RUN, CMD) are relative to this path. Think of it as `cd` inside the container.

**Reference:** `Dockerfile:3`

### Q51: Why COPY requirements.txt before the rest of the code?

**A:** Docker layer caching. Docker caches each instruction as a layer. Requirements change less often than code. By copying and installing requirements first, Docker reuses the cached layer when only code changes — making builds significantly faster.

**Reference:** `Dockerfile:5-6`

---

## 10. ML Theory

### Q52: What is the difference between Bagging and Boosting?

**A:**
- **Bagging** (Random Forest): Multiple models trained independently in parallel, predictions averaged. Reduces **variance** (overfitting).
- **Boosting** (Gradient Boosting, XGBoost, CatBoost): Models trained sequentially, each one correcting the errors of the previous. Reduces **bias** (underfitting).

### Q53: Why try multiple models instead of just one?

**A:** No single algorithm works best for all problems. Different models have different biases. Trying 7 models with hyperparameter tuning finds the best fit for this specific dataset.

### Q54: What is overfitting and how does this project prevent it?

**A:** Overfitting = model memorizes training data but fails on new data. Prevention methods:
- **Train/test split** — evaluate on unseen data
- **Cross-validation** (cv=3) — more robust evaluation
- **Hyperparameter tuning** — finds balanced complexity
- **R² threshold** (0.6) — rejects poor models

### Q55: What is the difference between training score and test score?

**A:** 
- **Training score** — how well model fits the training data (may be unrealistically high)
- **Test score** — how well model generalizes to unseen data (the real metric)
- Large gap = overfitting

### Q56: Why use both `SimpleImputer` AND `StandardScaler` in the pipeline?

**A:** They solve different problems:
- **Imputer** handles missing values (data completeness)
- **Scaler** normalizes ranges (feature scale)
A model needs both complete data AND comparable scales.

### Q57: What is `np.c_` and how is it different from `np.concatenate`?

**A:** `np.c_` is a shorthand for concatenating arrays column-wise (along axis=1). `np.c_[a, b]` is equivalent to `np.concatenate([a, b], axis=1)`. It's more readable for simple column stacking.

**Reference:** `src/components/data_transformation.py:86-91`

### Q58: What would happen if we fit the preprocessor on test data?

**A:** **Data leakage.** The test set would influence the scaling parameters and encoding categories. The model would get an unrealistic performance estimate because it effectively "saw" the test data during preprocessing.

### Q59: Why is it a regression problem and not classification?

**A:** The target variable `math_score` is a **continuous numerical value** (0-100). Regression predicts quantities. Classification predicts discrete categories (pass/fail, A/B/C/D grades).

### Q60: How would you improve this project?

**A:** Possible improvements:
- Add feature engineering (interaction features, polynomial features)
- Add more cross-validation folds (cv=5 or cv=10)
- Include deep learning model (neural network)
- Add model interpretability (SHAP, LIME)
- Add A/B testing for deployed models
- Add monitoring/drift detection
- Add more data sources

---

## Quick Reference — Key Code Locations

| Concept | File | Line(s) |
|---------|------|---------|
| Custom exception | `src/exception.py` | 5-21 |
| Logger setup | `src/logger.py` | 1-16 |
| Setup/package | `setup.py` | 16-22 |
| Data Ingestion config | `src/components/data_ingestion.py` | 9-13 |
| Train/test split | `src/components/data_ingestion.py` | 30 |
| Numerical pipeline | `src/components/data_transformation.py` | 41-44 |
| Categorical pipeline | `src/components/data_transformation.py` | 46-50 |
| ColumnTransformer | `src/components/data_transformation.py` | 52-55 |
| fit_transform vs transform | `src/components/data_transformation.py` | 83-84 |
| Save preprocessor | `src/components/data_transformation.py` | 93-96 |
| Array slicing for X/y | `src/components/model_trainer.py` | 33-38 |
| Model dictionary | `src/components/model_trainer.py` | 40-48 |
| Hyperparameter grids | `src/components/model_trainer.py` | 50-76 |
| GridSearchCV | `src/utils.py` | 28-29 |
| Best model selection | `src/components/model_trainer.py` | 84-88 |
| R² threshold check | `src/components/model_trainer.py` | 90-91 |
| CustomData class | `src/pipeline/predict_pipeline.py` | 8-40 |
| PredictPipeline | `src/pipeline/predict_pipeline.py` | 43-59 |
| Flask routes | `app.py` | 11-13, 16-33 |
| Form data extraction | `app.py` | 21-28 |
| Save object utility | `src/utils.py` | 10-17 |
| Load object utility | `src/utils.py` | 48-53 |
| Evaluate models | `src/utils.py` | 20-45 |
| Dockerfile | `Dockerfile` | 1-10 |
| EB config | `.ebextensions/python.config` | 1-3 |
