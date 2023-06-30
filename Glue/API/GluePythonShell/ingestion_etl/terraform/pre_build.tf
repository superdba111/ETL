module "pre_build" {
  source = "./modules/pre_build"
  providers = {
    aws = aws.environment
  }

  // General configuration
  environment         = var.terraform_environment_name
  workspace           = var.terraform_workspace_name
  workspace_branch    = var.terraform_workspace_branch
  emails              = var.emails
  s3_create           = var.s3_create
  s3_raw_bucket_name  = var.s3_raw_bucket_name
  s3_bucket_name      = var.s3_bucket_name
  s3_temp_bucket_name = var.s3_temp_bucket_name
  kms_role_arn        = var.kms_role_arn

  cluster_name            = var.cluster_name
  redshift_credentials    = var.redshift_credentials
  availability_zone       = var.availability_zone
  subnet_id               = var.subnet_id
  redshift_jdbc_url_name  = var.redshift_jdbc_url_name
  redshift_glue_connector = local.redshift_glue_connector
  tags                    = var.tags
  trigger_type            = var.trigger_type
  container_build         = var.container_build

}

output "pre_build" {
  value     = module.pre_build
  sensitive = false
}
