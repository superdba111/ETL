variable "role_arn" {
  type        = string
  default     = ""
  description = "(Optional) The ARN of the IAM role associated with this job."
}
variable "role_id" {
  type        = string
  default     = ""
  description = "(Optional) The ID of the IAM role associated with this job."
}

variable "s3_bucket_name" {}

variable "s3_temp_bucket_name" {}

variable "database_netsuite" {}

variable "database_zoho" {}

variable "database_dayforce" {}

variable "environment" {
  type = string
}

variable "workspace_branch" {
  type = string
}
variable "s3_raw_bucket_name" {}

variable "kms_role_arn" {}

variable "tags" {}

