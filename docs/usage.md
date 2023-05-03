# Usage

## Activity execution

URL is `/v1/activity/execute`

CURL example:

```bash
curl -X 'POST' \
  'http://localhost:8000/v1/activity/execute' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "activity_name": "your_remote_activity",
  "activity_task_queue": "your_queue",
  "args": "some args: string, object or null",
  "start_to_close_timeout": 10,
  "parent_workflow_id": "MyId",
  "schedule_to_start_timeout": 0,
  "heartbeat_timeout": 0,
  "schedule_to_close_timeout": 0,
  "retry_policy": {
    "initial_interval": 1,
    "backoff_coefficient": 2,
    "maximum_interval": 0,
    "maximum_attempts": 0
  },
  "parent_workflow_execution_timeout": 10,
  "parent_workflow_run_timeout": 0,
  "parent_workflow_task_timeout": 0
}'
```

### activity_name

**REQUIRED** name of remote activity

### activity_task_queue

**REQUIRED** name of queue with remote activity

### args

Default to *null*

#### Any

You can use any available argument format:

`"args": "string"`

`"args": 100500`

`"args": true`

`"args": "[1,2,3]"`

`"args": "{'foo':'bar'}"`

#### null

Using null by default obliges app use overloaded **execute_activity** method with NO args. So, now you can`t translate *null* (*None*) as an arg to remote activity. Will be fixed soon.

### Retry policy

Default to *null*, but you can provide it as an object in format like:
```json
"retry_policy": {
    "initial_interval": 1, # REQUIRED
    "backoff_coefficient": 2, # REQUIRED
    "maximum_interval": null,
    "maximum_attempts": 0
}
```

### Other arguments

All other arguments in example above are similar to Temporal API

---

## Workflow execution

URL is `/v1/workflow/execute`

CURL example:

```bash
curl -X 'POST' \
  'http://localhost:8000/v1/workflow/execute' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "workflow_name": "string",
  "workflow_task_queue": "string",
  "args": "string",
  "workflow_id": "string",
  "execution_timeout": 1
}'
```

### workflow_name

**REQUIRED** name of remote workflow

### workflow_task_queue

**REQUIRED** name of queue with remote workflow

### args

Args mechanic is similar to [activity](#args) one

### workflow_id

Default to *null*

If workflow_id is not provided or *null*, **UUID4** will be used

### execution_timeout

Default to *10* (seconds)
