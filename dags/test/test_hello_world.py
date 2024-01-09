import pendulum

from airflow.decorators import dag, task

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["test"],
)
def test_hello_world():

    @task()
    def hello_world():
        print("Hello, World!")

    @task()
    def hello_airflow():
        print("Hello, Airflow!")
    
    hello_world() >> hello_airflow()

test_hello_world()
