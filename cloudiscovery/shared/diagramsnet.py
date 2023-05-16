MX_FILE_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="{HOST}" modified="{MODIFIED}" agent="cloudiscovery" version="13.7.7" type="device">
   {DIAGRAMS}
</mxfile>
"""

DIAGRAM_TEMPLATE = """
<diagram id="{PAGE_ID}" name="{PAGE_TITLE}">
    <mxGraphModel dx="1186" dy="773" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="900" pageHeight="1169" math="0" shadow="0" background="#ffffff">
    <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        {CELLS}
    </root>
    </mxGraphModel>
</diagram>"""

CELL_TEMPLATE = """
<mxCell id="{CELL_IDX}" value="{TITLE}" style="{STYLE}" vertex="1" parent="{PARENT}">
   <mxGeometry x="{X}" y="{Y}" width="{W}" height="{H}" as="geometry" />
</mxCell>
"""

USER_OBJECT_TEMPLATE = """
<UserObject label="{TITLE}" tooltip="{TOOLTIP}" id="{CELL_IDX}">
    <mxCell style="{STYLE}" vertex="1" parent="{PARENT}">
        <mxGeometry x="{X}" y="{Y}" width="{W}" height="{H}" as="geometry" />
    </mxCell>
</UserObject>
"""

CONNECTOR_TEMPLATE = """
<mxCell id="{CELL_IDX}" style="{STYLE}" edge="1" parent="{PARENT}" source="{SOURCE}" target="{TARGET}">
    <mxGeometry relative="1" as="geometry" />
