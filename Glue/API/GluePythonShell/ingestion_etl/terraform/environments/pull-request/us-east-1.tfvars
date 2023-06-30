// Environment variables
terraform_environment_name     = "reporting-pr"
terraform_environment_region   = "us-east-1"
terraform_environment_iam_role = "arn:aws:iam::292923181097:role/Terraform"

organization = "einc"


netsuite_jobs = {
  "currency" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "customer" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "department" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "employee" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "subsidiary" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "vendor" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "transaction" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "transactionline" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "entity" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "item" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "currencyrate" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "customsegment" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "location" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "salesinvoiced" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
#  "invoice_data" = {
#    run_mode         = "fl",
#    trigger_schedule = "cron(0 10 30 1 ? 2023)",
#    start_date       = "2022-03-02",
#    end_date         = "2022-12-31"
#  },
  "accounttype" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "account" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "classification" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "customrecord_csegcseg_eb_bu" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "customrecord_vehicle_selection" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-01-01",
    end_date         = "2022-12-05"
  },
  "transaction_delta" = {
    run_mode         = "dl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "transactionline_delta" = {
    run_mode         = "dl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
    start_date       = "2022-03-02",
    end_date         = "2022-12-31"
  },
  "accountingperiod" = {
    run_mode         = "fl",
    trigger_schedule = "cron(0 10 30 1 ? 2023)",
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
    employee_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/Employees"
    bulk_export_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/EmployeeExportJobs"
    token_api_url = "https://dfidtst.np.dayforcehcm.com/connect/token"
    dayforce_script_name = "dayForcePythonEmployeePayrollSummaryGlueJob.py"
    start_date = "YYYY-MM-DD"
    end_date = "YYYY-MM-DD"
    pay_summary_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/EmployeePaySummaries"
    payee_api_url = "https://test.dayforcehcm.com/Api/einc/V1/Payee"
  },
  "employee_status" = {
    table = "employee_status",
    trigger_schedule = "cron(0 10 * * ? *)"
    employee_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/Employees"
    bulk_export_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/EmployeeExportJobs"
    token_api_url = "https://dfidtst.np.dayforcehcm.com/connect/token"
    dayforce_script_name = "dayForcePythonEmployeePayrollSummaryGlueJob.py"
    start_date = "YYYY-MM-DD"
    end_date = "YYYY-MM-DD"
    pay_summary_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/EmployeePaySummaries"
    payee_api_url = "https://test.dayforcehcm.com/Api/einc/V1/Payee"
  },
  "employee_payroll_summary" = {
    table = "employee_payroll_summary",
    trigger_schedule = "cron(0 10 * * ? *)"
    employee_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/Employees"
    bulk_export_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/EmployeeExportJobs"
    token_api_url = "https://dfidtst.np.dayforcehcm.com/connect/token"
    dayforce_script_name = "dayForcePythonEmployeePayrollSummaryGlueJob.py"
    start_date = "start_date"
    end_date = "end_date"
    pay_summary_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/EmployeePaySummaries"
    payee_api_url = "https://test.dayforcehcm.com/Api/einc/V1/Payee"
  },
  "payee" = {
    table = "payee",
    trigger_schedule = "cron(0 10 ? * MON *)"
    employee_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/Employees"
    bulk_export_api_url = "https://cantest63-services.dayforcehcm.com/Api/einc/V1/EmployeeExportJobs"
    token_api_url = "https://dfidtst.np.dayforcehcm.com/connect/token"
    dayforce_script_name = "dayForcePythonEmployeePayrollSummaryGlueJob.py"
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    pay_summary_api_url = "https://test.dayforcehcm.com/Api/einc/V1/EmployeePaySummaries"
    payee_api_url = "https://test.dayforcehcm.com/Api/einc/V1/Payee"
  }
}

database_dayforce = "dayforce_data_ingestion"

s3_create            = false
s3_raw_bucket_name   = "landing.datalake.reporting-dev.e.inc"
s3_bucket_name       = "processed.datalake.reporting-dev.e.inc"
s3_temp_bucket_name  =  "ingestion-etl-pr-temp"
database_netsuite    = "netsuite_data_ingestion"
secret_name_netsuite = "netsuite/user/pass/secrets"
run_mode             = "fl"
create_job           = true
create_role          = true
job_name             = ""
job_role_arn         = ""
job_dpu              = 2
job_language         = "python"
job_bookmark         = "disabled"
job_temp_dir         = ""
job_arguments        = {}
create_trigger       = true

trigger_name = "glue_trigger"

secret_name_zoho      = "zoho/user/pass/secrets"
database_zoho         = "zoho_data_ingestion"
zoho_trigger_schedule = ["cron(0 10 30 1 ? 2023)"]
trigger_job           = "glue_trigger_job"
trigger_type          = "SCHEDULED"
trigger_enabled       = true
trigger_description   = ""
trigger_arguments     = {}
trigger_timeout       = 2880
emails                = ["einc_sns-aaaaidzc5nk2f6v7ki3773acda@opsguru.slack.com"]
kms_role_arn          = "arn:aws:kms:us-east-1:605516946663:key/e6b6355c-9695-4d33-bd6e-b11e0952162d"

zoho_campaign_jobs = {
  "table_name" = {
    key = "val"
  }
}
database_zoho_campaign = "zoho_campaign_data_ingestion"

// redshift connection vars
redshift_glue_connector = "redshift_glue_connector_reporting_pr"
job_connections         = ["redshift_glue_connector_reporting_pr"]
cluster_name            = "datalake"
redshift_jdbc_url_name  = "datalake"
redshift_credentials    = "datalake/redshift"
availability_zone       = "us-east-1d"
subnet_id               = "subnet-0f6caf2a7b22db636"
tags                    = { map-migrated = "d-server-02mpp1acry7wg4" }
