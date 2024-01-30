import time

from prefect import flow


@flow(log_prints=True)
def sleepy(seconds: int = 60):
    print(f"sleeing for {seconds}")
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
