output "einc_redshift_connection_id" {
  value = aws_glue_connection.redshift_connection.id
}
output "einc_redshift_connection_arn" {
  value = aws_glue_connection.redshift_connection.arn
}
output "einc_redshift_connection_tags" {
  value = aws_glue_connection.redshift_connection.tags_all
}
