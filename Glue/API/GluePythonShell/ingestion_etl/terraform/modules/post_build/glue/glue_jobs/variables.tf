variable "netsuite_jobs" {}
variable "zoho_campaign_jobs" {}
variable "zoho_crm_jobs" {
}
variable "dayforce_jobs" {}
variable "region_name" {
}

variable "s3_bucket_name" {
}

variable "s3_raw_bucket_name" {}

variable "s3_temp_bucket_name" {}

variable "workspace_branch" {}


variable "secret_name_netsuite" {}
variable "secret_name_zoho" {}
variable "secret_name_dayforce" {}

variable "database_netsuite" {}
variable "database_zoho" {}
variable "database_dayforce" {}
variable "redshift_glue_connector" {}


variable "create" {
  default = true
}

variable "dpu" {
  default = 2
}


variable "command_name" {
  default = ""
}

variable "language" {
  default = "python"
}

variable "bookmark" {
  default     = "disabled"
  description = "It can be enabled, disabled or paused."
}

variable "bookmark_options" {
  type = map(string)

  default = {
    enabled  = "job-bookmark-enable"
    disabled = "job-bookmark-disable"
    paused   = "job-bookmark-pause"
  }
}

variable "max_concurrent" {
  default = 1
}

variable "arguments" {
  type    = map(string)
  default = {}
}

#Parameters
variable "organization" {}

variable "environment" {}

variable "name" {
  type        = string
  description = "(Required) Name that will be used for identify resources."
}

variable "tags" {

}

variable "database_zoho_campaign" {}

variable "zoho_campaign_script_location" {
  type        = string
  description = "(Required) Specifies the S3 path to a script that executes a job."
}

variable "netsuite_script_location" {
  type        = string
  description = "(Required) Specifies the S3 path to a script that executes a job."
}

variable "zoho_script_location" {
  type        = string
  description = "(Required) Specifies the S3 path to a script that executes a job."
}

variable "job_type" {
  type        = string
  default     = "glueetl"
  description = "pythonshell is for glue python, glueetl is for spark"
}

variable "python_version" {
  type        = number
  default     = 3
  description = "(Optional) The Python version being used to execute a Python shell job."

  validation {
    condition     = contains([3, 3.9], var.python_version)
    error_message = "Allowed values are 3( refers to 3.6) or 3.9 is allowed."
  }
}

variable "connections" {
  type = list(string)
}

variable "description" {
  type        = string
  default     = "Glue Job Ingestion"
  description = "(Optional) Description of the job."
}

variable "max_concurrent_runs" {
  type        = number
  default     = 1
  description = "(Optional) The maximum number of concurrent runs allowed for a job."
}

variable "glue_version" {
  type        = string
  default     = "4.0"
  description = "(Optional) The version of glue to use."
}

variable "max_retries" {
  type        = number
  default     = 0
  description = "(Optional) The maximum number of times to retry this job if it fails."
}

variable "notify_delay_after" {
  type        = number
  default     = null
  description = "(Optional) After a job run starts, the number of minutes to wait before sending a job run delay notification."
}

variable "role_arn" {
  description = "(Optional) The ARN of the IAM role associated with this job."
}


variable "timeout" {
  type        = number
  default     = 2880
  description = "(Optional) The job timeout in minutes."
}

variable "worker_type" {
  type        = string
  default     = "G.2X"
  description = "(Optional) G.1X and G.2X The type of predefined worker that is allocated when a job runs."

  validation {
    condition     = contains(["Standard", "G.1X", "G.2X"], var.worker_type)
    error_message = "Accepts a value of Standard, G.1X, or G.2X."
  }
}

variable "create_worker_type" {
  type        = bool
  default     = false
  description = "(Optional) Define worker type in case of glueetl"
}

variable "number_of_workers" {
  type        = number
  default     = 2
  description = "(Optional) The number of workers of a defined workerType that are allocated when a job runs."
}

variable "create_number_of_workers" {
  type        = bool
  default     = false
  description = "(Optional) Define number of workers in case glueetl"
}

variable "max_capacity" {
  type        = number
  default     = 1 #default 0.0625
  description = "(Optional) max_capacity needs to be set if pythonshell is chosen"
}


variable "security_configuration" {
  type        = string
  default     = ""
  description = "(Optional) The name of the Security Configuration to be associated with the job."
}

variable "create_security_configuration" {
  type        = bool
  default     = false
  description = "(Optional) Create AWS Glue Security Configuration associated with the job."
}

variable "security_configuration_cloudwatch_encryption" {
  type = object({
    cloudwatch_encryption_mode = string
    kms_key_arn                = string
  })
  default = {
    cloudwatch_encryption_mode = "DISABLED"
    kms_key_arn                = null
  }
  description = "(Optional) A cloudwatch_encryption block which contains encryption configuration for CloudWatch."
}

variable "security_configuration_job_bookmarks_encryption" {
  type = object({
    job_bookmarks_encryption_mode = string
    kms_key_arn                   = string
  })
  default = {
    job_bookmarks_encryption_mode = "DISABLED"
    kms_key_arn                   = null
  }
  description = "(Optional) A job_bookmarks_encryption block which contains encryption configuration for job bookmarks."
}

