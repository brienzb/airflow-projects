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

### 1-2. Install Python Library
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
cp ./projects/config/.env.template ./projects/config/.env
# And fill in the values of the variables
```

### 3. Export Environment Variables
```bash
export $(cat ./projects/config/.env | xargs)
```

### 4. Run Airflow Standalone
```bash
airflow standalone
```

<hr>

#### Reference
- [Airflow Docs - Quick Start](https://airflow.apache.org/docs/apache-airflow/stable/start.html)
