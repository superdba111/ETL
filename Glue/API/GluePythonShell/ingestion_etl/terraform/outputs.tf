# #output "instance_id" {
# #  description = "ID of the EC2 instance"
# #  value       = aws_instance.app_server.id
# #}
# #
# #output "instance_public_ip" {
# #  description = "Public IP address of the EC2 instance"
# #  value       = aws_instance.app_server.public_ip
# #}

# output "job_name_netsuite" {
#   value = "${module.post_build.module.glue_jobs.netsuite_job_id}"
# }

# output "job_name_zoho" {
#   value = "${module.post_build.module.glue_jobs.zoho_job_id}"
# }

# output "job_arn_netsuite" {
#   value = "${module.post_build.module.glue_jobs.netsuite_job_arn}"
# }

# output "job_arn_zoho" {
#   value = "${module.post_build.module.glue_jobs.zoho_job_arn}"
# }

# output "trigger_name_netsuite" {
#   value = "${module.post_build.module.glue_trigger.netsuite_name}"
# }

# output "trigger_name_zoho" {
#   value = "${module.post_build.module.glue_trigger.zoho_name}"
# }

# output "trigger_schedule_netsuite" {
#   value = "${module.post_build.module.glue_trigger.netsuite_schedule}"
# }

# output "trigger_schedule_zoho" {
#   value = "${module.post_build.module.glue_trigger.zoho_schedule}"
# }

# output "glue_job_netsuite_props_tbl" {
#   value = var.netsuite_tables
# }

# output "netsuite_database" {
#   value = "${module.pre_build.module.glue_database}"
# }