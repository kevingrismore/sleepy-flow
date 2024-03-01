from prefect import flow, task
from prefect_dask import DaskTaskRunner
from prefect.deployments import DeploymentImage

from dask_ecs.util import do_something_useful


@task
def do_something(number: int):
    print(number)
    do_something_useful()


@flow(log_prints=True, task_runner=DaskTaskRunner)
def ecs_flow():
    do_something.map([1])


if __name__ == "__main__":
    ecs_flow()
    # ecs_flow.from_source(
    #     source="https://github.com/kevingrismore/sleepy-flow.git",
    #     entrypoint="dask_ecs/ecs_flow.py:ecs_flow",
    # ).deploy(
    #     name="ecs-flow",
    #     work_pool_name="my-ecs-pool",
    #     image=DeploymentImage(
    #         name="kevingrismoreprefect/prefect-with-dask",
    #         tag="2",
    #         platform="linux/amd64",
    #     ),
    # )
