# Chapter 2: Project Setup, Exception Handling & Logging

## setup.py — Making it a Package

```python
from setuptools import find_packages, setup

setup(
    name='mlproject',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
```

**Purpose:** Makes the project installable as a Python package. When you run `pip install -e .`, it installs everything in `src/` so you can do `from src.components.data_ingestion import DataIngestion` from anywhere.

**`find_packages()`** — Finds all folders that have `__init__.py` file.

### requirements.txt
```
pandas
numpy
scikit-learn
catboost
xgboost
flask
-e .
```

The `-e .` triggers the editable install from `setup.py`.

---

## exception.py — Custom Error Handler

```python
import sys
from src.logger import logging

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error in [{0}] line [{1}] message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message
```

**How it works:**
- `sys.exc_info()` captures the **exact file** and **line number** where the error occurred
- Instead of a generic Python error, you get: `"Error in data_ingestion.py line 42 message: file not found"`
- Used everywhere: `raise CustomException(e, sys)`

---

## logger.py — File Logging

```python
import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
```

**Key points:**
- Creates a new log file **every time** you run the code (timestamped)
- Stores in `logs/` folder
- Format: `[timestamp] line_number module_name - LEVEL - message`
- Use: `logging.info("Your message")` throughout the code

## The Pattern: Config + Main Class
Every component follows this pattern:
1. **Config class** (`@dataclass`) — stores file paths only
2. **Main class** — does the actual work, uses config for paths

This separates **what to do** (config) from **how to do it** (main class).
