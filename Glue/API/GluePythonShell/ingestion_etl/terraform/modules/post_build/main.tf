#glue job
module "glue_jobs" {
  source = "./glue/glue_jobs"

  create = var.create_job

  name                     = format("%s%s", var.job_name, local.workspace_branch)
  role_arn                 = var.create_role ? local.glue_role_arn : var.job_role_arn
  netsuite_script_location = local.netsuite_job_script
  zoho_script_location     = local.zoho_job_script
  zoho_campaign_script_location = local.zoho_campaign_job_script

  #  connections = ["${var.job_connections}"]
  dpu              = var.job_dpu
  arguments        = var.job_arguments
  language         = var.job_language
  bookmark         = var.job_bookmark
  temp_dir         = var.job_temp_dir
  environment      = var.environment
  workspace_branch = local.workspace_branch

  s3_bucket_name     = local.bucket_name
  s3_raw_bucket_name = local.s3_raw_bucket_name
  s3_temp_bucket_name = var.s3_temp_bucket_name
  region_name        = var.region

  secret_name_netsuite = local.secret_name_netsuite
  database_netsuite    = local.database_netsuite
  netsuite_jobs        = var.netsuite_jobs

  database_zoho_campaign = var.database_zoho_campaign
  zoho_campaign_jobs = var.zoho_campaign_jobs
  zoho_crm_jobs      = var.zoho_crm_jobs
  secret_name_zoho = local.secret_name_zoho
  database_zoho    = local.database_zoho

  dayforce_jobs     = var.dayforce_jobs
  secret_name_dayforce = local.secret_name_dayforce
  database_dayforce    = local.database_dayforce
  #dayforce_script_location = local.dayforce_job_scriptm


  redshift_glue_connector = local.redshift_glue_connector
  connections             = var.connections

  organization = var.organization
  tags         = var.tags

}


##Glue job trigger
module "glue_trigger" {
  source = "./glue/glue_trigger"

  create = var.create_trigger

  name          = format("%s%s", var.trigger_name, local.workspace_branch)
  schedule_zoho = var.zoho_trigger_schedule
  job_name      = format("%s%s", var.trigger_job, local.workspace_branch)

  type        = var.trigger_type
  enabled     = var.trigger_enabled
  description = var.trigger_description
  arguments   = var.trigger_arguments
  timeout     = var.trigger_timeout

  netsuite_jobs    = var.netsuite_jobs
  zoho_crm_jobs      = var.zoho_crm_jobs
  dayforce_jobs      = var.dayforce_jobs
  organization     = var.organization
  environment      = var.environment
  workspace_branch = local.workspace_branch
  tags             = var.tags
  depends_on = [module.glue_jobs]

}

module "lake_formation" {
  source              = "./lake_formation"
  role_arn            = local.glue_role_arn
  netsuite_glue_db    = local.database_netsuite
  zoho_glue_db        = local.database_zoho
  dayforce_glue_db    = local.database_dayforce
  s3_location_arn     = var.ingestion_bucket_arn
  s3_raw_location_arn = var.ingestion_raw_bucket_arn
}
