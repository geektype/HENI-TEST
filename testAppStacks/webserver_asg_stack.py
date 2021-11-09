from aws_cdk import (
    core as cdk,
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
)


class WebserverASGStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.user_data = ec2.UserData.custom(
            content='#!/bin/bash\nsudo su\nyum update -y\nyum install -y httpd.x86_64\nsystemctl start httpd.service\nsystemctl enable httpd.service\necho "Hello World from $(hostname -f)" > /var/www/html/index.html'
        )
        self.machine_image = ec2.MachineImage.generic_linux(
            {"us-east-1": "ami-01cc34ab2709337aa"},
            user_data=self.user_data,
        )

        self.security_group = ec2.SecurityGroup(
            self,
            id="webserver-sg",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="webserver-sg",
        )

        self.security_group.add_ingress_rule(
            ec2.Peer.ipv4("10.0.0.0/16"), ec2.Port.all_traffic()
        )
        self.webserver_asg = autoscaling.AutoScalingGroup(
            self,
            id="webserver_asg",
            auto_scaling_group_name="webserver_asg",
            min_capacity=1,
            desired_capacity=2,
            max_capacity=5,
            vpc=vpc,
            instance_type=ec2.InstanceType(instance_type_identifier="t3.micro"),
            machine_image=self.machine_image,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
            security_group=self.security_group,
        )
