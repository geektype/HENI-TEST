from aws_cdk import (
    core as cdk,
    aws_ec2 as ec2,
)


class BaseNetworkStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        """
        Create the Base network consisting of a single VPC. Both private and
        public subnets across 2 availaibility zones.
        """
        super().__init__(scope, construct_id, **kwargs)
        self.subnets = []
        self.subnets.append(
            ec2.SubnetConfiguration(
                name="server",
                subnet_type=ec2.SubnetType.PRIVATE,
            )
        )

        self.subnets.append(
            ec2.SubnetConfiguration(
                name="public",
                subnet_type=ec2.SubnetType.PUBLIC,
            )
        )

        self.vpc = ec2.Vpc(
            self,
            id="main_vpc",
            cidr="10.0.0.0/16",
            max_azs=2,
            subnet_configuration=self.subnets,
        )
