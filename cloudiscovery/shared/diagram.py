import base64
import zlib
import json
import datetime
import os
import os.path
from pathlib import Path
from typing import List, Dict
from html import escape
from diagrams import Diagram, Cluster, Edge

from jinja2 import Environment, FileSystemLoader

from shared.common import Resource, ResourceEdge, ResourceDigest, message_handler
from shared.diagramsnet import (
    MX_FILE_TEMPLATE,
    DIAGRAM_TEMPLATE,
    CELL_TEMPLATE,
    CONNECTOR_TEMPLATE,
    USER_OBJECT_TEMPLATE,
    build_styles,
)
from shared.error_handler import exception

PATH_DIAGRAM_OUTPUT = "./assets/diagrams/"
DIAGRAM_CLUSTER = "diagram_cluster"
DIAGRAM_ROW_HEIGHT = 100
PUBLIC_SUBNET = "{public subnet}"
PRIVATE_SUBNET = "{private subnet}"
CELL_ID_MAP = {
    PUBLIC_SUBNET: "public_area_id",
    PRIVATE_SUBNET: "private_area_id"
}

class Mapsources:
    # diagrams modules that store classes that represent diagram elements
    diagrams_modules = [
        "analytics",
        "ar",
        "blockchain",
        "business",
        "compute",
        "cost",
        "database",
        "devtools",
        "enablement",
        "enduser",
        "engagement",
        "game",
        "general",
        "integration",
        "iot",
        "management",
        "media",
        "migration",
        "ml",
        "mobile",
        "network",
        "quantum",
        "robotics",
        "satellite",
        "security",
        "storage",
    ]

    # Class to mapping type resource from Terraform to Diagram Nodes
    mapresources = {
        "aws_lambda_function": "Lambda",
        "aws_emr_cluster": "EMRCluster",
        "aws_emr": "EMR",
        "aws_elasticsearch_domain": "ES",
        "aws_msk_cluster": "ManagedStreamingForKafka",
        "aws_sqs_queue_policy": "SQS",
        "aws_instance": "EC2",
        "aws_eks_cluster": "EKS",
        "aws_autoscaling_group": "AutoScaling",
        "aws_ecs_cluster": "ECS",
        "aws_db_instance": "RDS",
        "aws_elasticache_cluster": "ElastiCache",
        "aws_docdb_cluster": "DocumentDB",
        "aws_internet_gateway": "InternetGateway",
        "aws_nat_gateway": "NATGateway",
        "aws_elb_classic": "ELB",
        "aws_elb": "ELB",
        "aws_route_table": "RouteTable",
        "aws_subnet": "PublicSubnet",
        "aws_network_acl": "Nacl",
        "aws_vpc_peering_connection": "VPCPeering",
        "aws_vpc_endpoint_gateway": "Endpoint",
        "aws_iam_policy": "IAMPermissions",
        "aws_iam_user": "User",
        "aws_iam_group": "IAM",
        "aws_iam_role": "IAMRole",
        "aws_iam_instance_profile": "IAM",
        "aws_efs_file_system": "EFS",
        "aws_s3_bucket_policy": "S3",
        "aws_media_connect": "ElementalMediaconnect",
        "aws_media_convert": "ElementalMediaconvert",
        "aws_media_package": "ElementalMediapackage",
        "aws_media_store": "ElementalMediastore",
        "aws_media_tailor": "ElementalMediatailor",
        "aws_media_live": "ElementalMedialive",
        "aws_api_gateway_rest_api": "APIGateway",
        "aws_sagemaker": "Sagemaker",
        "aws_sagemaker_notebook_instance": "SagemakerNotebook",
        "aws_sagemaker_training_job": "SagemakerTrainingJob",
        "aws_sagemaker_model": "SagemakerModel",
        "aws_ssm_document": "SSM",
        "aws_cognito_identity_provider": "Cognito",
        "aws_iot_thing": "InternetOfThings",
        "aws_general": "General",
        "aws_appsync_graphql_api": "Appsync",
        "aws_iot_analytics": "IotAnalytics",
        "aws_securityhub_account": "SecurityHub",
        "aws_trusted_advisor": "TrustedAdvisor",
        "aws_kinesis_firehose": "KinesisDataFirehose",
        "aws_glue": "Glue",
        "aws_quicksight": "Quicksight",
        "aws_cloud9": "Cloud9",
        "aws_organizations_account": "Organizations",
        "aws_config": "Config",
        "aws_auto_scaling": "AutoScaling",
        "aws_backup": "Backup",
        "aws_cloudtrail": "Cloudtrail",
        "aws_cloudwatch": "Cloudwatch",
        "aws_data_pipeline": "DataPipeline",
        "aws_dms": "DMS",
        "aws_elastic_beanstalk_environment": "EB",
        "aws_fms": "FMS",
        "aws_global_accelerator": "GAX",
        "aws_inspector": "Inspector",
        "aws_cloudfront_distribution": "CloudFront",
        "aws_migration_hub": "MigrationHub",
        "aws_sns_topic": "SNS",
        "aws_vpc": "VPC",
        "aws_iot": "IotCore",
        "aws_iot_certificate": "IotCertificate",
        "aws_iot_policy": "IotPolicy",
        "aws_iot_type": "IotCore",  # TODO: need to fix with new diagram release
        "aws_iot_billing_group": "IotCore",  # TODO: need to fix with new diagram release
        "aws_iot_job": "IotJobs",
        "aws_alexa_skill": "IotAlexaSkill",
        "aws_acm": "ACM",
        "aws_mq": "MQ",
        "aws_athena": "Athena",
        "aws_artifact": "Artifact",
        "aws_batch": "Artifact",
        "aws_billingconsole": "General",  # TODO: need to fix with new diagram release
        "aws_ce": "CostExplorer",
        "aws_lex": "Lex",
        "aws_chime": "Chime",
        "aws_clouddirectory": "CloudDirectory",
        "aws_cloudformation": "Cloudformation",
        "aws_cloudhsm": "CloudHSM",
        "aws_cloudsearch": "Cloudsearch",
        "aws_codebuild": "Codebuild",
        "aws_codecommit": "Codecommit",
        "aws_codedeploy": "Codedeploy",
        "aws_codepipeline": "Codepipeline",
        "aws_codestar": "Codestar",
        "aws_discovery": "ApplicationDiscoveryService",
        "aws_dax": "DynamodbDax",
        "aws_deeplens": "Deeplens",
        "aws_delivery_logs": "General",  # TODO: need to fix with new diagram release
        "aws_diode": "General",  # TODO: need to fix with new diagram release
        "aws_directconnect": "DirectConnect",
        "aws_dlm": "General",  # TODO: need to fix with new diagram release
        "aws_ds": "DirectoryService",
        "aws_dynamodb": "Dynamodb",
        "aws_ecr": "EC2ContainerRegistry",
        "aws_efs": "ElasticFileSystemEFS",
        "aws_elastictranscoder": "ElasticTranscoder",
        "aws_events": "Eventbridge",
        "aws_freertos": "FreeRTOS",
        "aws_fsx": "Fsx",
        "aws_gamelift": "Gamelift",
        "aws_glacier": "S3Glacier",
        "aws_greengrass": "Greengrass",
        "aws_guardduty": "Guardduty",
        "aws_health": "General",  # TODO: need to fix with new diagram release
        "aws_iam": "IAM",
        "aws_importexport": "General",  # TODO: need to fix with new diagram release
        "aws_jellyfish": "General",  # TODO: need to fix with new diagram release
        "aws_kinesis": "Kinesis",
        "aws_kinesisanalytics": "KinesisDataAnalytics",
        "aws_kms": "KMS",
        "aws_lakeformation": "LakeFormation",
        "aws_license_manager": "LicenseManager",
        "aws_lightsail": "Lightsail",
        "aws_logs": "General",  # TODO: need to fix with new diagram release
        "aws_machinelearning": "MachineLearning",
        "aws_macie": "Macie",
        "aws_managedservices": "ManagedServices",
        "aws_marketplace": "Marketplace",
        "aws_mobile_hub": "General",  # TODO: need to fix with new diagram release
        "aws_monitoring": "General",  # TODO: need to fix with new diagram release
        "aws_opsworks": "Opsworks",
        "aws_pinpoint": "Pinpoint",
        "aws_polly": "Polly",
        "aws_qldb": "QLDB",
        "aws_ram": "ResourceAccessManager",
        "aws_redshift": "Redshift",
        "aws_rekognition": "Rekognition",
        "aws_resource_groups": "General",  # TODO: need to fix with new diagram release
        "aws_robomaker": "Robomaker",
        "aws_route53": "Route53",
        "aws_s3": "S3",
        "aws_secretsmanager": "SecretsManager",
        "aws_serverlessrepo": "ServerlessApplicationRepository",
        "aws_servicecatalog": "ServiceCatalog",
        "aws_servicediscovery": "General",  # TODO: need to fix with new diagram release
        "aws_ses": "SimpleEmailServiceSes",
        "aws_shield": "Shield",
        "aws_signer": "General",  # TODO: need to fix with new diagram release
        "aws_signin": "General",  # TODO: need to fix with new diagram release
        "aws_sms": "ServerMigrationService",
        "aws_sso": "SingleSignOn",
        "aws_states": "General",  # TODO: need to fix with new diagram release
        "aws_storagegateway": "StorageGateway",
        "aws_support": "Support",
        "aws_swf": "General",  # TODO: need to fix with new diagram release
        "aws_tagging": "General",  # TODO: need to fix with new diagram release
        "aws_transfer": "MigrationAndTransfer",
        "aws_translate": "Translate",
        "aws_tts": "General",  # TODO: need to fix with new diagram release
        "aws_vmie": "EC2",
        "aws_waf": "WAF",
        "aws_workdocs": "Workdocs",
        "aws_worklink": "Worklink",
        "aws_workmail": "Workmail",
        "aws_workspaces": "Workspaces",
        "aws_xray": "XRay",
        "aws_spotfleet": "EC2",
        "aws_sqs": "SQS",
        "aws_connect": "Connect",
        "aws_iotsitewise": "IotSitewise",
        "aws_neptune_cluster": "Neptune",
        "aws_alexa_for_business": "AlexaForBusiness",
        "aws_customer_gateway": "SiteToSiteVpn",
        "aws_vpn_connection": "SiteToSiteVpn",
        "aws_vpn_gateway": "SiteToSiteVpn",
        "aws_vpn_client_endpoint": "ClientVpn",
    }

    resource_styles = build_styles()


