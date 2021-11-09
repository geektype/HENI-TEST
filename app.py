from aws_cdk import core as cdk
from testAppStacks.base_network_stack import BaseNetworkStack
from testAppStacks.webserver_asg_stack import WebserverASGStack
from testAppStacks.alb_stack import ALBStack

app = cdk.App()

network_stack = BaseNetworkStack(app, "BaseNetworkStack")
webserver_asg_stack = WebserverASGStack(app, "WebserverASGStack", network_stack.vpc)
alb_stack = ALBStack(
    app, "ALBStack", network_stack.vpc, asg=webserver_asg_stack.webserver_asg
)

app.synth()
