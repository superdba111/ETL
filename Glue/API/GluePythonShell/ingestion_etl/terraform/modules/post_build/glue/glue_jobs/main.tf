locals {
  full_name               = "${var.organization}${var.workspace_branch}"
  tags                    = var.tags
  extra_py_files_netsuite = [
    "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/commonPythonGlueLib-1.0.0-py3-none-any.whl"
    #"s3://${var.s3_bucket_name}/zoho_library/glue_python_shell_og_zcrm-0.1-py3-none-any.whl"
  ]
  extra_py_files_zoho = [
    "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/commonPythonGlueLib-1.0.0-py3-none-any.whl",
    #"s3://${var.s3_bucket_name}/zoho_library/glue_python_shell_og_zcrm-0.1-py3-none-any.whl"
  ]
  extra_py_files_zoho_campaign = [
    "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/commonPythonGlueLib-1.0.0-py3-none-any.whl"
    #"s3://${var.s3_bucket_name}/zoho_library/glue_python_shell_og_zcrm-0.1-py3-none-any.whl"
  ]
  extra_py_files_dayforce = [
    "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/commonPythonGlueLib-1.0.0-py3-none-any.whl"
    #"s3://${var.s3_bucket_name}/zoho_library/glue_python_shell_og_zcrm-0.1-py3-none-any.whl"
  ]
  extra_jars = [
    "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/NQjc.jar"
    #"s3://${var.s3_bucket_name}/zoho_library/glue_python_shell_og_zcrm-0.1-py3-none-any.whl"
  ]
  env = "ingestion_etl_${var.environment}"

}