def add_resource_to_group(ordered_resources, group, resource):
    if Mapsources.mapresources.get(resource.digest.type) is not None:
        if group in ordered_resources:
            ordered_resources[group].append(resource)
        else:
            ordered_resources[group] = [resource]


class BaseDiagram(object):
    def __init__(self, engine: str = "sfdp"):
        """
        Class to perform data aggregation, diagram generation and image saving

        The class accepts the following parameters
        :param engine:
        """
        self.engine = engine

    def build(
        self,
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
        title: str,
        filename: str,
    ):
        self.make_directories()
        self.generate_diagram(resources, resource_relations, title, filename)

    def group_by_group(
        self, resources: List[Resource], initial_resource_relations: List[ResourceEdge]
    ) -> Dict[str, List[Resource]]:
        # Ordering Resource list to group resources into cluster
        ordered_resources: Dict[str, List[Resource]] = dict()
        for resource in resources:
            if Mapsources.mapresources.get(resource.digest.type) is not None:
                if resource.group in ordered_resources:
                    ordered_resources[resource.group].append(resource)
                else:
                    ordered_resources[resource.group] = [resource]
        return ordered_resources

    def process_relationships(
        self,
        grouped_resources: Dict[str, List[Resource]],
        resource_relations: List[ResourceEdge],
    ) -> List[ResourceEdge]:
        return resource_relations

    @exception
    def generate_diagram(
        self,
        resources: List[Resource],
        initial_resource_relations: List[ResourceEdge],
        title: str,
        filename: str,
    ):
        ordered_resources = self.group_by_group(resources, initial_resource_relations)
        relations = self.process_relationships(
            ordered_resources, initial_resource_relations
        )

        output_filename = PATH_DIAGRAM_OUTPUT + filename
        with Diagram(
            name=title,
            filename=output_filename,
            direction="TB",
            show=False,
            outformat=["dot","png"],
            graph_attr={"nodesep": "2.0", "ranksep": "1.0", "splines": "ortho"},
        ) as d:
            d.dot.engine = self.engine

            self.draw_diagram(ordered_resources=ordered_resources, relations=relations)

        message_handler("\n\nPNG diagram generated", "HEADER")
        message_handler("Check your diagram: " + output_filename + ".png", "OKBLUE")

    def draw_diagram(self, ordered_resources, relations):
        already_drawn_elements = {}

        # Import all AWS nodes
        for module in Mapsources.diagrams_modules:
            exec("from diagrams.aws." + module + " import *")

        nodes: Dict[ResourceDigest, any] = {}
        # Iterate resources to draw it
        for group_name in ordered_resources:
            if group_name == "":
                for resource in ordered_resources[group_name]:
                    node = eval(Mapsources.mapresources.get(resource.digest.type))(resource.name)
                    nodes[resource.digest] = node
            else:
                with Cluster(group_name.capitalize() + " resources") as cluster:
                    nodes[ResourceDigest(id=group_name, type=DIAGRAM_CLUSTER)] = cluster
                    for resource in ordered_resources[group_name]:
                        node = eval(Mapsources.mapresources.get(resource.digest.type))(resource.name)
                        nodes[resource.digest] = node

        for resource_relation in relations:
            if resource_relation.from_node == resource_relation.to_node:
                continue
            if (
                resource_relation.from_node in nodes
                and resource_relation.to_node in nodes
            ):
                from_node = nodes[resource_relation.from_node]
                to_node = nodes[resource_relation.to_node]
                if resource_relation.from_node not in already_drawn_elements:
                    already_drawn_elements[resource_relation.from_node] = {}
                if (
                    resource_relation.to_node
                    not in already_drawn_elements[resource_relation.from_node]
                ):
                    from_node >> Edge(label=resource_relation.label) >> to_node
                    already_drawn_elements[resource_relation.from_node][resource_relation.to_node] = True

    @staticmethod
    def make_directories():
        Path(PATH_DIAGRAM_OUTPUT).mkdir(parents=True, exist_ok=True)


