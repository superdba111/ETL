resource "aws_glue_catalog_database" "netsuite_glue_catalog_database" {
  name = var.database_netsuite

  #  create_table_default_permission {
  #    permissions = ["SELECT"]
  #
  #    principal {
  #      data_lake_principal_identifier = "IAM_ALLOWED_PRINCIPALS"
  #    }
  #  }
}

resource "aws_glue_catalog_database" "zoho_glue_catalog_database" {
  name = var.database_zoho

}

resource "aws_glue_catalog_database" "dayforce_glue_catalog_database" {
  name = var.database_dayforce

}