from aws_cdk import core as cdk
from testAppStacks.base_network_stack import BaseNetworkStack

app = cdk.App()

network_stack = BaseNetworkStack(app, "BaseNetworkStack")

app.synth()
