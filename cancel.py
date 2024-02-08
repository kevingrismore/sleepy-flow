from prefect import flow, task, get_client
from prefect.runtime import deployment
from prefect.client.schemas.filters import (
    FlowRunFilter,
    DeploymentFilter,
    DeploymentFilterId,
    FlowRunFilterState,
    FlowRunFilterStateType,
)
from prefect.client.schemas.objects import StateType
from prefect.states import Cancelled


@flow(log_prints=True)
def skip_example():
    if deployment_already_runing():
        return Cancelled()

    else:
        pass  # do other stuff


@task
async def deployment_already_runing() -> bool:
    deployment_id = deployment.get_id()
    print(deployment_id)
    async with get_client() as client:
        running_flows = await client.read_flow_runs(
            deployment_filter=DeploymentFilter(
                id=DeploymentFilterId(any_=["afb48780-0969-4e77-9561-f201106d7430"])
            ),
            flow_run_filter=FlowRunFilter(
                state=FlowRunFilterState(
                    type=FlowRunFilterStateType(
                        any_=[StateType.RUNNING, StateType.PENDING, StateType.PAUSED]
                    )
                )
            ),
        )
    print(len(running_flows))
    if len(running_flows) > 1:
        print("Another flow is running, skipping")
        return True

    else:
        print("No other flow is running, continuing")
        return False


async def get_flow_runs():
    async with get_client() as client:
        running_flows = await client.read_flow_runs(
            deployment_filter=DeploymentFilter(
                id=DeploymentFilterId(any_=["afb48780-0969-4e77-9561-f201106d7430"])
            ),
            flow_run_filter=FlowRunFilter(
                state=FlowRunFilterState(
                    type=FlowRunFilterStateType(
                        any_=[StateType.RUNNING, StateType.PENDING, StateType.PAUSED]
                    )
                )
            ),
        )
        print(len(running_flows))


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
