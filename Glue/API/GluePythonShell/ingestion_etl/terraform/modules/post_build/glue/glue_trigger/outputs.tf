#output "netsuite_name" {
#  value = "${join(",", aws_glue_trigger.glue_job_trigger_netsuite.*.name)}"
#}
#
#output "netsuite_type" {
#  value = "${join(",", aws_glue_trigger.glue_job_trigger_netsuite.*.type)}"
#}
#
#output "netsuite_schedule" {
#  value = "${join(",", aws_glue_trigger.glue_job_trigger_netsuite.*.schedule)}"
#}
#
#output "netsuite_actions" {
#  value = "${aws_glue_trigger.glue_job_trigger_netsuite.*.actions}"
#}

#output "zoho_name" {
#  value = "${join(",", aws_glue_trigger.glue_job_trigger_zoho.*.name)}"
#}
#
#output "zoho_type" {
#  value = "${join(",", aws_glue_trigger.glue_job_trigger_zoho.*.type)}"
#}
#
#output "zoho_schedule" {
#  value = "${join(",", aws_glue_trigger.glue_job_trigger_zoho.*.schedule)}"
#}
#
#output "zoho_actions" {
#  value = "${aws_glue_trigger.glue_job_trigger_zoho.*.actions}"
#}