resource "aws_glue_job" "netsuite_glue_job" {

  for_each = var.netsuite_jobs

  name                   = "${local.full_name}_netsuite_${each.key}_${each.value.run_mode}"
  role_arn               = var.role_arn
  connections            = var.connections
  description            = "${var.description} - ${each.key}"
  glue_version           = var.glue_version
  max_retries            = var.max_retries
  timeout                = var.timeout
  security_configuration = var.create_security_configuration ? join("", aws_glue_security_configuration.sec_cfg.*.id) : var.security_configuration
  worker_type            = var.worker_type
  number_of_workers      = var.number_of_workers
  tags                   = local.tags
  #max_capacity           = var.max_capacity

  command {
    name            = var.job_type
    script_location = var.netsuite_script_location
    python_version  = var.python_version
  }

  default_arguments = {
    "--job-language"                          = var.job_language
    "--class"                                 = var.class
    "--extra-py-files"                        = length(local.extra_py_files_netsuite) > 0 ? join(",", local.extra_py_files_netsuite) : null
    "--extra-jars"                            = length(local.extra_jars) > 0 ? join(",", local.extra_jars) : null
    "--user-jars-first"                       = var.user_jars_first
    "--use-postgres-driver"                   = var.use_postgres_driver
    "--extra-files"                           = length(var.extra_files) > 0 ? join(",", var.extra_files) : null
    "--job-bookmark-option"                   = var.job_bookmark_option
    "--TempDir"                               = var.temp_dir
    "--enable-s3-parquet-optimized-committer" = var.enable_s3_parquet_optimized_committer
    "--enable-rename-algorithm-v2"            = var.enable_rename_algorithm_v2
    "--enable-glue-datacatalog"               = var.enable_glue_datacatalog ? "" : null
    "--enable-metrics"                        = var.enable_metrics ? "" : null
    "--enable-continuous-cloudwatch-log"      = var.enable_continuous_cloudwatch_log
    "--enable-continuous-log-filter"          = var.enable_continuous_log_filter
    "--continuous-log-logGroup"               = join("", aws_cloudwatch_log_group.log_group.*.name)
    "--continuous-log-logStreamPrefix"        = var.continuous_log_stream_prefix
    "--continuous-log-conversionPattern"      = var.continuous_log_conversion_pattern
    "--aws_secret_manager_region"             = var.region_name
    "--bucket_name"                           = var.s3_bucket_name
    "--table"                                 = each.key
    "--secret_name"                           = var.secret_name_netsuite
    "--database"                              = var.database_netsuite
    "--redshift_glue_connector"               = var.redshift_glue_connector
    "--run_mode"                              = "${each.value.run_mode}"
#    "--start_date"                            = "${each.value.start_date}"
#    "--end_date"                              = "${each.value.end_date}"
    "--s3_raw_bucket_name"                    = "${var.s3_raw_bucket_name}"
    "--env"                                   = "${local.env}"
    "--TempDir"                               = "s3://${var.s3_temp_bucket_name}/${local.env}/netsuite_${each.key}/temp/"
#    "--enable-spark-ui"                       = var.enable_spark_ui
#    "--spark-event-logs-path"                 = var.spark_event_logs_path
    "--additional-python-modules"             = length(var.additional_python_modules) > 0 ? join(",", var.additional_python_modules) : null
#    "--pip-install"                           = "cryptography"
    "--conf"                                  = "spark.driver.maxResultSize=10g --conf spark.driver.memory=20g"
    "--s3-py-modules"                         = length(local.extra_py_files_netsuite) > 0 ? join(",", local.extra_py_files_netsuite) : null
    "--use_auth"                              = "${var.use_auth}"

  }


  execution_property {
    max_concurrent_runs = var.max_concurrent_runs
  }

  dynamic "notification_property" {
    for_each = var.notify_delay_after == null ? [] : [1]

    content {
      notify_delay_after = var.notify_delay_after
    }
  }
}
resource "aws_glue_job" "zoho_glue_job" {

  for_each = var.zoho_crm_jobs

  name                   = "${local.full_name}_zoho_crm_${each.key}"
  role_arn               = var.role_arn
  connections            = var.connections
  description            = "${var.description} - ${each.key}"
  glue_version           = "3.0"
  max_retries            = var.max_retries
  timeout                = var.timeout
  security_configuration = var.create_security_configuration ? join("", aws_glue_security_configuration.sec_cfg.*.id) : var.security_configuration
  #  worker_type            = var.worker_type
  #  number_of_workers      = var.number_of_workers
  tags                   = local.tags
  max_capacity           = var.max_capacity

  command {
    name            = "pythonshell"
    script_location = var.zoho_script_location
    python_version  = 3.9
  }

  default_arguments = {
    "--job-language"                          = var.job_language
    "--class"                                 = var.class
    "--extra-py-files"                        = length(local.extra_py_files_zoho) > 0 ? join(",", local.extra_py_files_zoho) : null
    "--extra-jars"                            = length(var.extra_jars) > 0 ? join(",", var.extra_jars) : null
    "--user-jars-first"                       = var.user_jars_first
    "--use-postgres-driver"                   = var.use_postgres_driver
    "--extra-files"                           = length(var.extra_files) > 0 ? join(",", var.extra_files) : null
    "--job-bookmark-option"                   = var.job_bookmark_option
    "--TempDir"                               = var.temp_dir
    "--enable-s3-parquet-optimized-committer" = var.enable_s3_parquet_optimized_committer
    "--enable-rename-algorithm-v2"            = var.enable_rename_algorithm_v2
    "--enable-glue-datacatalog"               = var.enable_glue_datacatalog ? "" : null
    "--enable-metrics"                        = var.enable_metrics ? "" : null
    "--enable-continuous-cloudwatch-log"      = var.enable_continuous_cloudwatch_log
    "--enable-continuous-log-filter"          = var.enable_continuous_log_filter
    "--continuous-log-logGroup"               = join("", aws_cloudwatch_log_group.log_group.*.name)
    "--continuous-log-logStreamPrefix"        = var.continuous_log_stream_prefix
    "--continuous-log-conversionPattern"      = var.continuous_log_conversion_pattern
    "--aws_secret_manager_region"             = var.region_name
    "--bucket_name"                           = var.s3_bucket_name
    "--table"                                 = "${each.value.table}"
    "--secret_name"                           = var.secret_name_zoho
    "--database"                              = var.database_zoho
    "--redshift_glue_connector"               = var.redshift_glue_connector
    "--s3_raw_bucket_name"                    = "${var.s3_raw_bucket_name}"
    "--env"                                   = "${local.env}"
    #    "--enable-spark-ui"                       = var.enable_spark_ui
    #    "--spark-event-logs-path"                 = var.spark_event_logs_path
    #    "--additional-python-modules"             = length(var.additional_python_modules) > 0 ? join(",", var.additional_python_modules) : null
  }


  execution_property {
    max_concurrent_runs = var.max_concurrent_runs
  }

  dynamic "notification_property" {
    for_each = var.notify_delay_after == null ? [] : [1]

    content {
      notify_delay_after = var.notify_delay_after
    }
  }
}
resource "aws_glue_job" "zoho_campaign_glue_job" {

  for_each = var.zoho_campaign_jobs

  name                   = "${local.full_name}_zoho_campaign_${each.key}"
  role_arn               = var.role_arn
  connections            = var.connections
  description            = "${var.description} - ${each.key}"
  glue_version           = "3.0"
  max_retries            = var.max_retries
  timeout                = var.timeout
  security_configuration = var.create_security_configuration ? join("", aws_glue_security_configuration.sec_cfg.*.id) : var.security_configuration
  #  worker_type            = var.worker_type
  #  number_of_workers      = var.number_of_workers
  tags                   = local.tags
  max_capacity           = var.max_capacity

  command {
    name            = "pythonshell"
    script_location = var.zoho_campaign_script_location
    python_version  = 3.9
  }

  default_arguments = {
    "--job-language"                          = var.job_language
    "--class"                                 = var.class
    "--extra-py-files"                        = length(local.extra_py_files_zoho_campaign) > 0 ? join(",", local.extra_py_files_zoho_campaign) : null
    "--extra-jars"                            = length(var.extra_jars) > 0 ? join(",", var.extra_jars) : null
    "--user-jars-first"                       = var.user_jars_first
    "--use-postgres-driver"                   = var.use_postgres_driver
    "--extra-files"                           = length(var.extra_files) > 0 ? join(",", var.extra_files) : null
    "--job-bookmark-option"                   = var.job_bookmark_option
    "--TempDir"                               = var.temp_dir
    "--enable-s3-parquet-optimized-committer" = var.enable_s3_parquet_optimized_committer
    "--enable-rename-algorithm-v2"            = var.enable_rename_algorithm_v2
    "--enable-glue-datacatalog"               = var.enable_glue_datacatalog ? "" : null
    "--enable-metrics"                        = var.enable_metrics ? "" : null
    "--enable-continuous-cloudwatch-log"      = var.enable_continuous_cloudwatch_log
    "--enable-continuous-log-filter"          = var.enable_continuous_log_filter
    "--continuous-log-logGroup"               = join("", aws_cloudwatch_log_group.log_group.*.name)
    "--continuous-log-logStreamPrefix"        = var.continuous_log_stream_prefix
    "--continuous-log-conversionPattern"      = var.continuous_log_conversion_pattern
    "--aws_secret_manager_region"             = var.region_name
    "--bucket_name"                           = var.s3_bucket_name
    "--table"                                 = each.key
    "--secret_name"                           = var.secret_name_netsuite
    "--database"                              = var.database_zoho_campaign
    "--redshift_glue_connector"               = var.redshift_glue_connector
#    "--run_mode"                              = "${each.value.run_mode}"
#    "--start_date"                            = "${each.value.start_date}"
#    "--end_date"                              = "${each.value.end_date}"
    "--s3_raw_bucket_name"                    = "${var.s3_raw_bucket_name}"
    "--env"                                   = "${local.env}"
    #    "--enable-spark-ui"                       = var.enable_spark_ui
    #    "--spark-event-logs-path"                 = var.spark_event_logs_path
    #    "--additional-python-modules"             = length(var.additional_python_modules) > 0 ? join(",", var.additional_python_modules) : null
  }


  execution_property {
    max_concurrent_runs = var.max_concurrent_runs
  }

  dynamic "notification_property" {
    for_each = var.notify_delay_after == null ? [] : [1]

    content {
      notify_delay_after = var.notify_delay_after
    }
  }
}
resource "aws_glue_job" "dayforce_glue_job" {

  for_each = var.dayforce_jobs

  name                   = "${local.full_name}_dayforce_${each.key}"
  role_arn               = var.role_arn
  connections            = var.connections
  description            = "${var.description} - ${each.key}"
  glue_version           = "3.0"
  max_retries            = var.max_retries
  timeout                = var.timeout
  security_configuration = var.create_security_configuration ? join("", aws_glue_security_configuration.sec_cfg.*.id) : var.security_configuration
  #  worker_type            = var.worker_type
  #  number_of_workers      = var.number_of_workers
  tags                   = local.tags
  max_capacity           = var.max_capacity

  command {
    name            = "pythonshell"
    #script_location = var.dayforce_script_location
    script_location   = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/dayForcePythonGlueJob/${each.value.dayforce_script_name}"
    python_version  = 3.9
  }

  default_arguments = {
    "--job-language"                          = var.job_language
    "--class"                                 = var.class
    "--extra-py-files"                        = length(local.extra_py_files_dayforce) > 0 ? join(",", local.extra_py_files_dayforce) : null
    "--extra-jars"                            = length(var.extra_jars) > 0 ? join(",", var.extra_jars) : null
    "--user-jars-first"                       = var.user_jars_first
    "--use-postgres-driver"                   = var.use_postgres_driver
    "--extra-files"                           = length(var.extra_files) > 0 ? join(",", var.extra_files) : null
    "--job-bookmark-option"                   = var.job_bookmark_option
    "--TempDir"                               = var.temp_dir
    "--enable-s3-parquet-optimized-committer" = var.enable_s3_parquet_optimized_committer
    "--enable-rename-algorithm-v2"            = var.enable_rename_algorithm_v2
    "--enable-glue-datacatalog"               = var.enable_glue_datacatalog ? "" : null
    "--enable-metrics"                        = var.enable_metrics ? "" : null
    "--enable-continuous-cloudwatch-log"      = var.enable_continuous_cloudwatch_log
    "--enable-continuous-log-filter"          = var.enable_continuous_log_filter
    "--continuous-log-logGroup"               = join("", aws_cloudwatch_log_group.log_group.*.name)
    "--continuous-log-logStreamPrefix"        = var.continuous_log_stream_prefix
    "--continuous-log-conversionPattern"      = var.continuous_log_conversion_pattern
    "--aws_secret_manager_region"             = var.region_name
    "--bucket_name"                           = var.s3_bucket_name
    "--table"                                 = "${each.value.table}"
    "--secret_name"                           = var.secret_name_dayforce
    "--database"                              = var.database_dayforce
    "--redshift_glue_connector"               = var.redshift_glue_connector
    "--s3_raw_bucket_name"                    = "${var.s3_raw_bucket_name}"
    "--env"                                   = "${local.env}"
    "--employee_api_url"                      = "${each.value.employee_api_url}"
    "--bulk_export_api_url"                   = "${each.value.bulk_export_api_url}"
    "--token_api_url"                         = "${each.value.token_api_url}"
    "--start_date"                            = "${each.value.start_date}"
    "--end_date"                              = "${each.value.end_date}"
    "--pay_summary_api_url"                   = "${each.value.pay_summary_api_url}"
    "--payee_api_url"                         = "${each.value.payee_api_url}"
    #    "--enable-spark-ui"                       = var.enable_spark_ui
    #    "--spark-event-logs-path"                 = var.spark_event_logs_path
    #    "--additional-python-modules"             = length(var.additional_python_modules) > 0 ? join(",", var.additional_python_modules) : null
  }


  execution_property {
    max_concurrent_runs = var.max_concurrent_runs
  }

  dynamic "notification_property" {
    for_each = var.notify_delay_after == null ? [] : [1]

    content {
      notify_delay_after = var.notify_delay_after
    }
  }
}
resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/aws-glue/jobs/${local.full_name}"
  retention_in_days = var.log_group_retention_in_days
  tags              = var.tags
}

resource "aws_glue_security_configuration" "sec_cfg" {
  count = var.create_security_configuration ? 1 : 0
  name  = "${local.full_name}-sec-config"

  encryption_configuration {
    dynamic "cloudwatch_encryption" {
      for_each = [var.security_configuration_cloudwatch_encryption]

      content {
        cloudwatch_encryption_mode = cloudwatch_encryption.value.cloudwatch_encryption_mode
        kms_key_arn                = cloudwatch_encryption.value.kms_key_arn
      }
    }

    dynamic "job_bookmarks_encryption" {
      for_each = [var.security_configuration_job_bookmarks_encryption]

      content {
        job_bookmarks_encryption_mode = job_bookmarks_encryption.value.job_bookmarks_encryption_mode
        kms_key_arn                   = job_bookmarks_encryption.value.kms_key_arn
      }
    }

    dynamic "s3_encryption" {
      for_each = [var.security_configuration_s3_encryption]

      content {
        s3_encryption_mode = s3_encryption.value.s3_encryption_mode
        kms_key_arn        = s3_encryption.value.kms_key_arn
      }
    }
  }
}