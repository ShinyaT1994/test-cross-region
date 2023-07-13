import os

import aws_cdk as cdk

from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    App,
    aws_wafv2 as wafv2_,
)

class Wafv2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # WebACLを作成
        self.webacl = wafv2_.CfnWebACL(
            self,
            'WebAcl',
            default_action={'allow': {}},
            scope='CLOUDFRONT',
            name='my-webacl',
            visibility_config=wafv2_.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name='webacl',
                sampled_requests_enabled=True,
            ),
            rules=[
                wafv2_.CfnWebACL.RuleProperty(
                    name='custom-basic-auth-rule',
                    priority=1,
                    statement=wafv2_.CfnWebACL.StatementProperty(
                        not_statement=wafv2_.CfnWebACL.NotStatementProperty(
                            statement=wafv2_.CfnWebACL.StatementProperty(
                                byte_match_statement = \
                                    wafv2_.CfnWebACL.ByteMatchStatementProperty(
                                        field_to_match= \
                                            wafv2_.CfnWebACL.FieldToMatchProperty(
                                                single_header={'name': 'authorization'},
                                            ),
                                        positional_constraint='EXACTLY',
                                        text_transformations= [
                                            wafv2_.CfnWebACL.TextTransformationProperty(
                                                priority=0,
                                                type='NONE'
                                            )
                                        ],
                                        # コマンドライン等で作成したusername:passwordのBase64Encode
                                        search_string='Basic dGVzdDp0ZXN0',
                                    ),
                            ),
                        ),
                    ),
                    visibility_config=wafv2_.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name='custom-basic-auth-rule',
                        sampled_requests_enabled=True,
                    ),
                    action=wafv2_.CfnWebACL.RuleActionProperty(
                        block=wafv2_.CfnWebACL.BlockActionProperty(
                            custom_response= \
                                wafv2_.CfnWebACL.CustomResponseProperty(
                                    response_code=401,
                                    response_headers=[
                                        wafv2_.CfnWebACL.CustomHTTPHeaderProperty(
                                            name='www-authenticate',
                                            value='Basic'
                                        )
                                    ],
                                ),
                        ),
                    ),
                ),
            ],
        )