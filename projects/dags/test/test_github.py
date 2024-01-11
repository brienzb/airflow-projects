import os
import pendulum

from airflow.decorators import dag, task

@dag(
    schedule="0 10 * * *",
    start_date=pendulum.datetime(2024, 1, 1),
    catchup=False,
    tags=["test", "github"],
)
def test_github():
    @task()
    def print_repo_list():
        # This task is not working.
        # Need to check!
        from github import Github, Auth
    
        auth = Auth.Token(f"{os.getenv('GITHUB_ACCESS_TOKEN')}")
        g = Github(auth=auth)

        for repo in g.get_user().get_repos():
            print(repo.name)

    print_repo_list()

test_github()
