output "lake_formation_id" {
  description = "Amazon Resource Name (ARN) specifying the role."
  value       = aws_lakeformation_permissions.glue_netsuite_db_access.id
}