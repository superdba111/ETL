// Environment variables
terraform_environment_name     = "prod"
terraform_environment_region   = "us-east-1"
terraform_environment_iam_role = "arn:aws:iam::605516946663:role/Terraform"

organization = "einc"

netsuite_jobs = {
  "currency" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "customer" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "department" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "employee" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "subsidiary" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "vendor" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "transaction" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2018-08-01",
    end_date         = "2020-01-01"
  },
  "transactionline" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2018-08-01",
    end_date         = "2020-01-01"
  },
  "entity" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "item" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "currencyrate" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "customsegment" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "location" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "salesinvoiced" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
#  "invoice_data" = {
#    run_mode         = "fl",
#    trigger_schedule = "cron(0 10 * * ? *)",
#    start_date       = "2018-08-01",
#    end_date         = "2023-01-09"
#  },
  "accounttype" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "account" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "classification" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "customrecord_csegcseg_eb_bu" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2023-01-09"
  },
  "customrecord_vehicle_selection" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2022-01-01",
    end_date         = "2022-12-05"
  },
  "transaction_delta" = {
    run_mode         = "dl",
    trigger_schedule = "cron(0 10-22 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2020-01-01"
  },
  "transactionline_delta" = {
    run_mode         = "dl",
    trigger_schedule = "cron(0 10-22/3 * * ? *)",
    start_date       = "2018-08-01",
    end_date         = "2020-01-01"
  },
  "accountingperiod" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2022-09-01",
    end_date         = "2023-01-12"
  },
  "transactionaccountingline" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2022-09-01",
    end_date         = "2023-01-12"
  },
  "term" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2022-09-01",
    end_date         = "2023-01-12"
  },
  "consolidatedExchangeRate" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 * * ? *)",
    start_date       = "2022-09-01",
    end_date         = "2023-01-12"
  }
}
#processed.datalake.reporting-dev.e.inc

zoho_crm_jobs = {
  "glue_jobs" = {
    table = "Accounts,Contacts,zrouteiqzcrm__Routes,Dealer_Discount_Requests,fusion__SMS_Messages,Territory_Assigments,Dealer_Applications,Leads,Subform_1",
    trigger_schedule = "cron(0 10 ? * MON *)"
  }
}

dayforce_jobs = {
  "employee_properties" = {
    table = "employee_properties",
    trigger_schedule = "cron(0 10 * * ? *)"
    employee_api_url = "https://can63-services.dayforcehcm.com/Api/einc/V1/Employees"
    bulk_export_api_url = "https://can63-services.dayforcehcm.com/Api/einc/V1/EmployeeExportJobs"
    token_api_url = "https://dfid.dayforcehcm.com/connect/token"
    dayforce_script_name = "dayForcePythonEmployeePropertiesGlueJob.py"
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    pay_summary_api_url = "https://can63-services.dayforcehcm.com/Api/einc/V1/EmployeePaySummaries"
  },
  "employee_status" = {
    table = "employee_status",
    trigger_schedule = "cron(0 10 * * ? *)"
    employee_api_url = "https://can63-services.dayforcehcm.com/Api/einc/V1/Employees"
    bulk_export_api_url = "https://can63-services.dayforcehcm.com/Api/einc/V1/EmployeeExportJobs"
    token_api_url = "https://dfid.dayforcehcm.com/connect/token"
    dayforce_script_name = "dayForcePythonEmployeeStatusGlueJob.py"
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    pay_summary_api_url = "https://can63-services.dayforcehcm.com/Api/einc/V1/EmployeePaySummaries"
  },
  "employee_payroll_summary" = {
    table = "employee_payroll_summary",
    trigger_schedule = "cron(0 10 * * ? *)"
    employee_api_url = "https://can63-services.dayforcehcm.com/Api/einc/V1/Employees"
    bulk_export_api_url = "https://can63-services.dayforcehcm.com/Api/einc/V1/EmployeeExportJobs"
    token_api_url = "https://dfid.dayforcehcm.com/connect/token"
    dayforce_script_name = "dayForcePythonEmployeePayrollSummaryGlueJob.py"
    start_date = "start_date"
    end_date = "end_date"
    pay_summary_api_url = "https://can63-services.dayforcehcm.com/Api/einc/V1/EmployeePaySummaries"
  }
}

database_dayforce = "dayforce_data_ingestion"

s3_create            = false
s3_raw_bucket_name   = "landing.datalake.reporting.e.inc"
s3_bucket_name       = "processed.datalake.reporting.e.inc"
s3_temp_bucket_name  =  "ingestion-etl-prod-temp"
database_netsuite    = "einc-processed-netsuite"
secret_name_netsuite = "netsuite/user/pass/secrets"

create_job   = true
create_role  = true
job_name     = ""
job_role_arn = ""

job_dpu        = 2
job_language   = "python"
job_bookmark   = "disabled"
job_temp_dir   = ""
job_arguments  = {}
create_trigger = true

trigger_name = "glue_trigger"

secret_name_zoho      = "zoho/user/pass/secrets"
database_zoho         = "einc-processed-netsuite"
zoho_trigger_schedule = ["cron(0 10 * * ? *)"]
trigger_job           = "glue_trigger_job"
trigger_type          = "SCHEDULED"
trigger_enabled       = true
trigger_description   = ""
trigger_arguments     = {}
trigger_timeout       = 2880
emails                = ["einc_sns-aaaaidzc5nk2f6v7ki3773acda@opsguru.slack.com", "data-ingestion-alerts-aaaaitsikwzpnjogrepedxnwuy@eblock.slack.com"]
kms_role_arn          = "arn:aws:kms:us-east-1:605516946663:key/e6b6355c-9695-4d33-bd6e-b11e0952162d"

zoho_campaign_jobs = {
  "table_name" = {
    key = "val"
  }
}

database_zoho_campaign = "zoho_campaign_data_ingestion"

// redshift connection vars
redshift_glue_connector = "redshift_glue_connector_prod"
job_connections         = ["redshift_glue_connector_prod"]
cluster_name            = "datalake"
redshift_jdbc_url_name  = "data_warehouse"
redshift_credentials    = "prod/redshift/datalake"
availability_zone       = "us-east-1c"
subnet_id               = "subnet-0db5d4958bb7ddf2a"
tags                    = { map-migrated = "d-server-02mpp1acry7wg4" }
