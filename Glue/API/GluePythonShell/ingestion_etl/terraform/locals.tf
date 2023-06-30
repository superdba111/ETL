locals {
#redshift_glue_connector is defined for each environments in their respective files
redshift_glue_connector = var.terraform_workspace_name == "pull-request" ? "${var.redshift_glue_connector}-${var.terraform_workspace_branch}" : var.redshift_glue_connector
job_connections         = ["${local.redshift_glue_connector}"]
} 