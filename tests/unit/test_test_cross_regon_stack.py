import aws_cdk as core
import aws_cdk.assertions as assertions

from test_cross_regon.test_cross_regon_stack import TestCrossRegonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in test_cross_regon/test_cross_regon_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TestCrossRegonStack(app, "test-cross-regon")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
