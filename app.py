from aws_cdk import core as cdk
from testAppStacks.base_network_stack import BaseNetworkStack
from testAppStacks.webserver_asg_stack import WebserverASGStack

app = cdk.App()

network_stack = BaseNetworkStack(app, "BaseNetworkStack")
webserver_asg_stack = WebserverASGStack(app, "WebserverASGStack", network_stack.vpc)

app.synth()
