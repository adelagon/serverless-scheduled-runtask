import copy
from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_ecs as ecs,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_applicationautoscaling as appscaling,
    aws_ecs_patterns as ecs_patterns
)
from constructs import Construct

class ServerlessScheduledRuntaskStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### ECS Cluster
        cluster = ecs.Cluster(
            self, "ECSCluster",
        )

        ### create schedules & tasks
        for sched in config['schedules']:
            ## Configure lambda type tasks
            if sched['task']['type'] == "lambda":
                task_name = sched['task']['name']
                task_handler = sched['task']['handler']
                task_environ = sched['task']['environment']
                lambda_func = _lambda.Function(
                    self, task_name,
                    runtime=_lambda.Runtime.PYTHON_3_9,
                    code=_lambda.Code.from_asset("lambda"),
                    handler=task_handler,
                    retry_attempts=0
                )
                
                for env in task_environ:
                    key, val = env.popitem()
                    lambda_func.add_environment(key, val)
           
                rule = events.Rule(
                    self, "{}Schedule".format(task_name),

                    schedule=events.Schedule.expression(sched['task']['cron']),
                    targets=[
                        targets.LambdaFunction(lambda_func)
                    ]
                )
        
                sns_policy = iam.PolicyStatement(
                    actions=["sns:*"],
                    resources=["*"],
                    effect=iam.Effect.ALLOW
                )

                lambda_func.add_to_role_policy(sns_policy)

            ## Configure fargate type tasks
            if sched['task']['type'] == "fargate":
                task_name = sched['task']['name']
                task = ecs_patterns.ScheduledFargateTask(
                    self, task_name,
                    cluster=cluster,
                    scheduled_fargate_task_image_options=ecs_patterns.ScheduledFargateTaskImageOptions(
                        image=ecs.ContainerImage.from_registry("amazonlinux/amazonlinux"),
                        memory_limit_mib=512,
                        command=sched['task']['command'],
                        log_driver=ecs.LogDrivers.aws_logs(
                            stream_prefix=task_name
                        )
                    ),
                    schedule=appscaling.Schedule.expression(sched['task']['cron']),
                    platform_version=ecs.FargatePlatformVersion.LATEST
                )