variable "security_configuration_s3_encryption" {
  type = object({
    s3_encryption_mode = string
    kms_key_arn        = string
  })
  default = {
    s3_encryption_mode = "DISABLED"
    kms_key_arn        = null
  }
  description = "(Optional) A s3_encryption block which contains encryption configuration for S3 data."
}


variable "log_group_retention_in_days" {
  type        = number
  default     = 7
  description = "(Optional) The default number of days log events retained in the glue job log group."
}


variable "job_language" {
  type        = string
  default     = "python"
  description = "(Optional) The script programming language."

  validation {
    condition     = contains(["scala", "python"], var.job_language)
    error_message = "Accepts a value of 'scala' or 'python'."
  }
}

variable "class" {
  type        = string
  default     = null
  description = "(Optional) The Scala class that serves as the entry point for your Scala script."
}

#variable "extra_py_files" {
#  type    = list(string)
#  default = [
#    "s3://zoho-api-test-fuat/glue-python/zoho_glue_source_codes/commonPythonGlueLib-1.0.0-py3-none-any.whl",
#    "s3://einc-og-poc-testing/zoho_library/glue_python_shell_og_zcrm-0.1-py3-none-any.whl"
#  ]
#  description = "(Optional) The Amazon S3 paths to additional Python modules that AWS Glue adds to the Python path before executing your script."
#}

variable "extra_jars" {
  type        = list(string)
  default     = []
  description = "(Optional) The Amazon S3 paths to additional Java .jar files that AWS Glue adds to the Java classpath before executing your script."
}

variable "user_jars_first" {
  type        = bool
  default     = null
  description = "(Optional) Prioritizes the customer's extra JAR files in the classpath."
}

variable "use_postgres_driver" {
  type        = bool
  default     = null
  description = "(Optional) Prioritizes the Postgres JDBC driver in the class path to avoid a conflict with the Amazon Redshift JDBC driver."
}

variable "extra_files" {
  type        = list(string)
  default     = []
  description = "(Optional) The Amazon S3 paths to additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it."
}

variable "job_bookmark_option" {
  type        = string
  default     = "job-bookmark-disable"
  description = "(Optional) Controls the behavior of a job bookmark."

  validation {
    condition = contains([
      "job-bookmark-enable", "job-bookmark-disable", "job-bookmark-pause"
    ], var.job_bookmark_option)
    error_message = "Accepts a value of 'job-bookmark-enable', 'job-bookmark-disable' or 'job-bookmark-pause'."
  }
}

variable "temp_dir" {
  type        = string
  default     = null
  description = "(Optional) Specifies an Amazon S3 path to a bucket that can be used as a temporary directory for the job."
}

variable "enable_s3_parquet_optimized_committer" {
  type        = bool
  default     = true
  description = "(Optional) Enables the EMRFS S3-optimized committer for writing Parquet data into Amazon S3."
}

variable "enable_rename_algorithm_v2" {
  type        = bool
  default     = true
  description = "(Optional) Sets the EMRFS rename algorithm version to version 2."
}

variable "enable_glue_datacatalog" {
  type        = bool
  default     = true
  description = "(Optional) Enables you to use the AWS Glue Data Catalog as an Apache Spark Hive metastore."
}

variable "enable_metrics" {
  type        = bool
  default     = true
  description = "(Optional) Enables the collection of metrics for job profiling for job run."
}

variable "enable_continuous_cloudwatch_log" {
  type        = bool
  default     = true
  description = "(Optional) Enables real-time continuous logging for AWS Glue jobs."
}

variable "enable_continuous_log_filter" {
  type        = bool
  default     = true
  description = "(Optional) Specifies a standard filter or no filter when you create or edit a job enabled for continuous logging."
}

variable "continuous_log_stream_prefix" {
  type        = string
  default     = null
  description = "(Optional) Specifies a custom CloudWatch log stream prefix for a job enabled for continuous logging."
}

variable "continuous_log_conversion_pattern" {
  type        = string
  default     = null
  description = "(Optional) Specifies a custom conversion log pattern for a job enabled for continuous logging."
}

variable "enable_spark_ui" {
  type        = bool
  default     = false
  description = "(Optional) Enable Spark UI to monitor and debug AWS Glue ETL jobs."
}

variable "spark_event_logs_path" {
  type        = string
  default     = null
  description = "(Optional) Specifies an Amazon S3 path. When using the Spark UI monitoring feature."
}

variable "additional_python_modules" {
  type        = list(string)
  default     = ["awswrangler","PyJWT","cryptography","pyjwt[crypto]"]
  description = "(Optional) List of Python modules to add a new module or change the version of an existing module."
}
#variable "s3_bucket_name" {
#  description = "Netsuite and Zoho bucket"
#  type = string
#  default = "zoho-api-test-fuat"
#}

variable "use_auth" {
  type        = string
  default     = "N"
  description = "(Optional) Set it to Y when using auth for netsuite"
}