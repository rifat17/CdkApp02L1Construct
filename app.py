#!/usr/bin/env python3
import aws_cdk as cdk
from typing import cast

from aws_pdk.cdk_graph import CdkGraph, ICdkGraphPlugin
from aws_pdk.cdk_graph_plugin_diagram import (
    CdkGraphDiagramPlugin,
    DiagramFormat,
)

from cdk_app_02_l1.cdk_app_02_l1_stack import CdkApp02L1Stack
from cdk_app_02_l1.constants import REGION, STACK_NAME, ACCOUNT


app = cdk.App()
CdkApp02L1Stack(
    app,
    STACK_NAME,
    env=cdk.Environment(account=ACCOUNT, region=REGION),
)

# app.synth()


graph_plugin = CdkGraphDiagramPlugin(
    diagrams=[
        {
            "name": "cdk_graph_diagram",
            "title": "AWS stack",
            "format": DiagramFormat.PNG,
        }
    ]
)
graph = CdkGraph(app, plugins=[cast(ICdkGraphPlugin, graph_plugin)])

if __name__ == "__main__":
    app.synth()
    graph.report()
