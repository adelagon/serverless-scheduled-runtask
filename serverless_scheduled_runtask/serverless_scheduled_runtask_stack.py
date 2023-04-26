import copy
from aws_cdk import (
    # Duration,
    Stack,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as _lambda
)
from constructs import Construct

class ServerlessScheduledRuntaskStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # roles
        # scheduler_role = iam.Role(
        #     self, "SchedulerRole",
        #     assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com")
        # )

        # scheduler_events_policy = iam.PolicyStatement(
        #     actions=["events:PutEvents"],
        #     resources=[event_bus.event_bus_arn],
        #     effect=iam.Effect.ALLOW
        # )

        # scheduler_role.add_to_policy(scheduler_events_policy)


        for sched in config['schedules']:
            # Configure lambda-type tasks
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
                    #event_pattern=events.EventPattern(
                    #    source=["sms.events"]
                    #),
                    schedule=events.Schedule.expression(sched['task']['cron']),
                    targets=[
                        targets.LambdaFunction(lambda_func)
                    ]
                )
        

        
        