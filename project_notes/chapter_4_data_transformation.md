# Chapter 4: Data Transformation

## The Problem
ML algorithms only understand **numbers** — not words. Our data has both:

| Column | Type | Problem |
|--------|------|---------|
| writing_score | Numerical (0-100) | Already a number ✅ |
| reading_score | Numerical (0-100) | Already a number ✅ |
| gender | Categorical | "male"/"female" — needs encoding |
| race_ethnicity | Categorical | "group A"/"group B" — needs encoding |
| parental_level_of_education | Categorical | Text — needs encoding |
| lunch | Categorical | "standard"/"free" — needs encoding |
| test_preparation_course | Categorical | "none"/"completed" — needs encoding |

## The 3 Transformers

### 1. SimpleImputer — Fill Missing Values
```python
SimpleImputer(strategy="median")        # For numbers: fill with median
SimpleImputer(strategy="most_frequent") # For categories: fill with most common
```
If a writing score is missing, use the median of all writing scores.

### 2. OneHotEncoder — Words to Numbers
Converts each category into its own column of 0s and 1s:

```
gender          →    gender_female  gender_male
male            →    0              1
female          →    1              0
```

### 3. StandardScaler — Same Scale
Makes all numbers have **mean=0** and **standard deviation=1**.
Formula: `(value - mean) / standard_deviation`

**Why?** A model shouldn't treat "score=75" as more important than "score=0.5" just because the number is bigger.

## Pipeline — Assembly Line for Data
```python
num_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
```
Step 1 output → Step 2 input. No manual work needed.

## ColumnTransformer — Different Treatment for Different Columns
```python
preprocessor = ColumnTransformer([
    ("num_pipeline", num_pipeline, ["writing_score", "reading_score"]),
    ("cat_pipeline", cat_pipeline, ["gender", "race_ethnicity", ...])
])
```
Numerical columns get imputer + scaler. Categorical columns get imputer + one-hot + scaler.

## fit_transform vs transform — CRITICAL!
```python
preprocessor.fit_transform(train_df)  # LEARNS: median, scale, categories
preprocessor.transform(test_df)       # APPLIES: uses train's learnings
```
- **Train:** Learn the patterns AND transform
- **Test:** Only transform (never learn from test — that would be cheating/leakage)

## Saving the Preprocessor
```python
save_object(file_path='artifacts/preprocessor.pkl', obj=preprocessor)
```
Saves the preprocessor so when a user submits a form on the website, we transform their one row EXACTLY the same way we transformed training data. The encoding mappings are locked in.

## np.c_ — Combining Features + Target
```python
train_arr = np.c_[transformed_features, math_scores]
```
Stacks features and target side-by-side as one big array for the model trainer.

## The "Why" Behind Each Design Decision

| Decision | Why |
|----------|-----|
| Separate Config class | Easy to change paths without touching logic |
| Pipeline | Ensures consistent step order, prevents mistakes |
| fit_transform on train only | Prevents data leakage (test data influencing training) |
| Save preprocessor.pkl | Reuse exact same transformation for web predictions |
