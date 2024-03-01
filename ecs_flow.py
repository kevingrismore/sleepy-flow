from prefect import flow
from prefect_dask import DaskTaskRunner

from util import do_something_useful


@flow(log_prints=True, task_runner=DaskTaskRunner)
def ecs_flow():
    do_something_useful()


if __name__ == "__main__":
    ecs_flow.from_source(
        source="https://github.com/kevingrismore/sleepy-flow.git",
        entrypoint="ecs_flow.py:ecs_flow",
    ).deploy(
        name="ecs-flow",
        image="kevingrismoreprefect/prefect-with-dask:1",
    )
