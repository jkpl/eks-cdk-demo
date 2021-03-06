#!/usr/bin/env python3

import os

from aws_cdk import (
    core,
)

import infra.network
import infra.cluster_users
import infra.eks

# Config

name = os.getenv('ENV_NAME', 'mytest')
cluster_name = name
tags = {
    'Team': 'kubebois'
}
cluster_version = '1.14'
env = core.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'), # if not set, CDK will not detect all available AZs
    region=os.getenv('CDK_DEFAULT_REGION', 'eu-central-1')
)

# Stacks

app = core.App()
network_stack = infra.network.EksNetworkStack(
    scope=app,
    id=name + '-network',
    cidr_id=100,
    cluster_name=cluster_name,
    env=env,
    tags=tags,
)
cluster_stack = infra.eks.EksStack(
    scope=app,
    id=name + '-eks',
    cluster_name=cluster_name,
    cluster_version=cluster_version,
    vpc=network_stack.vpc,
    env=env,
    tags=tags,
)
cluster_users_stack = infra.cluster_users.EksClusterUsersStack(
    scope=app,
    id=name + '-users',
    clusters=[cluster_stack.cluster],
    env=env,
    tags=tags,
)

# Synthesize!

app.synth()
