import aws_cdk as core
import aws_cdk.assertions as assertions

from serverless_scheduled_runtask.serverless_scheduled_runtask_stack import ServerlessScheduledRuntaskStack

# example tests. To run these tests, uncomment this file along with the example
# resource in serverless_scheduled_runtask/serverless_scheduled_runtask_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ServerlessScheduledRuntaskStack(app, "serverless-scheduled-runtask")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
