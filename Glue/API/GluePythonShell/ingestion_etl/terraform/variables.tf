#Parameters
variable "organization" {
  type        = string
  default     = "einc"
  description = "(Optional) Organization abbreviation that will be prefixed to resource names."
}


variable "netsuite_jobs" {
}

variable "dayforce_jobs" {}


variable "redshift_glue_connector" {
  type        = string
  description = "Redshift Glue Connector"
}

variable "zoho_crm_jobs" {
}

variable "s3_bucket_name" {
  description = "Netsuite and Zoho bucket"
  type        = string
}

variable "database_netsuite" {
  description = "Netsuite database name"
  type        = string
}

variable "database_zoho" {
  description = "Zoho database name"
  type        = string
}

variable "secret_name_netsuite" {
  description = "Netsuite secrets"
  type        = string
}

variable "secret_name_zoho" {
  description = "Zoho secrets"
  type        = string
}

variable "create_job" {
  default = true
}

variable "job_name" {
  default = ""
}

variable "job_role_arn" {
  default = ""
}

variable "create_role" {
  type        = bool
  description = "(Optional) Create AWS IAM role associated with the job."
}

variable "job_connections" {
  type = list(string)
}

variable "job_dpu" {
  default = 2
}

variable "job_language" {
  default = "python"
}

variable "job_bookmark" {
  default = "disabled"
}

variable "job_temp_dir" {
  default = ""
}

variable "job_arguments" {
  type = map(string)
}

# ---- aws_glue_trigger
variable "create_trigger" {
  default = true
}

variable "trigger_name" {
  default = "glue_trigger"
}


variable "zoho_trigger_schedule" {
  type = list(string)
}

variable "trigger_job" {
  default = "glue_trigger_job"
}

variable "trigger_type" {
  description = "It can be CONDITIONAL, ON_DEMAND, and SCHEDULED."
}

variable "trigger_enabled" {
  default = true
}

variable "trigger_description" {
  default = ""
}

variable "trigger_arguments" {
  type = map(string)
}

variable "trigger_timeout" {
  default = 2880
}

variable "database_zoho_campaign" {}
variable "database_dayforce" {}

#variable "zoho_campaign_script_location" {}
variable "zoho_campaign_jobs" {}
variable "emails" {}

variable "s3_create" {}

variable "s3_raw_bucket_name" {}

variable "s3_temp_bucket_name" {}

variable "kms_role_arn" {}

variable "cluster_name" {
}

variable "redshift_credentials" {
}

variable "availability_zone" {
}

variable "subnet_id" {
}

variable "redshift_jdbc_url_name" {

}
variable "tags" {

}

variable "container_build" {
  type = string
  default = "false"
}
