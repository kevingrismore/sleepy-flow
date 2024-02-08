from prefect import flow, task, get_client
from prefect.runtime import deployment
from prefect.client.schemas.filters import (
    FlowRunFilter,
    DeploymentFilter,
    FlowRunFilterState,
    FlowRunFilterStateType,
)
from prefect.states import Cancelled


@flow
def skip_example():
    if deployment_already_runing():
        return Cancelled()

    else:
        pass  # do other stuff


@task
async def deployment_already_runing() -> bool:
    deployment_id = deployment.get_id()
    print(deployment_id)
    client = get_client()
    running_flows = await client.read_flow_runs(
        deployment_filter=DeploymentFilter(id=deployment_id),
        flow_run_filter=FlowRunFilter(
            state=FlowRunFilterState(
                type=FlowRunFilterStateType(states=["RUNNING", "PENDING", "PAUSED"])
            )
        ),
    )
    # print(running_flows)
    if len(running_flows) > 1:
        print("Another flow is running, skipping")
        return True

    else:
        print("No other flow is running, continuing")
        return False


if __name__ == "__main__":
    skip_example()

    # skip_example.from_source(
    #     source="https://github.com/kevingrismore/sleepy-flow.git",
    #     entrypoint="cancel.py:skip_example",
    # ).deploy(
    #     name="aci-skip-example",
    #     image="prefecthq/prefect:2-latest",
    #     work_pool_name="aci-test",
    #     build=False,
    # )
