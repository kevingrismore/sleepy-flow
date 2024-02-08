from prefect import flow, get_client
from prefect.runtime import deployment
from prefect.states import Cancelled


@flow
def skip_example():
    if deployment_already_runing():
        return Cancelled()

    else:
        pass  # do other stuff


def deployment_already_runing() -> bool:
    deployment_id = deployment.get_id()
    client = get_client()
    running_flows = client.read_flow_runs(
        deployment_filter={
            "id": deployment_id,
            "state": ["RUNNING", "PENDING", "PAUSED"],
        }
    )
    if len(running_flows) > 1:
        print("Another flow is running, skipping")
        return True

    else:
        print("No other flow is running, continuing")
        return False


if __name__ == "__main__":
    skip_example.from_source(
        source="https://github.com/kevingrismore/sleepy-flow.git",
        entrypoint="cancel.py:skip_example",
    ).deploy(
        name="aci-skip-example",
        image="prefecthq/prefect:2-latest",
        work_pool_name="aci-test",
        build=False,
    )