class NoDiagram(BaseDiagram):
    def __init__(self):
        """
        Special class that doesn't generate any image.

        Command should be refactored not to have such class
        """
        super().__init__("")

    def generate_diagram(
        self,
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
        title: str,
        filename: str,
    ):
        pass

    def build(
        self,
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
        title: str,
        filename: str,
    ):
        pass


class VPCDiagramsNetDiagram(BaseDiagram):
    def generate_diagram(
        self,
        resources: List[Resource],
        initial_resource_relations: List[ResourceEdge],
        title: str,
        filename: str,
    ):
        ordered_resources = self.group_by_group(resources, initial_resource_relations)
        relations = self.process_relationships(
            ordered_resources,
            initial_resource_relations
        )
        diagram = self.build_diagram(
            ordered_resources,
            relations,
            resources,
            initial_resource_relations
        )
        output_filename = PATH_DIAGRAM_OUTPUT + filename + ".drawio"

        with open(output_filename, "w") as diagram_file:
            diagram_file.write(diagram)

        message_handler("\n\nDiagrams.net diagram generated", "HEADER")
        message_handler("Check your diagram: " + output_filename, "OKBLUE")

        super().generate_diagram(
            ordered_resources,
            initial_resource_relations,
            title,
            filename
        )

    # pylint: disable=too-many-locals,too-many-statements
    def build_diagram(
        self,
        resources: Dict[str, List[Resource]],
        resource_relations: List[ResourceEdge],
        initial_resources: List[Resource],
        initial_resource_relations: List[ResourceEdge],
    ):
        diagrams = DIAGRAM_TEMPLATE.format_map(
            {
                "PAGE_ID": "PAGE-1",
                "PAGE_TITLE": "VPC - Generic",
                "CELLS": self.render_vpc_generic(
                    resources,
                    resource_relations,
                    initial_resources,
                    initial_resource_relations
                )
            }
        )
        diagrams += DIAGRAM_TEMPLATE.format_map(
            {
                "PAGE_ID": "PAGE-2",
                "PAGE_TITLE": "VPC - With AZ",
                "CELLS": self.render_vpc_with_az(
                    resources,
                    resource_relations,
                    initial_resources,
                    initial_resource_relations
                )
            }
        )
        return MX_FILE_TEMPLATE.format_map(
            {
                "HOST": "app.diagrams.net",
                "MODIFIED": datetime.datetime.utcnow().isoformat(),
                "DIAGRAMS": diagrams
            }
        )

    def render_vpc_generic(
        self,
        resources: Dict[str, List[Resource]],
        resource_relations: List[ResourceEdge],
        initial_resources: List[Resource],
        initial_resource_relations: List[ResourceEdge],
    ) -> str:
        mxgraph_cells = ""
        cell_id = 1

        vpc_resource = self.get_vpc_resource(initial_resources)
        added_resources: List[ResourceDigest] = []
        vpc_box_height = 56565656
        subnet_box_height = 424242
        vpc_cell_id = f"zB3y0Dp3mfEUP9Fxs3Er-{cell_id}"

        if vpc_resource.overview is None or vpc_resource.overview == {}:
            mxgraph_cells += CELL_TEMPLATE.format_map(
                {
                    "CELL_IDX": vpc_cell_id,
                    "PARENT": "1",
                    "X": "0",
                    "Y": "0",
                    "STYLE": Mapsources.resource_styles["aws_vpc_group"],
                    "TITLE": vpc_resource.name,
                    "W": "1300",
                    "H": vpc_box_height,
                }
            )
        else:
            mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                {
                    "CELL_IDX": vpc_cell_id,
                    "PARENT": "1",
                    "X": "0",
                    "Y": "0",
                    "STYLE": Mapsources.resource_styles["aws_vpc_group"],
                    "TITLE": vpc_resource.name,
                    "W": "1300",
                    "H": vpc_box_height,
                    "TOOLTIP": self.get_tooltip(
                        vpc_resource.overview,
                        vpc_resource.digest.type
                    )
                }
            )

        cell_id += 1

        public_rows = 0
        private_rows = 0

        has_public_resources = self.has_subnet_type(
            PUBLIC_SUBNET,
            resource_relations
        )
        has_private_resources = self.has_subnet_type(
            PRIVATE_SUBNET,
            resource_relations
        )

        subnet_box_width = "600"
        if not has_public_resources & has_private_resources:
            subnet_box_width = "880"

        if has_public_resources:
            public_subnet_x = 40
            public_subnet_y = 40
            cell_id += 1
            public_subnet = CELL_TEMPLATE.format_map(
                {
                    "CELL_IDX": CELL_ID_MAP[PUBLIC_SUBNET],
                    "PARENT": vpc_cell_id,
                    "X": str(public_subnet_x),
                    "Y": str(public_subnet_y),
                    "STYLE": Mapsources.resource_styles["aws_public_subnet_group"],
                    "TITLE": "Public subnet",
                    "W": subnet_box_width,
                    "H": subnet_box_height,
                }
            )
            mxgraph_cells += public_subnet

            (mxgraph_cells, public_rows) = self.render_subnet_items(
                added_resources,
                mxgraph_cells,
                PUBLIC_SUBNET,
                resource_relations,
                resources,
                has_private_resources,
            )

        if has_private_resources:
            private_subnet_x = 680
            private_subnet_y = 40
            cell_id += 1
            private_subnet = CELL_TEMPLATE.format_map(
                {
                    "CELL_IDX": CELL_ID_MAP[PRIVATE_SUBNET],
                    "PARENT": vpc_cell_id,
                    "X": str(private_subnet_x),
                    "Y": str(private_subnet_y),
                    "STYLE": Mapsources.resource_styles["aws_private_subnet_group"],
                    "TITLE": "Private subnet",
                    "W": subnet_box_width,
                    "H": subnet_box_height,
                }
            )
            mxgraph_cells += private_subnet

            (mxgraph_cells, private_rows) = self.render_subnet_items(
                added_resources,
                mxgraph_cells,
                PRIVATE_SUBNET,
                resource_relations,
                resources,
                has_public_resources,
            )
        subnet_rows = max(public_rows, private_rows)
        new_subnet_box_height = subnet_rows * DIAGRAM_ROW_HEIGHT + 40

        mxgraph_cells = mxgraph_cells.replace(
            str(subnet_box_height),
            str(new_subnet_box_height)
        )

        count = 0
        row = 0
        public_subnet_x = 0
        offset = 60
        for _, resource_group in resources.items():
            for resource in resource_group:
                if resource.digest.type in ["aws_subnet", "aws_vpc"]:
                    continue
                if resource.digest not in added_resources:
                    added_resources.append(resource.digest)
                    style = (
                        Mapsources.resource_styles[resource.digest.type]
                        if resource.digest.type in Mapsources.resource_styles
                        else Mapsources.resource_styles["aws_general"]
                    )

                    if resource.overview is None or resource.overview == {}:
                        mxgraph_cells += CELL_TEMPLATE.format_map(
                            {
                                "CELL_IDX": resource.digest.to_string(),
                                "PARENT": vpc_cell_id,
                                "X": str(count * 120 + public_subnet_x + offset),
                                "Y": str(new_subnet_box_height + row * DIAGRAM_ROW_HEIGHT + offset),
                                "STYLE": style.replace("fontSize=12", "fontSize=8"),
                                "TITLE": resource.name,
                                "W": "50",
                                "H": "50",
                            }
                        )
                    else:
                        mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                            {
                                "CELL_IDX": resource.digest.to_string(),
                                "PARENT": vpc_cell_id,
                                "X": str(count * 120 + public_subnet_x + offset),
                                "Y": str(new_subnet_box_height + row * DIAGRAM_ROW_HEIGHT + offset),
                                "STYLE": style.replace("fontSize=12", "fontSize=8"),
                                "TITLE": resource.name,
                                "W": "50",
                                "H": "50",
                                "TOOLTIP": self.get_tooltip(
                                    resource.overview,
                                    resource.digest.type
                                )
                            }
                        )

                    count += 1
                    if count % 6 == 0:
                        row += 1
                        count = 0

        new_vpc_box_height = new_subnet_box_height + DIAGRAM_ROW_HEIGHT * row + 180
        return mxgraph_cells.replace(
            str(vpc_box_height),
            str(new_vpc_box_height)
        )

    def render_vpc_with_az(
        self,
        resources: Dict[str, List[Resource]],
        resource_relations: List[ResourceEdge],
        initial_resources: List[Resource],
        initial_resource_relations: List[ResourceEdge],
    ) -> str:
        cloud_width = 1500
        cloud_height = 765
        cell_padding = 30
        cloud_y_offset = 120
        element_width = 48
        vpc_right_padding = element_width + cell_padding
        cloud_right_padding = vpc_right_padding + cell_padding

        # Internet
        mxgraph_cells = CELL_TEMPLATE.format_map(
            {
                "CELL_IDX": "internet",
                "PARENT": "1",
                "X": (cloud_width/2) - (78 * 2),
                "Y": "20",
                "STYLE": Mapsources.resource_styles["internet"],
                "TITLE": "Internet",
                "W": "78",
                "H": "48",
            }
        )

        # Cloud
        mxgraph_cells += CELL_TEMPLATE.format_map(
            {
                "CELL_IDX": "cloud",
                "PARENT": "1",
                "X": cell_padding,
                "Y": cloud_y_offset,
                "STYLE": Mapsources.resource_styles["aws_cloud"],
                "TITLE": "AWS Cloud",
                "W": cloud_width + cloud_right_padding,
                "H": cloud_height,
            }
        )

        # VPC
        cell_id = 1
        vpc_resource = self.get_vpc_resource(initial_resources)
        added_resources: List[ResourceDigest] = []
        vpc_cell_id = f"vpc-{cell_id}"
        vpc_y_offset = cell_padding
        vpc_width = cloud_width - (cell_padding * 2)
        vpc_height = cloud_height - (cell_padding * 2) - vpc_y_offset

        if vpc_resource.overview is None or vpc_resource.overview == {}:
            mxgraph_cells += CELL_TEMPLATE.format_map(
                {
                    "CELL_IDX": vpc_cell_id,
                    "PARENT": "cloud",
                    "X": cell_padding,
                    "Y": cell_padding + vpc_y_offset,
                    "STYLE": Mapsources.resource_styles["aws_vpc_group"],
                    "TITLE": vpc_resource.name,
                    "W": vpc_width + vpc_right_padding,
                    "H": vpc_height,
                }
            )
        else:
            mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                {
                    "CELL_IDX": vpc_cell_id,
                    "PARENT": "cloud",
                    "X": cell_padding,
                    "Y": cell_padding + vpc_y_offset,
                    "STYLE": Mapsources.resource_styles["aws_vpc_group"],
                    "TITLE": vpc_resource.name,
                    "W": vpc_width + vpc_right_padding,
                    "H": vpc_height,
                    "TOOLTIP": self.get_tooltip(
                        vpc_resource.overview,
                        vpc_resource.digest.type
                    )
                }
            )
        cell_id += 1

        # Internet gateway
        vpc_igw_resource = self.get_vpc_igws(
            initial_resources,
            initial_resource_relations,
            vpc_resource
        )
        if vpc_igw_resource is not None:
            vpc_igw_width = 40
            vpc_igw_height = vpc_igw_width
            if vpc_igw_resource.overview is None or vpc_igw_resource.overview == {}:
                mxgraph_cells += CELL_TEMPLATE.format_map(
                    {
                        "CELL_IDX": vpc_igw_resource.digest.id,
                        "PARENT": vpc_cell_id,
                        "X": (vpc_width / 2) - (vpc_igw_width  / 2) + vpc_right_padding,
                        "Y": (vpc_igw_height / 2) - vpc_igw_height,
                        "STYLE": Mapsources.resource_styles["aws_internet_gateway"],
                        "TITLE": "",
                        "W": vpc_igw_width,
                        "H": vpc_igw_height,
                    }
                )
            else:
                mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                    {
                        "CELL_IDX": vpc_igw_resource.digest.id,
                        "PARENT": vpc_cell_id,
                        "X": (vpc_width / 2) - (vpc_igw_width  / 2) + vpc_right_padding,
                        "Y": (vpc_igw_height / 2) - vpc_igw_height,
                        "STYLE": Mapsources.resource_styles["aws_internet_gateway"],
                        "TITLE": "",
                        "W": vpc_igw_width,
                        "H": vpc_igw_height,
                        "TOOLTIP": self.get_tooltip(
                            vpc_igw_resource.overview,
                            vpc_igw_resource.digest.type
                        )
                    }
                )

            mxgraph_cells += CONNECTOR_TEMPLATE.format_map(
                {
                    "CELL_IDX": f"{vpc_igw_resource.digest.id}_ingress",
                    "PARENT": "1",
                    "STYLE": Mapsources.resource_styles["connection_bidirectional"],
                    "SOURCE": "internet",
                    "TARGET": vpc_igw_resource.digest.id,
                }
            )

        # Availability Zones
        availability_zones = self.get_az_resources(
            initial_resources,
            initial_resource_relations,
            vpc_resource
        )

        number_of_az = len(availability_zones)
        az_y_offset = cell_padding * 2 if vpc_igw_resource is not None else 0
        az_width = (vpc_width - ((number_of_az + 1) * cell_padding)) / number_of_az
        az_height = vpc_height - (cell_padding * 2) - az_y_offset
        az_index = 1

        for az, az_resources in availability_zones.items():
            mxgraph_cells += CELL_TEMPLATE.format_map(
                {
                    "CELL_IDX": az,
                    "PARENT": vpc_cell_id,
                    "X": (cell_padding * az_index) + (az_width * (az_index - 1)),
                    "Y": cell_padding + az_y_offset,
                    "STYLE": Mapsources.resource_styles["aws_az"],
                    "TITLE": az,
                    "W": az_width,
                    "H": az_height,
                }
            )

            # AZ Subnets
            number_of_subnets = len(az_resources)
            subnet_width = az_width - (cell_padding * 2)
            subnet_height = (az_height - ((number_of_subnets + 1) * cell_padding)) / number_of_subnets
            subnet_index = 1
            subnet_ngw_resource = None
            instances_width = element_width
            instances_height = instances_width
            ngw_width = 40
            ngw_height = ngw_width

            az_public_subnet = self.get_zones_public_subnet(
                az_resources,
                initial_resources,
                initial_resource_relations
            )

            if az_public_subnet is not None:
                # Ensure public subnet is always at the front of the list
                az_resources.insert(0, az_resources.pop(az_resources.index(az_public_subnet)))

            for subnet in az_resources:
                subnet_style = Mapsources.resource_styles["aws_private_subnet_group"]
                subnet_isPublic = az_public_subnet is not None and subnet.digest.id == az_public_subnet.digest.id
                if subnet_isPublic:
                    subnet_style = Mapsources.resource_styles["aws_public_subnet_group"]


                if subnet.overview is None or subnet.overview == {}:
                    mxgraph_cells += CELL_TEMPLATE.format_map(
                        {
                            "CELL_IDX": subnet.digest.id,
                            "PARENT": az,
                            "X": cell_padding,
                            "Y": (cell_padding * subnet_index) + (subnet_height * (subnet_index - 1)),
                            "STYLE": subnet_style,
                            "TITLE": subnet.name,
                            "W": subnet_width,
                            "H": subnet_height,
                        }
                    )
                else:
                    mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                        {
                            "CELL_IDX": subnet.digest.id,
                            "PARENT": az,
                            "X": cell_padding,
                            "Y": (cell_padding * subnet_index) + (subnet_height * (subnet_index - 1)),
                            "STYLE": subnet_style,
                            "TITLE": subnet.name,
                            "W": subnet_width,
                            "H": subnet_height,
                            "TOOLTIP": self.get_tooltip(
                                subnet.overview,
                                subnet.digest.type
                            )
                        }
                    )

                if subnet_isPublic and vpc_igw_resource is not None:
                    # Connection public subnet to igw
                    mxgraph_cells += CONNECTOR_TEMPLATE.format_map(
                        {
                            "CELL_IDX": f"{vpc_igw_resource.digest.id}_{subnet.digest.id}_public_ingress_eggress",
                            "PARENT": vpc_cell_id,
                            "STYLE": Mapsources.resource_styles["connection_bidirectional"] + Mapsources.resource_styles["connection_top_middle"],
                            "SOURCE": subnet.digest.id,
                            "TARGET": vpc_igw_resource.digest.id,
                        }
                    )

                # Instances
                mxgraph_cells += CELL_TEMPLATE.format_map(
                    {
                        "CELL_IDX": f"{subnet.digest.id}_instances",
                        "PARENT": subnet.digest.id,
                        "X": (subnet_width / 2) - (instances_width / 2),
                        "Y": (subnet_height / 2) - (instances_height / 2),
                        "STYLE": Mapsources.resource_styles["aws_instances"],
                        "TITLE": "Instances",
                        "W": instances_width,
                        "H": instances_height,
                    }
                )

                if subnet_isPublic:
                    # Nat Gateways
                    subnet_ngw_resource = self.get_subnet_ngws(initial_resources, subnet)
                    if (subnet_ngw_resource is not None):
                        if subnet_ngw_resource.overview is None or subnet_ngw_resource.overview == {}:
                            mxgraph_cells += CELL_TEMPLATE.format_map(
                                {
                                    "CELL_IDX": subnet_ngw_resource.digest.id,
                                    "PARENT": subnet.digest.id,
                                    "X": subnet_width - (cell_padding * 2),
                                    "Y": cell_padding,
                                    "STYLE": Mapsources.resource_styles["aws_nat_gateway"],
                                    "TITLE": "",
                                    "W": ngw_width,
                                    "H": ngw_height,
                                }
                            )
                        else:
                            mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                                {
                                    "CELL_IDX": subnet_ngw_resource.digest.id,
                                    "PARENT": subnet.digest.id,
                                    "X": subnet_width - (cell_padding * 2),
                                    "Y": cell_padding,
                                    "STYLE": Mapsources.resource_styles["aws_nat_gateway"],
                                    "TITLE": "",
                                    "W": ngw_width,
                                    "H": ngw_height,
                                    "TOOLTIP": self.get_tooltip(
                                        subnet_ngw_resource.overview,
                                        subnet_ngw_resource.digest.type
                                    )
                                }
                            )
                elif subnet_ngw_resource is not None:
                    #connection from instance to public subnet's ngw if available
                    mxgraph_cells += CONNECTOR_TEMPLATE.format_map(
                        {
                            "CELL_IDX": f"{vpc_igw_resource.digest.id}_{subnet.digest.id}_private_eggress",
                            "PARENT": az,
                            "STYLE": Mapsources.resource_styles["connection_one_direction"] + Mapsources.resource_styles["connection_top_right"],
                            "SOURCE": subnet.digest.id,
                            "TARGET": subnet_ngw_resource.digest.id,
                        }
                    )
                
                subnet_index += 1

            az_index += 1

        # customer gateways
        customer_gateways = self.get_customer_gateways(initial_resources)
        if customer_gateways is not None:
            number_of_cgws = len(customer_gateways)
            cgw_width = element_width
            cgw_height = cgw_width
            cgw_index = 1
            vpn_y = cloud_y_offset + (cell_padding * 1.5)

            mxgraph_cells += CELL_TEMPLATE.format_map(
                {
                    "CELL_IDX": "datacenters",
                    "PARENT": "1",
                    "X": cloud_width + cloud_right_padding + (cell_padding * 5),
                    "Y": cloud_y_offset,
                    "STYLE": Mapsources.resource_styles["aws_datacenter"],
                    "TITLE": "Data Centers",
                    "W": cgw_width + (cell_padding * 2),
                    "H": (cgw_height + cell_padding) * number_of_cgws + cell_padding,
                }
            )

            for cgw in customer_gateways:
                cgw_y = (cell_padding * 1.5) + ((cgw_height + cell_padding) * (cgw_index - 1))
                if cgw.overview is None or cgw.overview == {}:
                    mxgraph_cells += CELL_TEMPLATE.format_map(
                        {
                            "CELL_IDX": cgw.digest.id,
                            "PARENT": "datacenters",
                            "X": cell_padding,
                            "Y": cgw_y,
                            "STYLE": Mapsources.resource_styles["aws_general"],
                            "TITLE": "",
                            "W": cgw_width,
                            "H": cgw_height,
                        }
                    )
                else:
                    mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                        {
                            "CELL_IDX": cgw.digest.id,
                            "PARENT": "datacenters",
                            "X": cell_padding,
                            "Y": cgw_y,
                            "STYLE": Mapsources.resource_styles["aws_general"],
                            "TITLE": "",
                            "W": cgw_width,
                            "H": cgw_height,
                            "TOOLTIP": self.get_tooltip(
                                cgw.overview,
                                cgw.digest.type
                            )
                        }
                    )

                # vpn connections
                vpn_connections = self.get_vpn_connections(initial_resources, initial_resource_relations, cgw)
                vpn_x = cloud_width + cloud_right_padding + (cell_padding * 2)
                vpn_width = cgw_width
                vpn_height = vpn_width
                for vpn in vpn_connections:
                    if vpn.overview is None or vpn.overview == {}:
                        mxgraph_cells += CELL_TEMPLATE.format_map(
                            {
                                "CELL_IDX": vpn.digest.id,
                                "PARENT": "1",
                                "X": vpn_x,
                                "Y": vpn_y,
                                "STYLE": Mapsources.resource_styles["aws_vpn_connection"],
                                "TITLE": "",
                                "W": vpn_width,
                                "H": vpn_height,
                            }
                        )
                    else:
                        mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                            {
                                "CELL_IDX": vpn.digest.id,
                                "PARENT": "1",
                                "X": vpn_x,
                                "Y": vpn_y,
                                "STYLE": Mapsources.resource_styles["aws_vpn_connection"],
                                "TITLE": "",
                                "W": vpn_width,
                                "H": vpn_height,
                                "TOOLTIP": self.get_tooltip(
                                    vpn.overview,
                                    vpn.digest.type
                                )
                            }
                        )

                    mxgraph_cells += CONNECTOR_TEMPLATE.format_map(
                        {
                            "CELL_IDX": f"{vpn.digest.id}_{cgw.digest.id}",
                            "PARENT": "1",
                            "STYLE": Mapsources.resource_styles["connection_bidirectional"],
                            "SOURCE": vpn.digest.id,
                            "TARGET": cgw.digest.id,
                        }
                    )

                    vpn_y += cell_padding + vpn_height

                cgw_index += 1
            
            # vpn gateways
            vpn_gateways = self.get_vpn_gateways(initial_resources, initial_resource_relations, vpc_resource)
            if vpn_gateways is not None or vpn_gateways != []:
                gateway_width = element_width
                gateway_height = gateway_width
                gateway_x = vpc_width
                gateway_y = cell_padding
                for gateway in vpn_gateways:
                    if gateway.overview is None or gateway.overview == {}:
                        mxgraph_cells += CELL_TEMPLATE.format_map(
                            {
                                "CELL_IDX": gateway.digest.id,
                                "PARENT": vpc_cell_id,
                                "X": gateway_x,
                                "Y": gateway_y,
                                "STYLE": Mapsources.resource_styles["aws_vpn_gateway"],
                                "TITLE": "",
                                "W": gateway_width,
                                "H": gateway_height,
                            }
                        )
                    else:
                        mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                            {
                                "CELL_IDX": gateway.digest.id,
                                "PARENT": vpc_cell_id,
                                "X": gateway_x,
                                "Y": gateway_y,
                                "STYLE": Mapsources.resource_styles["aws_vpn_gateway"],
                                "TITLE": "",
                                "W": gateway_width,
                                "H": gateway_height,
                                "TOOLTIP": self.get_tooltip(
                                    gateway.overview,
                                    gateway.digest.type
                                )
                            }
                        )

                    gateway_y += cell_padding + gateway_width

                    # vpn gateway connections
                    connections = self.get_vpn_gateway_connections(initial_resource_relations, gateway)
                    for connection in connections:
                        mxgraph_cells += CONNECTOR_TEMPLATE.format_map(
                            {
                                "CELL_IDX": f"{gateway.digest.id}_{connection}",
                                "PARENT": "1",
                                "STYLE": Mapsources.resource_styles["connection_bidirectional"] + Mapsources.resource_styles["connection_exit_right_middle_entry_left_middle"],
                                "SOURCE": gateway.digest.id,
                                "TARGET": connection,
                            }
                        )

        return mxgraph_cells

    # pylint: disable=too-many-locals,too-many-arguments
    def render_subnet_items(
        self,
        added_resources,
        mxgraph_cells,
        subnet_id,
        resource_relations,
        resources,
        has_other_subnet,
    ) -> (str, int):
        items_in_row = 6
        if has_other_subnet:
            items_in_row = 3
        count = 0
        row = 0
        offset = 60
        # pylint: disable=too-many-nested-blocks
        for relation in resource_relations:
            if relation.to_node == ResourceDigest(id=subnet_id, type="aws_subnet"):
                for _, resource_group in resources.items():
                    for resource in resource_group:
                        if (
                            resource.digest == relation.from_node
                            and relation.from_node not in added_resources
                        ):
                            added_resources.append(relation.from_node)
                            style = (
                                Mapsources.resource_styles[relation.from_node.type]
                                if relation.from_node.type in Mapsources.resource_styles
                                else Mapsources.resource_styles["aws_general"]
                            )

                            if resource.overview is None or resource.overview == {}:
                                mxgraph_cells += CELL_TEMPLATE.format_map(
                                    {
                                        "CELL_IDX": relation.from_node.to_string(),
                                        "PARENT": CELL_ID_MAP[subnet_id],
                                        "X": str(offset + count * 140),
                                        "Y": str(offset + row * DIAGRAM_ROW_HEIGHT),
                                        "STYLE": style.replace("fontSize=12", "fontSize=8"),
                                        "TITLE": resource.name,
                                        "W": "50",
                                        "H": "50",
                                    }
                                )
                            else:
                                mxgraph_cells += USER_OBJECT_TEMPLATE.format_map(
                                    {
                                        "CELL_IDX": relation.from_node.to_string(),
                                        "PARENT": CELL_ID_MAP[subnet_id],
                                        "X": str(offset + count * 140),
                                        "Y": str(offset + row * DIAGRAM_ROW_HEIGHT),
                                        "STYLE": style.replace("fontSize=12", "fontSize=8"),
                                        "TITLE": resource.name,
                                        "W": "50",
                                        "H": "50",
                                        "TOOLTIP": self.get_tooltip(
                                            resource.overview,
                                            relation.from_node.type
                                        )
                                    }
                                )
                            count += 1

                            if count % items_in_row == 0:
                                row += 1
                                count = 0
        return mxgraph_cells, row + 1

    def get_az_resources(
        self,
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
        vpc_resource: Resource
    ) -> Dict[str, List[Resource]]:
        attached_subnets = self.get_vpc_subnets(resources, resource_relations, vpc_resource)

        if attached_subnets is None or attached_subnets == []:
            return {}

        return {subnet.attributes["AvailabilityZone"]: [innersubnet for innersubnet in attached_subnets if innersubnet.attributes["AvailabilityZone"] == subnet.attributes["AvailabilityZone"]] for subnet in attached_subnets}

    def get_zones_public_subnet(
        self,
        az_resources: List[Resource],
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
    ) -> Resource:
        for resource in az_resources:
            if self.is_subnet_public(resource, resources, resource_relations):
                return resource
        
        return None

    @staticmethod
    def is_subnet_public(
        resource: Resource,
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
    ) -> bool:
        if resource.digest.type != "aws_subnet":
            return False

        for relation in resource_relations:
            if relation.from_node.type == "aws_route_table" and (
                relation.to_node == resource.digest or (
                    relation.to_node.type == "aws_vpc" and
                    relation.to_node.id == resource.attributes["VpcId"]
                )
            ):
                for route_table in resources:
                    if route_table.digest == relation.from_node:
                        return route_table.attributes["IsPublic"]

        return False

    @staticmethod
    def get_tooltip(overview: dict[str, object], resource_type: str) -> str:
        dir_template = Environment(
            loader=FileSystemLoader(
                os.path.dirname(os.path.abspath(__file__)) + "/../templates/"
            ),
            trim_blocks=True,
        )
        output = escape(
            dir_template.get_template("overview_html.html").render(
                resource_overview=overview,
                resource_type=resource_type
            )
        )
        return ''.join(output.splitlines())

    @staticmethod
    def has_subnet_type(subnet_id, resource_relations) -> bool:
        for relation in resource_relations:
            if relation.to_node == ResourceDigest(id=subnet_id, type="aws_subnet"):
                return True
        return False

    @staticmethod
    def get_customer_gateways(
        resources: List[Resource]
    ) -> List[Resource]:
        return [resource for resource in resources if resource.digest.type == "aws_customer_gateway"]

    @staticmethod
    def get_vpn_connections(
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
        cgw_resource: Resource
    ) -> List[Resource]:
        vpn_connections = [relation.from_node.id for relation in resource_relations if relation.to_node.id == cgw_resource.digest.id and relation.from_node.type == "aws_vpn_connection"]

        if vpn_connections is None or vpn_connections == []:
            return []

        return [resource for resource in resources if resource.digest.id in vpn_connections]

    @staticmethod
    def get_vpn_gateways(
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
        vpc_resource: Resource
    ) -> List[Resource]:
        attached_gateways = [relation.from_node.id for relation in resource_relations if relation.to_node.id == vpc_resource.digest.id and relation.from_node.type == "aws_vpn_gateway"]

        if attached_gateways is None or attached_gateways == []:
            return []

        return [resource for resource in resources if resource.digest.id in attached_gateways]

    @staticmethod
    def get_vpn_gateway_connections(
        resource_relations: List[ResourceEdge],
        gateway_resource: Resource
    ) -> List[str]:
        return [relation.from_node.id for relation in resource_relations if relation.to_node.id == gateway_resource.digest.id and relation.from_node.type == "aws_vpn_connection"]

    @staticmethod
    def get_vpc_resource(resources: List[Resource]) -> Resource:
        vpc_resource = None

        for resource in resources:
            if resource.digest.type == "aws_vpc":
                if vpc_resource is None:
                    vpc_resource = resource
                else:
                    raise Exception("Only one VPC in a region is currently supported.")

        if vpc_resource is None:
            raise Exception("At least one VPC is required.")

        return vpc_resource

    @staticmethod
    def get_vpc_subnets(
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
        vpc_resource: Resource
    ) -> List[Resource]:
        attached_subnets = [relation.from_node.id for relation in resource_relations if relation.to_node.id == vpc_resource.digest.id and relation.from_node.type == "aws_subnet"]

        if attached_subnets is None or attached_subnets == []:
            return []

        return [resource for resource in resources if resource.digest.id in attached_subnets]

    @staticmethod
    def get_vpc_igws(
        resources: List[Resource],
        resource_relations: List[ResourceEdge],
        vpc_resource: Resource
    ) -> Resource:
        attached_igw = [relation.from_node.id for relation in resource_relations if relation.to_node.id == vpc_resource.digest.id and relation.from_node.type == "aws_internet_gateway"]

        if attached_igw is None or attached_igw == []:
            return None

        igws = [resource for resource in resources if resource.digest.id in attached_igw]
        return igws[0] if igws != [] else None

    @staticmethod
    def get_subnet_ngws(
        resources: List[Resource],
        subnet_resource: Resource
    ) -> Resource:

        ngws = [resource for resource in resources if resource.digest.type == "aws_nat_gateway" and resource.attributes["SubnetId"] == subnet_resource.digest.id]
        return ngws[0] if ngws != [] else None

    @staticmethod
    def decode_inflate(value: str):
        decoded = base64.b64decode(value)
        try:
            result = zlib.decompress(decoded, -15)
        # pylint: disable=broad-except
        except Exception:
            result = decoded
        return result.decode("utf-8")

    @staticmethod
    def deflate_encode(value: str):
        return base64.b64encode(zlib.compress(value.encode("utf-8"))[2:-4]).decode(
            "utf-8"
        )