#!/usr/bin/env python3
import os

import aws_cdk as cdk

from test_cross_regon.ap_northeast_1 import CloudFrontStack
from test_cross_regon.us_east_1 import Wafv2Stack

app = cdk.App()

# ScopeをCloudFrontとするため、us-east-1にStackを作成する
wafv2_stack = Wafv2Stack(
    app, 'Wafv2Stack', env=cdk.Environment(region='us-east-1'),
    cross_region_references=True,
)

# ap-northeast-1のStackでCloudFrontを作成する
cloudfront_stack = CloudFrontStack(
    app, 'CloudFrontStack', wafv2_stack.webacl,
    env=cdk.Environment(region='ap-northeast-1'),
    cross_region_references=True,
)

app.synth()