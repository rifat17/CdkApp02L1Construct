from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnTag,
)
from constructs import Construct
from cdk_app_02_l1.models import SubnetType
from cdk_app_02_l1.constants import STACK_NAME

class CdkApp02L1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc_logical_id = f"{STACK_NAME}VPC"
        vpc_name_tag = CfnTag(key="Name", value=vpc_logical_id)
        my_vpc = ec2.CfnVPC(
            self,
            vpc_logical_id,
            cidr_block="10.0.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags=[vpc_name_tag],
        )

        internet_gateway = ec2.CfnInternetGateway(self, "InternetGateway")

        ec2.CfnVPCGatewayAttachment(
            self,
            "IgAttachment",
            vpc_id=my_vpc.attr_vpc_id,
            internet_gateway_id=internet_gateway.attr_internet_gateway_id,
        )

        subnets = [
            {"cidr_block": "10.0.0.0/24", "access": SubnetType.PUBLIC},
            {"cidr_block": "10.0.1.0/24", "access": SubnetType.PUBLIC},
            {"cidr_block": "10.0.2.0/24", "access": SubnetType.PRIVATE},
            {"cidr_block": "10.0.3.0/24", "access": SubnetType.PRIVATE},
        ]

        for idx, subnet_config in enumerate(subnets):
            subnet_logical_id = f"{subnet_config.get("access")}Subnet{idx+1}"
            is_public_subnet = subnet_config.get("access") == SubnetType.PUBLIC
            cidr_block = subnet_config.get("cidr_block")

            subnet = ec2.CfnSubnet(
                self,
                subnet_logical_id,
                vpc_id=my_vpc.attr_vpc_id,
                cidr_block=cidr_block,
                map_public_ip_on_launch=is_public_subnet,
                availability_zone=Stack.availability_zones.fget(self)[idx%2]
            )

            route_table = ec2.CfnRouteTable(
                self,
                f"{subnet_logical_id}RouteTable",
                vpc_id=my_vpc.attr_vpc_id
                )
            ec2.CfnSubnetRouteTableAssociation(
                self,
                f"{subnet_logical_id}RouteTableAssoc",
                subnet_id=subnet.attr_subnet_id,
                route_table_id=route_table.attr_route_table_id,
            )

            if is_public_subnet:
                ec2.CfnRoute(
                    self,
                    f"{subnet_logical_id}InternetRoute",
                    route_table_id=route_table.attr_route_table_id,
                    destination_cidr_block="0.0.0.0/0",
                    gateway_id=internet_gateway.attr_internet_gateway_id
                )




