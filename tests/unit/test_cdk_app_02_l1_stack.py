import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_app_02_l1.cdk_app_02_l1_stack import CdkApp02L1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_app_02_l1/cdk_app_02_l1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkApp02L1Stack(app, "cdk-app-02-l1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
