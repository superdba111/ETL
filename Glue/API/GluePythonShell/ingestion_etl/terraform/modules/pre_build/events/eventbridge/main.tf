locals {
  emails = var.emails
}


resource "aws_cloudwatch_event_rule" "console" {
  name          = "capture_glue_job_status"
  description   = "Glue Job State Change"
  tags          = var.tags
  event_pattern = <<EOF
{
  "source": ["aws.glue"],
  "detail-type": ["Glue Job State Change"],
  "detail": {
    "severity": ["ERROR"],
    "state": ["FAILED", "ERROR", "STOPPED"],
    "$or": [
      { "jobName": [{ "prefix": "einc_netsuite_" }] },
      { "jobName": [{ "prefix": "einc_zoho_" }] },
      { "jobName": [{ "prefix": "einc_dayforce_" }] }
    ]
  }
}
EOF
}

resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.console.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.glue_jobs_status.arn
  input_transformer {
    input_paths = {
      jobname = "$.detail.jobName",
      state   = "$.detail.state",
      time    = "$.time"
    }
    input_template = "\"Glue job: [<jobname>] => State: [<state>] => Time: [<time>]\""
  }


}

resource "aws_sns_topic" "glue_jobs_status" {
  name = "glue_jobs_status"
  tags = var.tags
}


resource "aws_sns_topic_subscription" "topic_email_subscription" {
  count     = length(local.emails)
  topic_arn = aws_sns_topic.glue_jobs_status.arn
  protocol  = "email"
  endpoint  = local.emails[count.index]
}

resource "aws_sns_topic_policy" "default" {
  arn    = aws_sns_topic.glue_jobs_status.arn
  policy = data.aws_iam_policy_document.sns_topic_policy.json
}

data "aws_iam_policy_document" "sns_topic_policy" {
  statement {
    effect  = "Allow"
    actions = ["SNS:Publish"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    resources = [aws_sns_topic.glue_jobs_status.arn]
  }
}