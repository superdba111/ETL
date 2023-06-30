#Parameters
variable "organization" {
  type        = string
  default     = "einc"
  description = "(Optional) Organization abbreviation that will be prefixed to resource names."
}

variable "environment" {
  type        = string
  description = "(Required) Environment name."
  default     = "dev"
}


variable "region" {
  type = string
}
variable "netsuite_jobs" {}

variable "dayforce_jobs" {}

variable "zoho_campaign_jobs" {}


variable "zoho_crm_jobs" {

}

variable "s3_bucket_name" {
}

variable "s3_temp_bucket_name" {}

variable "database_netsuite" {
  description = "Netsuite database name"
  type        = string
  default     = "netsuite_data_ingestion"
}

variable "database_zoho" {
  description = "Zoho database name"
  type        = string
  default     = "zoho_data_ingestion"
}

variable "database_zoho_campaign" {
  description = "Zoho database name"
  type        = string
}


variable "database_dayforce" {
  description = "Dayforce database name"
  type        = string
}

#variable "zoho_campaign_script_location" {
#  description = "Zoho database name"
#  type        = string
#}

variable "secret_name_netsuite" {
  description = "Netsuite secrets"
  type        = string
  default     = "netsuite/user/pass/secrets"
}

variable "secret_name_zoho" {
  description = "Zoho secrets"
  type        = string
  default     = "zoho/user/pass/secrets"
}


variable "secret_name_dayforce" {
  description = "Dayforce secrets"
  type        = string
  default     = "dayforce/user/pass/secrets"
}

variable "redshift_glue_connector" {
}


variable "create_job" {
  default = true
}

variable "job_name" {
  default = ""
}

variable "glue_role_arn" {
  type = string
}

variable "ingestion_bucket_arn" {
  type = string
}

variable "ingestion_raw_bucket_arn" {}

variable "job_role_arn" {
  default = ""
}

variable "create_role" {
  type        = bool
  default     = true
  description = "(Optional) Create AWS IAM role associated with the job."
}

variable "connections" {
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
  type    = map(string)
  default = {}
}

# ---- aws_glue_trigger
variable "create_trigger" {
  default = true
}

variable "trigger_name" {
  default = "glue_trigger"
}


variable "zoho_trigger_schedule" {
  type    = list(string)
  default = [
    "cron(52 13 * * ? *)"
  ]
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
  type    = map(string)
  default = {}
}

variable "trigger_timeout" {
  default = 2880
}

variable "workspace" {
  type    = string
  default = ""
}

variable "workspace_branch" {
  type    = string
  default = ""
}

variable "s3_create" {}

variable "s3_raw_bucket_name" {}

variable "tags" {}