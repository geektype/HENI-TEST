from aws_cdk import (
    core as cdk,
    aws_elasticloadbalancingv2 as elb,
    aws_ec2 as ec2,
)


class ALBStack(cdk.Stack):
    def __init__(
        self, scope: cdk.Construct, construct_id: str, vpc, asg, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        alb = elb.ApplicationLoadBalancer(
            self,
            id="app-alb",
            vpc=vpc,
            internet_facing=True,
        )

        webserver_TG = elb.ApplicationTargetGroup(
            self,
            id="webserverTG",
            target_group_name="webserverTG",
            vpc=vpc,
            target_type=elb.TargetType.INSTANCE,
            protocol=elb.ApplicationProtocol.HTTP,
            protocol_version=elb.ApplicationProtocolVersion.HTTP1,
        )

        asg.attach_to_application_target_group(webserver_TG)

        webserver_HTTP_listner = elb.ApplicationListener(
            self,
            id="webserver_HTTP_listner",
            load_balancer=alb,
            default_target_groups=[webserver_TG],
            open=True,
            port=80,
            protocol=elb.Protocol.HTTP,
        )

        cdk.CfnOutput(self, "ALB URL", value=alb.load_balancer_dns_name)
