# Airflow Projects
This is Airflow Projects.

## Environment
- Python 3.10.13 (Use pyenv and virtualenv)
- Airflow 2.8.0

## Run

### 1-1. Install Airflow
```bash
./install_airflow.sh
```

### 1-2. Install Python library
```bash
pip install -r requirements.txt
```

### 2. Set Airflow Home
```bash
export AIRFLOW_HOME={THIS_PROJECT_PATH}/airflow
```

### 3. Run Airflow Standalone
```bash
airflow standalone
```

<hr>

#### Reference
- [Airflow Docs - Quick Start](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
