# Google Trend Reporting Program
This program reports a list of trending search keywords provided by [Google Trend](https://trends.google.com/trends/trendingsearches/daily) as a GitHub issue.

## Environment
- Python 3.10.13

## Run

### 1. Set Environment Variables
```bash
cp ./template/.env.template .env
# And fill in the values of the variables
```

### 2. Install Python Library
```bash
pip install -r requirements.txt
```

### 3-1. Run in Local
```bash
python main.py
```

### 3-2. Run in Server
```bash
# Revise .env
# PHASE="real" 

# 1. Directly enter command
nohup python -u main.py > google-trend-reporting-program.log 2>&1 < /dev/null &

# 2. Run script
./gtrp.sh
```