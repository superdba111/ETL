
locals {
  database_netsuite       = var.workspace == "pull-request" ? "${var.database_netsuite}_${var.environment}_db_${var.workspace_branch}" : "${var.database_netsuite}_${var.environment}_db"
  database_zoho           = var.workspace == "pull-request" ? "${var.database_zoho}_${var.environment}_db_${var.workspace_branch}" : "${var.database_zoho}_${var.environment}_db"
  database_zoho_campaign  = var.workspace == "pull-request" ? "${var.database_zoho_campaign}_${var.environment}_db_${var.workspace_branch}" : "${var.database_zoho_campaign}_${var.environment}_db"
  database_dayforce       = var.workspace == "pull-request" ? "${var.database_dayforce}_${var.environment}_db_${var.workspace_branch}" : "${var.database_dayforce}_${var.environment}_db"
  secret_name_netsuite    = var.workspace == "production" ? "prod/${var.secret_name_netsuite}" : "dev/${var.secret_name_netsuite}"
  secret_name_zoho        = var.workspace == "production" ? "prod/${var.secret_name_zoho}" : "dev/${var.secret_name_zoho}"
  secret_name_dayforce    = var.workspace == "production" ? "prod/${var.secret_name_dayforce}" : "dev/${var.secret_name_dayforce}"

  glue_role_arn           = var.glue_role_arn
  #bucket_name             = var.workspace == "" ? "${var.s3_bucket_name}-${var.environment}" : "${var.s3_bucket_name}-${var.environment}-${var.workspace_branch}"
  #bucket_name             = var.s3_create  ? "${var.s3_bucket_name}-${var.environment}" : "${var.s3_bucket_name}"
  bucket_name             = "${var.s3_bucket_name}"
  netsuite_job_script     = "s3://${local.bucket_name}/glue-python/glue_source_codes/netSuitePythonGlueJob/netSuitePythonGlueJob.py"
  zoho_job_script         = "s3://${local.bucket_name}/glue-python/glue_source_codes/zohoPythonGlueJob/zohoCrmPythonGlueJob.py"
  zoho_campaign_job_script = "s3://${local.bucket_name}/glue-python/glue_source_codes/zohoPythonGlueJob/zohoCampaignPythonGlueJob.py"
  #dayforce_job_script      = "s3://${local.bucket_name}/glue-python/glue_source_codes/dayForcePythonGlueJob/${var.dayforce_script_name}"

  redshift_glue_connector = "${var.redshift_glue_connector}"
  #terraform_environment_region = "${var.region}"
  workspace_branch        = var.workspace == "pull-request" ? "-${var.workspace_branch}" : ""
  s3_raw_bucket_name      = var.s3_create ? "${local.bucket_name}" : "${var.s3_raw_bucket_name}"


}
