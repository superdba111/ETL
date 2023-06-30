module "glue_role" {
  source             = "./glue/glue_role"
  s3_bucket_name     = local.bucket_name
  database_netsuite  = local.database_netsuite
  database_zoho      = local.database_zoho
  database_dayforce = local.database_dayforce
  environment        = var.environment
  workspace_branch   = local.workspace_branch
  s3_raw_bucket_name = local.s3_raw_bucket_name
  s3_temp_bucket_name = var.s3_temp_bucket_name
  kms_role_arn       = var.kms_role_arn
  tags               = var.tags
}


module "glue_database" {
  source            = "./glue/glue_database"
  database_netsuite = local.database_netsuite
  database_zoho     = local.database_zoho
  database_dayforce = local.database_dayforce
  role_arn          = module.glue_role.glue_role_arn
  depends_on        = [module.glue_role]
}


module "s3_utils" {
  source         = "./s3"
  s3_bucket_name = local.bucket_name
  environment    = var.environment
  depends_on     = [module.glue_database]
  s3_create      = var.s3_create
  tags           = var.tags
}

module "events" {
  source = "./events/eventbridge"
  emails = var.emails
  tags   = var.tags
}

module "glue_connection" {
  source                  = "./glue/glue_connection"
  cluster_name            = var.cluster_name
  redshift_credentials    = var.redshift_credentials
  availability_zone       = var.availability_zone
  subnet_id               = var.subnet_id
  redshift_jdbc_url_name  = var.redshift_jdbc_url_name
  redshift_glue_connector = var.redshift_glue_connector
  tags                    = var.tags
}
