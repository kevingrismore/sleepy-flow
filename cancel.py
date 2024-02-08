import time

from prefect import flow, task, get_client
from prefect.context import get_run_context
from prefect.client.schemas.filters import (
    FlowRunFilter,
    DeploymentFilter,
    DeploymentFilterId,
    FlowRunFilterState,
    FlowRunFilterStateType,
    FlowRunFilterExpectedStartTime,
)
from prefect.client.schemas.objects import StateType
from prefect.runtime import deployment, flow_run
from prefect.states import Cancelled


@flow(log_prints=True)
def skip_example():
    if deployment_already_running():
        return Cancelled()

    else:
        time.sleep(30)  # do other stuff


@task
async def deployment_already_running() -> bool:
    scheduled_start_time = flow_run.get_scheduled_start_time()
    deployment_id = deployment.get_id()
    async with get_client() as client:
        # find any running, pending, or paused flows for this deployment that started
        # at or before the current flow run's start time
        running_flows = await client.read_flow_runs(
            deployment_filter=DeploymentFilter(
                id=DeploymentFilterId(any_=[deployment_id])
            ),
            flow_run_filter=FlowRunFilter(
                state=FlowRunFilterState(
                    type=FlowRunFilterStateType(
                        any_=[StateType.RUNNING, StateType.PENDING, StateType.PAUSED]
                    )
                ),
                start_time=FlowRunFilterExpectedStartTime(
                    before_=scheduled_start_time,
                ),
            ),
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
