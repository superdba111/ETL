output "glue_role_arn" {
  value = "${module.glue_role.glue_role_arn}"
}

output "ingestion_bucket_arn" {
  value = "${module.s3_utils.ingestion_bucket_arn}"
}

output "container_build" {
  value = "${var.container_build}"
}