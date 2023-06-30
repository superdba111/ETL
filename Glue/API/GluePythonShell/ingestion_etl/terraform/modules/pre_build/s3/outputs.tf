output "ingestion_bucket_id" {
  value = aws_s3_bucket.ingestion_bucket.*.id
}
output "ingestion_bucket_arn" {
  value = aws_s3_bucket.ingestion_bucket.*.arn
}
output "aws_s3_object_file_uploader" {
  value = aws_s3_object.netsuite_python_local_script_upload
}