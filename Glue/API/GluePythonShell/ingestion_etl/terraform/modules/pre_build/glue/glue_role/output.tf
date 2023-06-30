output "glue_role_id" {
  description = "Glue role name."
  value       = length(var.role_id) > 0 ? var.role_id : join("", aws_iam_role.glue.*.id)
}

output "glue_role_arn" {
  description = "Amazon Resource Name (ARN) specifying the role."
  value       = length(var.role_arn) > 0 ? var.role_arn : join("", aws_iam_role.glue.*.arn)
}
