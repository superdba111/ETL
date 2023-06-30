locals {
  ingestion_bucket_arn     = "arn:aws:s3:::${var.s3_bucket_name}"
  ingestion_raw_bucket_arn = "arn:aws:s3:::${var.s3_raw_bucket_name}"
}

module "post_build" {
  source    = "./modules/post_build"
  providers = {
    aws = aws.environment
  }

  // General configuration
  environment           = var.terraform_environment_name
  workspace             = var.terraform_workspace_name
  workspace_branch      = var.terraform_workspace_branch
  region                = var.terraform_environment_region
  trigger_name          = var.trigger_name
  zoho_trigger_schedule = var.zoho_trigger_schedule
  trigger_job           = var.trigger_job
  terraform_state_path  = var.terraform_state_path

  trigger_type        = var.trigger_type
  trigger_enabled     = var.trigger_enabled
  trigger_description = var.trigger_description
  trigger_arguments   = var.trigger_arguments
  trigger_timeout     = var.trigger_timeout

  netsuite_jobs  = var.netsuite_jobs
  zoho_crm_jobs    = var.zoho_crm_jobs
  dayforce_jobs     = var.dayforce_jobs
  organization   = var.organization
  create_trigger = var.create_trigger


  database_zoho_campaign = var.database_zoho_campaign
#  zoho_campaign_script_location = var.zoho_campaign_script_location
  zoho_campaign_jobs = var.zoho_campaign_jobs
  database_dayforce = var.database_dayforce


  job_role_arn = var.job_role_arn

  connections              = local.job_connections
  job_name                 = var.job_name
  job_dpu                  = var.job_dpu
  job_arguments            = var.job_arguments
  job_language             = var.job_language
  job_bookmark             = var.job_bookmark
  job_temp_dir             = var.job_temp_dir
  ingestion_bucket_arn     = local.ingestion_bucket_arn
  ingestion_raw_bucket_arn = local.ingestion_raw_bucket_arn
  glue_role_arn            = module.pre_build.glue_role_arn
  s3_create                = var.s3_create
  s3_raw_bucket_name       = var.s3_raw_bucket_name
  s3_bucket_name           = var.s3_bucket_name
  s3_temp_bucket_name      = var.s3_temp_bucket_name
  redshift_glue_connector  = var.redshift_glue_connector
  tags                     = var.tags
  depends_on               = [
    module.pre_build
  ]
}

output "post_build" {
  value     = module.post_build
  sensitive = false
}
 