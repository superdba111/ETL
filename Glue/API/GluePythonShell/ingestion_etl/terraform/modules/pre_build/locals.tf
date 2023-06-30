locals {
  #bucket_name       = var.workspace == "" ? "${var.s3_bucket_name}-${var.environment}" : "${var.s3_bucket_name}-${var.environment}-${var.workspace_branch}"
  #bucket_name        = var.s3_create  ? "${var.s3_bucket_name}-${var.environment}" : "${var.s3_bucket_name}"
  bucket_name        = "${var.s3_bucket_name}"
  database_netsuite  = var.workspace == "pull-request" ? "${var.database_netsuite}_${var.environment}_db_${var.workspace_branch}" : "${var.database_netsuite}_${var.environment}_db"
  database_zoho      = var.workspace == "pull-request" ? "${var.database_zoho}_${var.environment}_db_${var.workspace_branch}" : "${var.database_zoho}_${var.environment}_db"
  database_dayforce  = var.workspace == "pull-request" ? "${var.database_dayforce}_${var.environment}_db_${var.workspace_branch}" : "${var.database_dayforce}_${var.environment}_db"
  workspace_branch   = var.workspace == "pull-request" ? "-${var.workspace_branch}" : ""
  s3_raw_bucket_name = var.s3_create ? "${local.bucket_name}" : "${var.s3_raw_bucket_name}"

}
