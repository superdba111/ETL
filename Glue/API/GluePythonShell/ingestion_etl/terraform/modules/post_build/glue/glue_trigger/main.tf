locals {
  full_name = "${var.organization}${var.workspace_branch}"
  tags      = var.tags
}

resource "aws_glue_trigger" "glue_job_trigger_netsuite" {
  for_each = var.netsuite_jobs


  name     = "${var.name}_netsuite_${each.key}_${each.value.run_mode}${var.workspace_branch}"
  schedule = var.type == "SCHEDULED" ? "${each.value.trigger_schedule}" : ""
  type     = "${var.type}"
  tags     = local.tags

  enabled     = "${var.enabled}"
  description = "${var.description} - ${each.key}"

  actions {
    job_name  = "${local.full_name}_netsuite_${each.key}_${each.value.run_mode}"
    arguments = "${var.arguments}"
    timeout   = "${var.timeout}"
  }
}

resource "aws_glue_trigger" "glue_job_trigger_zoho" {
  for_each = var.zoho_crm_jobs

  name        = "${var.name}_zoho_${each.key}"
  schedule    = var.type == "SCHEDULED" ? "${each.value.trigger_schedule}" : ""
  type        = "${var.type}"
  tags        = local.tags
  enabled     = "${var.enabled}"
  description = "${var.description} - ${each.key}"

  actions {
    job_name  = "${local.full_name}_zoho_crm_${each.key}"
    arguments = "${var.arguments}"
    timeout   = "${var.timeout}"
  }
}


resource "aws_glue_trigger" "glue_job_trigger_dayforce" {
  for_each = var.dayforce_jobs

  name        = "${var.name}_dayforce_${each.key}${var.workspace_branch}"
  schedule    = var.type == "SCHEDULED" ? "${each.value.trigger_schedule}" : ""
  type        = "${var.type}"
  tags        = local.tags
  enabled     = "${var.enabled}"
  description = "${var.description} - ${each.key}"

  actions {
    job_name  = "${local.full_name}_dayforce_${each.key}"
    arguments = "${var.arguments}"
    timeout   = "${var.timeout}"
  }
}