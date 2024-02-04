import time

from prefect import flow, task


@flow(log_prints=True)
def sleepy(seconds: int = 60, times: int = 1):
    for i in range(times):
        sleepy_task(seconds=seconds)


@task
def sleepy_task(seconds: int = 60):
    print(f"sleeping for {seconds}")
    time.sleep(seconds)


if __name__ == "__main__":
    sleepy.from_source(
        source="https://github.com/kevingrismore/sleepy-flow.git",
        entrypoint="sleepy.py:sleepy",
    ).deploy(
        name="azure-sleepy",
        image="prefecthq/prefect:2-latest",
        work_pool_name="azure-kubernetes",
        build=False,
    )

    # sleepy.from_source(
    #     source="https://github.com/kevingrismore/sleepy-flow.git",
    #     entrypoint="sleepy.py:sleepy",
    # ).deploy(
    #     name="azure-sleepy-2",
    #     image="prefecthq/prefect:2-latest",
    #     work_pool_name="azure-kubernetes-default",
    #     build=False,
    # )
