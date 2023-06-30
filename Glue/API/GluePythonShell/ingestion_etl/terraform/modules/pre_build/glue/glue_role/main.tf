resource "aws_iam_role" "glue" {
  name               = "AWSGlueServiceRoleIngestion${var.workspace_branch}"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sts:AssumeRole"
        ]
        Principal = {
          "Service" = "glue.amazonaws.com"
        }
      }
    ]
  })
  tags = var.tags

}

#Define custom policy
#resource "aws_iam_role_policy" "ingestion_s3_policy" {
#  name = "ingestion_s3_policy"
#  role = "${aws_iam_role.glue.id}"
#  policy = <<EOF
#{
#  "Version": "2012-10-17",
#  "Statement": [
#    {
#      "Effect": "Allow",
#      "Action": [
#        "s3:*"
#      ],
#      "Resource": [
#        "arn:aws:s3:::${var.s3_bucket_name}",
#        "arn:aws:s3:::${var.s3_bucket_name}/*"
#      ]
#    }
#  ]
#}
#EOF
#}

#resource "aws_iam_role_policy_attachment" "glue_service" {
#  role       = "${aws_iam_role.glue.id}"
#  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
#}





resource "aws_iam_role_policy" "ingestion_s3_policy" {
  name   = "AWSGlueServiceRoleIngestionS3Policy"
  role   = "${aws_iam_role.glue.id}"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "glue:*",
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:ListAllMyBuckets",
                "s3:GetBucketAcl",
                "ec2:DescribeVpcEndpoints",
                "ec2:DescribeRouteTables",
                "ec2:CreateNetworkInterface",
                "ec2:DeleteNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcAttribute",
                "iam:ListRolePolicies",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "cloudwatch:PutMetricData"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::${var.s3_bucket_name}/*",
                "arn:aws:s3:::${var.s3_bucket_name}",
                "arn:aws:s3:::${var.s3_raw_bucket_name}/*",
                "arn:aws:s3:::${var.s3_raw_bucket_name}",
                "arn:aws:s3:::${var.s3_temp_bucket_name}/*",
                "arn:aws:s3:::${var.s3_temp_bucket_name}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::crawler-public*",
                "arn:aws:s3:::${var.s3_bucket_name}*",
                "arn:aws:s3:::${var.workspace_branch}*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::crawler-public*",
                "arn:aws:s3:::einc-og-poc-testing*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:*:*:/aws-glue/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:DeleteTags"
            ],
            "Condition": {
                "ForAllValues:StringEquals": {
                    "aws:TagKeys": [
                        "aws-glue-service-resource"
                    ]
                }
            },
            "Resource": [
                "arn:aws:ec2:*:*:network-interface/*",
                "arn:aws:ec2:*:*:security-group/*",
                "arn:aws:ec2:*:*:instance/*"
            ]
        },
        {
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Effect": "Allow",
            "Resource": "*"
        },
        {
        "Effect": "Allow",
        "Action": [
          "glue:*"
        ],
        "Resource": [
          "arn:aws:glue:*:*:catalog",
          "arn:aws:glue:*:*:database/${var.database_netsuite}",
          "arn:aws:glue:*:*:table/${var.database_netsuite}/*",
          "arn:aws:glue:*:*:database/${var.database_zoho}",
          "arn:aws:glue:*:*:table/${var.database_zoho}/*",
          "arn:aws:glue:*:*:database/${var.database_dayforce}",
          "arn:aws:glue:*:*:table/${var.database_dayforce}/*"
        ]
      },
      {
        "Effect": "Allow",
        "Action": [
            "lakeformation:GetDataAccess",
            "lakeformation:GrantPermissions"
        ],
        "Resource": ["*"]
      },
      {
        "Action": [
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ],
        "Effect": "Allow",
        "Resource": "${var.kms_role_arn}"
      },
      {
        "Action": [
          "redshift:*"
        ],
        "Effect": "Allow",
        "Resource": "*"
      }


    ]
}
EOF
}


