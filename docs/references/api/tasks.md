# Tasks

Declarative units of work: an agent, a description, and per-call overrides
packaged into named, documented work units executed by the Runner.

## Core

- `augments.adk.tasks.Task`
- `augments.adk.tasks.TaskDependency`
- `augments.adk.tasks.TaskInputFilter`

## Pipelines

- `augments.adk.tasks.TaskPipeline`
- `augments.adk.tasks.TaskPipelineResult`
- `augments.adk.tasks.TaskPipelineState`

## Task groups

- `augments.adk.tasks.TaskGroup`
- `augments.adk.tasks.TaskGroupResult`
- `augments.adk.tasks.ErrorPolicy`

## Input and output

- `augments.adk.tasks.TaskInputData`
- `augments.adk.tasks.TaskOutput`

## Exceptions

- `augments.adk.tasks.TaskPipelineDefinitionError`

Tasks run via `Runner.arun_task`, `Runner.arun_task_pipeline`, and
`Runner.arun_task_group`. Usage lives in the
[Tasks guide](../../tasks/tasks.md).
