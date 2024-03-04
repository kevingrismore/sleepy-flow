from prefect import flow, task
from prefect_dask import DaskTaskRunner


@task
def do_something(number: int):
    try:
        from util import do_something_useful

        print("imported util during local run")
    except ModuleNotFoundError:
        from dask_ecs.util import do_something_useful

        print("imported dask_ecs.util during deployment run")
    print(number)
    do_something_useful()


@flow(log_prints=True, task_runner=DaskTaskRunner)
def ecs_flow():
    do_something.submit(1)


if __name__ == "__main__":
    ecs_flow.serve("dask-ecs-flow")
    # ecs_flow()
