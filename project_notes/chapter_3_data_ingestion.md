# Chapter 3: Data Ingestion

## What is Ingestion?
Like receiving raw ingredients in a restaurant:
1. Get a bag of potatoes (raw CSV)
2. Wash and sort them (save raw copy)
3. Split: 80% for cooking (train), 20% for taste-testing later (test)

## Code Walkthrough

### Imports
```python
import os                              # File/folder operations
import sys                             # System access (for exceptions)
from src.exception import CustomException  # Custom error handler
from src.logger import logging         # File logging
import pandas as pd                    # CSV reading, DataFrames
from sklearn.model_selection import train_test_split  # 80/20 split
from dataclasses import dataclass      # Auto __init__ for configs
```

### Config Class
```python
@dataclass
class DataIngestionConfig:
    train_data_path = 'artifacts/train.csv'
    test_data_path = 'artifacts/test.csv'
    raw_data_path = 'artifacts/data.csv'
```
- `@dataclass` auto-generates `__init__()`
- `os.path.join()` uses correct slash for any OS (Mac/Linux: `/`, Windows: `\`)

### Main Class
```python
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
```

### The Core Method
```python
def initiate_data_ingestion(self):
    # 1. Read the CSV
    df = pd.read_csv('notebook/data/stud.csv')

    # 2. Create artifacts directory
    os.makedirs('artifacts', exist_ok=True)
    # exist_ok=True: no error if folder already exists

    # 3. Save raw backup
    df.to_csv('artifacts/data.csv', index=False, header=True)

    # 4. Split 80/20
    train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
    # random_state=42 ensures same split every time (reproducibility)

    # 5. Save splits
    train_set.to_csv('artifacts/train.csv', index=False, header=True)
    test_set.to_csv('artifacts/test.csv', index=False, header=True)

    # 6. Return paths for next stage
    return ('artifacts/train.csv', 'artifacts/test.csv')
```

### Why `random_state=42`?
Without it, every run would give a different random split. The model would learn from different data each time — impossible to debug. `42` is just a common convention (Answer to the Ultimate Question of Life, the Universe, and Everything).

### Why `exist_ok=True`?
- `os.makedirs("path")` → errors if path exists
- `os.makedirs("path", exist_ok=True)` → silently skips if exists

## Full Data Flow So Far
```
notebook/data/stud.csv
    ↓
data_ingestion.py
    ↓
artifacts/
  ├── data.csv     (raw backup)
  ├── train.csv    (80% for training)
  └── test.csv     (20% for testing)
    ↓ (returns paths)
data_transformation.py
```
