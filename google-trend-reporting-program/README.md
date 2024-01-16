# Google Trend Reporting Program
This program reports a list of trending search keywords provided by [Google Trend](https://trends.google.com/trends/trendingsearches/daily) as a GitHub issue.

## Environment
- Python 3.10.13

## Run

### 1. Set Environment Variables
```bash
cp .env.template .env
# And fill in the values of the variables
```

### 2. Install Python Library
```bash
pip install -r requirements.txt
```

### 3. Run
```bash
python google-trend-reporting.py
```