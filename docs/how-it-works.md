# How it works?

## Principal

App is a combination of FastAPI-based REST server and official Temporal SDK in async runtime. Executor is stateless and create every new connection to Temporal server with every REST invocation.

## Activity

### Execution

To execute any remote activity, the app uses **INTERNAL_WORKFLOW**, which consists of **execute_activity** method.

This internal workflow executes in [TEMPORAL_INTERNAL_TASK_QUEUE](./index.md#temporal_internal_task_queue) and can be renamed (see [TEMPORAL_INTERNAL_FLOW_NAME](./index.md#temporal_internal_flow_name))

All attributes, started with **parent_workflow_** are the attributes for this workflow, for ex:

```
parent_workflow_id
parent_workflow_execution_timeout
parent_workflow_run_timeout
parent_workflow_task_timeout
```
They are similar to Temporal SDK attributes for workflows, see the official API documentaion

Other attributes are using for **execute_activity** themselves, for ex:

```
activity_name
activity_task_queue
args
start_to_close_timeout
schedule_to_start_timeout
heartbeat_timeout
schedule_to_close_timeout
retry_policy
```

## Workflow

### Execution

Remote workflow execution is much simple, then the activity one. It uses **client.execute_workflow** method of official SDK.

There are some args for this method:

```
workflow_name
workflow_task_queue
args
workflow_id
execution_timeout
```

### Execution as a child workflow

Feature will be added soon...