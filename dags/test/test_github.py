import pendulum

from airflow.decorators import dag, task
from github import Github, Auth

@dag(
    schedule="0 10 * * *",
    start_date=pendulum.datetime(2024, 1, 1),
    catchup=False,
    tags=["test", "github"],
)
def test_github():
    auth = Auth.Token("{ACCESS_TOKEN}")
    g = Github(auth=auth)

    @task()
    def print_repo_list():
        for repo in g.get_user().get_repos():
            print(repo.name)

    print_repo_list()

test_github()
