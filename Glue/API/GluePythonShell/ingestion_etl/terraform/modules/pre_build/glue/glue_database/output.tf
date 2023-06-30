output "netsuite_glue_db" {
  value = "${aws_glue_catalog_database.netsuite_glue_catalog_database.id}"
}
output "zoho_glue_db" {
  value = "${aws_glue_catalog_database.zoho_glue_catalog_database.id}"
}