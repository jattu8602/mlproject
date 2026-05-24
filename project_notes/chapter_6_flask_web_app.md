# Chapter 6: Flask Web App & Prediction Pipeline

## What is Flask?
A tiny Python web server that:
1. Shows HTML pages when you visit a URL
2. Receives form data when you submit
3. Runs Python code to process that data
4. Shows the result back on the page

## Basic Flask Pattern
```python
from flask import Flask, request, render_template

app = Flask(__name__)          # Create web app

@app.route('/url')             # When user visits this URL
def function_name():
    return render_template('page.html')   # Show this HTML
```

## Our App's Routes
```python
@app.route('/')                # http://localhost:5000/
    → index.html ("Welcome")

@app.route('/predictdata', methods=['GET', 'POST'])
    # GET  → show home.html (empty form)
    # POST → collect data → predict → show result
```

## GET vs POST
| Method | When | What happens |
|--------|------|-------------|
| GET | First visit to page | Show the empty form |
| POST | User clicks "Submit" | Collect form data, predict, show result |

## CustomData Class
Takes 7 form inputs and converts to a 1-row DataFrame:
```python
data = CustomData(
    gender=request.form.get('gender'),
    race_ethnicity=request.form.get('ethnicity'),
    ...
)
pred_df = data.get_data_as_data_frame()
```

## PredictPipeline Class
```python
predict_pipeline = PredictPipeline()
results = predict_pipeline.predict(pred_df)
# result: predicted math score (e.g. 64.6)
```

Inside `predict()`:
1. Load `model.pkl` — the trained brain
2. Load `preprocessor.pkl` — the transformation rules
3. `preprocessor.transform(features)` — convert raw input to numbers
4. `model.predict(scaled)` — predict math score
5. Return the prediction

## The Complete End-to-End Flow
```
User opens http://localhost:5000           → Welcome page
         ↓
User visits /predictdata                    → Sees a form with 7 fields
         ↓
User fills: gender, race, lunch, scores... → Clicks "Predict"
         ↓
request.form collects all 7 fields          → CustomData stores them
         ↓
get_data_as_data_frame()                    → pandas DataFrame (1 row)
         ↓
PredictPipeline.predict(DataFrame)
    ├── load preprocessor.pkl → transform raw data
    └── load model.pkl → predict math score
         ↓
Result (e.g. 64.6) shown on page           ✅ DONE!
```
