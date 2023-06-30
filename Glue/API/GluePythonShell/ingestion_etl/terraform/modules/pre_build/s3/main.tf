resource "aws_s3_bucket" "ingestion_bucket" {
  count  = var.s3_create ? 1 : 0
  bucket = var.s3_bucket_name

  tags          = var.tags
  force_destroy = false
}

resource "aws_s3_bucket_acl" "ingestion_bucket_acl" {
  count  = var.s3_create ? 1 : 0
  bucket = aws_s3_bucket.ingestion_bucket[count.index].id
  acl    = "private"

}

resource "aws_s3_bucket_public_access_block" "public_block" {
  count  = var.s3_create ? 1 : 0
  bucket = aws_s3_bucket.ingestion_bucket[count.index].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


locals {
  from_netsuite_python_local_script_location = "../gluePython/netSuitePythonGlueJob/netSuitePythonGlueJob.py"
  to_netsuite_python_s3_script_location      = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/netSuitePythonGlueJob/netSuitePythonGlueJob.py"

  from_zoho_python_local_script_location = "../gluePython/zohoPythonGlueJob/zohoCrmPythonGlueJob.py"
  to_zoho_python_s3_script_location      = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/zohoPythonGlueJob/zohoCrmPythonGlueJob.py"

  from_zoho_campaign_python_local_script_location = "../gluePython/zohoPythonGlueJob/zohoCampaignPythonGlueJob.py"
  to_zoho_campaign_python_s3_script_location      = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/zohoPythonGlueJob/zohoCampaignPythonGlueJob.py"

  from_common_lib_s3_path = "../common_api_lib/dist/commonPythonGlueLib-1.0.0-py3-none-any.whl"
  to_common_lib_s3_path   = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/commonPythonGlueLib-1.0.0-py3-none-any.whl"

  from_extra_jar_path = "../gluePython/netsuiteModuleLib/NQjc.jar"
  to_extra_jar_path   = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/NQjc.jar"

  from_zoho_lib_s3_path = "../gluePython/zohoModuleLib/glue_python_shell_og_zcrm-0.1-py3-none-any.whl"
  to_zoho_lib_s3_path   = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/glue_python_shell_og_zcrm-0.1-py3-none-any.whl"

  from_day_force_properties_python_local_script_location = "../gluePython/dayForcePythonGlueJob/dayForcePythonEmployeePropertiesGlueJob.py"
  to_day_force_properties_python_s3_script_location      = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/dayForceGlueJob/dayForcePythonEmployeePropertiesGlueJob.py"

  from_day_force_status_python_local_script_location = "../gluePython/dayForcePythonGlueJob/dayForcePythonEmployeeStatusGlueJob.py"
  to_day_force_status_python_s3_script_location      = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/dayForceGlueJob/dayForcePythonEmployeeStatusGlueJob.py"

  from_day_force_payroll_summary_python_local_script_location = "../gluePython/dayForcePythonGlueJob/dayForcePythonEmployeePayrollSummaryGlueJob.py"
  to_day_force_payroll_summary_python_s3_script_location      = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/dayForceGlueJob/dayForcePythonEmployeePayrollSummaryGlueJob.py"

  from_day_force_payee_python_local_script_location = "../gluePython/dayForcePythonGlueJob/dayForcePythonPayeeGlueJob.py"
  to_day_force_payee_python_s3_script_location      = "s3://${var.s3_bucket_name}/glue-python/glue_source_codes/dayForceGlueJob/dayForcePythonPayeeGlueJob.py"



}

resource "aws_s3_object" "netsuite_python_local_script_upload" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/netSuitePythonGlueJob/netSuitePythonGlueJob.py"
  source     = local.from_netsuite_python_local_script_location
  etag       = filemd5(local.from_netsuite_python_local_script_location)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}

resource "aws_s3_object" "common_python_glue_lib" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/commonPythonGlueLib-1.0.0-py3-none-any.whl"
  source     = local.from_common_lib_s3_path
  etag       = filemd5(local.from_common_lib_s3_path)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}

resource "aws_s3_object" "zoho_python_local_script_upload" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/zohoPythonGlueJob/zohoCrmPythonGlueJob.py"
  source     = local.from_zoho_python_local_script_location
  etag       = filemd5(local.from_zoho_python_local_script_location)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}

resource "aws_s3_object" "zoho_campaign_python_local_script_upload" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/zohoPythonGlueJob/zohoCampaignPythonGlueJob.py"
  source     = local.from_zoho_campaign_python_local_script_location
  etag       = filemd5(local.from_zoho_campaign_python_local_script_location)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}


resource "aws_s3_object" "dayForce_properties_python_local_script_upload" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/dayForcePythonGlueJob/dayForcePythonEmployeePropertiesGlueJob.py"
  source     = local.from_day_force_properties_python_local_script_location
  etag       = filemd5(local.from_day_force_properties_python_local_script_location)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}

resource "aws_s3_object" "zoho_python_glue_lib" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/glue_python_shell_og_zcrm-0.1-py3-none-any.whl"
  source     = local.from_zoho_lib_s3_path
  etag       = filemd5(local.from_zoho_lib_s3_path)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}

resource "aws_s3_object" "extra_jars" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/NQjc.jar"
  source     = local.from_extra_jar_path
  etag       = filemd5(local.from_extra_jar_path)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}

#resource "aws_s3_object" "file_loader" {
#
#  for_each = fileset("../../gluePython/", "**")
#  bucket = var.s3_bucket_name
#  key = each.value
#  source = "./../gluePython/${each.value}"
#  etag = filemd5("./../gluePython/${each.value}")
#
#  depends_on = [aws_s3_bucket.ingestion_bucket]
#
#}
resource "aws_s3_object" "dayForce_status_python_local_script_upload" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/dayForcePythonGlueJob/dayForcePythonEmployeeStatusGlueJob.py"
  source     = local.from_day_force_status_python_local_script_location
  etag       = filemd5(local.from_day_force_status_python_local_script_location)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}
resource "aws_s3_object" "dayForce_payroll_summary_python_local_script_upload" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/dayForcePythonGlueJob/dayForcePythonEmployeePayrollSummaryGlueJob.py"
  source     = local.from_day_force_payroll_summary_python_local_script_location
  etag       = filemd5(local.from_day_force_payroll_summary_python_local_script_location)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}
resource "aws_s3_object" "dayForce_payee_python_local_script_upload" {
  bucket     = var.s3_bucket_name
  key        = "glue-python/glue_source_codes/dayForcePythonGlueJob/dayForcePythonPayeeGlueJob.py"
  source     = local.from_day_force_payee_python_local_script_location
  etag       = filemd5(local.from_day_force_payee_python_local_script_location)
  tags       = var.tags
  depends_on = [aws_s3_bucket.ingestion_bucket]
}