</mxCell>
"""

def _add_general_resources(styles):
    points = "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
    n1 = (
        "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;collapsible=0;recursiveResize=0;"
        "shape=mxgraph.aws4.group;fillColor=none;verticalAlign=top;dashed=0;autosize=1;fixedWidth=1;"
    )

    n2 = (
        "gradientDirection=north;outlineConnect=0;fontColor=#232F3E;gradientColor=#505863;fillColor=#1E262E;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    n3 = "spacingLeft=30;align=left;"
    n4 = "grIcon=mxgraph.aws4.group_security_group;grStroke=0;"

    styles["aws_cloud"] = points + n1 + n3 + "strokeColor=#232F3E;fontColor=#232F3E;grIcon=mxgraph.aws4.group_aws_cloud;"
    styles["aws_vpc_group"] = points + n1 + n3 + "fillColor=#FFFFFF;fontColor=#AAB7B8;strokeColor=#248814;grIcon=mxgraph.aws4.group_vpc;"
    styles["aws_az"] = n1 + "strokeColor=#147EBA;dashed=1;fontColor=#147EBA;"
    styles["aws_private_subnet_group"] = points + n1 + n4 + "fillColor=#E6F2F8;fontColor=#147EBA;strokeColor=#147EBA;"
    styles["aws_public_subnet_group"] = points + n1 + n4 + "fillColor=#E9F3E6;fontColor=#248814;strokeColor=#248814;"
    styles["aws_datacenter"] = points + n1 + n3 +"strokeColor=#5A6C86;fontColor=#5A6C86;grIcon=mxgraph.aws4.group_corporate_data_center;"
    styles["aws_general"] = n2 + "resIcon=mxgraph.aws4.general;"

    styles["connection_bidirectional"] = "strokeColor=#000000;edgeStyle=orthogonalEdgeStyle;html=1;jettySize=auto;orthogonal=1;orthogonalLoop=1;startFill=1;endFill=1;startArrow=classic;noJump=0;rounded=1;jumpStyle=none;"
    styles["connection_one_direction"] = "strokeColor=#000000;edgeStyle=orthogonalEdgeStyle;html=1;jettySize=auto;orthogonal=1;orthogonalLoop=1;startFill=1;endFill=0;noJump=0;rounded=1;jumpStyle=none;"

    styles["connection_top_middle"] = "exitX=0.5;exitY=0;exitDx=0;exitDy=0;"
    styles["connection_top_right"] = "exitX=0.75;exitY=0;exitDx=0;exitDy=0;"
    styles["connection_exit_right_middle_entry_left_middle"] = "entryX=0;entryY=0.5;entryDx=0;entryDy=0;"


def _add_analytics_resources(styles):
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#945DF2;gradientDirection=north;fillColor=#5A30B5;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )
    styles["aws_athena"] = n2 + "resIcon=mxgraph.aws4.athena;"
    styles["aws_elasticsearch_domain"] = n2 + "resIcon=mxgraph.aws4.elasticsearch_service;"
    styles["aws_emr"] = n2 + "resIcon=mxgraph.aws4.emr;"
    styles["aws_emr_cluster"] = n2 + "resIcon=mxgraph.aws4.emr;"
    styles["aws_kinesis"] = n2 + "resIcon=mxgraph.aws4.kinesis;"
    styles["aws_kinesisanalytics"] = n2 + "resIcon=mxgraph.aws4.kinesis_data_analytics;"
    styles["aws_kinesis_firehose"] = n2 + "resIcon=mxgraph.aws4.kinesis_data_firehose;"
    styles["aws_quicksight"] = n2 + "resIcon=mxgraph.aws4.quicksight;"
    styles["aws_redshift"] = n2 + "resIcon=mxgraph.aws4.redshift;"
    styles["aws_data_pipeline"] = n2 + "resIcon=mxgraph.aws4.data_pipeline;"
    styles["aws_msk_cluster"] = n2 + "resIcon=mxgraph.aws4.managed_streaming_for_kafka;"
    styles["aws_glue"] = n2 + "resIcon=mxgraph.aws4.glue;"
    styles["aws_lakeformation"] = n2 + "resIcon=mxgraph.aws4.lake_formation;"


def _add_application_integration_resources(styles):
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#F34482;gradientDirection=north;fillColor=#BC1356;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    styles["aws_sns_topic"] = n2 + "resIcon=mxgraph.aws4.sns;"
    styles["aws_sqs"] = n2 + "resIcon=mxgraph.aws4.sqs;"
    styles["aws_appsync_graphql_api"] = n2 + "resIcon=mxgraph.aws4.appsync;"
    styles["aws_events"] = n2 + "resIcon=mxgraph.aws4.eventbridge;"


def _add_compute_resources(styles):
    n = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#D05C17;strokeColor=none;dashed=0;"
        "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"
        "pointerEvents=1;whiteSpace=wrap;"
    )
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#F78E04;gradientDirection=north;fillColor=#D05C17;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    styles["aws_instance"] = n2 + "resIcon=mxgraph.aws4.ec2;"
    styles["aws_instances"] = "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#D45B07;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.instances;"
    styles["aws_autoscaling_group"] = n2 + "resIcon=mxgraph.aws4.auto_scaling2;"
    styles["aws_batch"] = n2 + "resIcon=mxgraph.aws4.batch;"
    styles["aws_elastic_beanstalk_environment"] = n2 + "resIcon=mxgraph.aws4.elastic_beanstalk;"
    styles["aws_lambda_function"] = n + "shape=mxgraph.aws4.lambda_function;"


def _add_container_resources(styles):
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#F78E04;gradientDirection=north;fillColor=#D05C17;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    styles["aws_eks_cluster"] = n2 + "resIcon=mxgraph.aws4.eks;"
    styles["aws_ecr"] = n2 + "resIcon=mxgraph.aws4.ecr;"
    styles["aws_ecs_cluster"] = n2 + "resIcon=mxgraph.aws4.ecs;"


def _add_customer_engagement_resources(styles):
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#4D72F3;gradientDirection=north;fillColor=#3334B9;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    styles["aws_connect"] = n2 + "resIcon=mxgraph.aws4.connect;"
    styles["aws_pinpoint"] = n2 + "resIcon=mxgraph.aws4.pinpoint;"
    styles["aws_ses"] = n2 + "resIcon=mxgraph.aws4.simple_email_service;"


def _add_database_resources(styles):
    n = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#3334B9;strokeColor=none;dashed=0;"
        "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"
        "pointerEvents=1;whiteSpace=wrap;"
    )
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#4D72F3;gradientDirection=north;fillColor=#3334B9;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    styles["aws_docdb_cluster"] = n2 + "resIcon=mxgraph.aws4.documentdb_with_mongodb_compatibility;"
    styles["aws_dynamodb"] = n2 + "resIcon=mxgraph.aws4.dynamodb;"
    styles["aws_elasticache_cluster"] = n2 + "resIcon=mxgraph.aws4.elasticache;"
    styles["aws_neptune_cluster"] = n2 + "resIcon=mxgraph.aws4.neptune;"
    styles["aws_redshift"] = n2 + "resIcon=mxgraph.aws4.redshift;"
    styles["aws_db_instance"] = n + "shape=mxgraph.aws4.rds_instance;"
    styles["aws_dax"] = n + "shape=mxgraph.aws4.dynamodb_dax;"


def _add_ml_resources(styles):
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#4AB29A;gradientDirection=north;fillColor=#116D5B;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    styles["aws_sagemaker"] = n2 + "resIcon=mxgraph.aws4.sagemaker;"


def _add_management_governance_resources(styles):
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#F34482;gradientDirection=north;fillColor=#BC1356;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    styles["aws_cloudwatch"] = n2 + "resIcon=mxgraph.aws4.cloudwatch_2;"
    styles["aws_autoscaling_group"] = n2 + "resIcon=mxgraph.aws4.autoscaling;"
    styles["aws_auto_scaling"] = n2 + "resIcon=mxgraph.aws4.autoscaling;"
    styles["aws_cloudformation"] = n2 + "resIcon=mxgraph.aws4.cloudformation;"


def _add_network_resources(styles):
    points = "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
    n = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#5A30B5;strokeColor=none;dashed=0;"
        "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"
        "pointerEvents=1;whiteSpace=wrap;"
    )
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#945DF2;gradientDirection=north;fillColor=#5A30B5;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    styles["aws_vpc"] = n2 + "resIcon=mxgraph.aws4.vpc;"
    styles["aws_api_gateway_rest_api"] = n2 + "resIcon=mxgraph.aws4.api_gateway;"
    styles["aws_cloudfront_distribution"] = n2 + "resIcon=mxgraph.aws4.cloudfront;"
    styles["aws_vpn_client_endpoint"] = n2 + "resIcon=mxgraph.aws4.client_vpn;"
    styles["aws_elb"] = n2 + "resIcon=mxgraph.aws4.elastic_load_balancing;"
    styles["aws_directconnect"] = n2 + "resIcon=mxgraph.aws4.direct_connect;"
    styles["aws_global_accelerator"] = n2 + "resIcon=mxgraph.aws4.global_accelerator;"

    styles["aws_route_table"] = n + "shape=mxgraph.aws4.route_table;"
    styles["aws_vpc_endpoint_gateway"] = n + "shape=mxgraph.aws4.gateway;"
    styles["aws_internet_gateway"] = n + "shape=mxgraph.aws4.internet_gateway;"
    styles["aws_nat_gateway"] = n + "shape=mxgraph.aws4.nat_gateway;"
    styles["aws_network_acl"] = n + "shape=mxgraph.aws4.network_access_control_list;"
    styles["aws_elb_classic"] = n + "shape=mxgraph.aws4.classic_load_balancer;"
    styles["aws_vpn_connection"] = n + "shape=mxgraph.aws4.vpn_connection;"
    styles["aws_vpn_gateway"] = n + "shape=mxgraph.aws4.vpn_gateway;"

    styles["internet"] = "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#232F3D;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.internet;"

def _add_storage_resources(styles):
    n = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#277116;strokeColor=none;dashed=0;"
        "verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;"
        "pointerEvents=1;whiteSpace=wrap;"
    )
    n2 = (
        "outlineConnect=0;fontColor=#232F3E;gradientColor=#60A337;gradientDirection=north;fillColor=#277116;"
        "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
        "fontSize=12;fontStyle=0;aspect=fixed;whiteSpace=wrap;shape=mxgraph.aws4.resourceIcon;"
    )

    styles["aws_efs_file_system"] = n2 + "resIcon=mxgraph.aws4.elastic_file_system;"
    styles["aws_fsx"] = n2 + "resIcon=mxgraph.aws4.fsx;"
    styles["aws_s3"] = n + "shape=mxgraph.aws4.bucket;"


def build_styles():
    styles = {}
    _add_general_resources(styles)
    _add_analytics_resources(styles)
    _add_application_integration_resources(styles)
    _add_compute_resources(styles)
    _add_container_resources(styles)
    _add_customer_engagement_resources(styles)
    _add_database_resources(styles)
    _add_ml_resources(styles)
    _add_management_governance_resources(styles)
    _add_network_resources(styles)
    _add_storage_resources(styles)
    return styles
