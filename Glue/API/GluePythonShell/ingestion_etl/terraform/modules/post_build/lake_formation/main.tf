resource "aws_lakeformation_permissions" "glue_netsuite_db_access" {
  principal                     = var.role_arn
  permissions                   = ["ALTER", "CREATE_TABLE", "DESCRIBE"]
  permissions_with_grant_option = ["ALTER", "CREATE_TABLE", "DESCRIBE"]
  #  permissions = ["ALL"]

  database {
    name = var.netsuite_glue_db
  }
}

resource "aws_lakeformation_permissions" "glue_zoho_db_access" {
  principal                     = var.role_arn
  permissions                   = ["ALTER", "CREATE_TABLE", "DESCRIBE"]
  permissions_with_grant_option = ["ALTER", "CREATE_TABLE", "DESCRIBE"]
  #  permissions = ["ALL"]

  database {
    name = var.zoho_glue_db
  }
}

resource "aws_lakeformation_permissions" "glue_netsuite_table_access" {
  principal   = var.role_arn
  permissions = ["ALL"]

  table {
    database_name = var.netsuite_glue_db
    wildcard      = true
  }
}

resource "aws_lakeformation_permissions" "glue_zoho_crm_table_access" {
  principal   = var.role_arn
  permissions = ["ALL"]

  table {
    database_name = var.zoho_glue_db
    wildcard      = true
  }
}


resource "aws_lakeformation_permissions" "glue_dayforce_table_access" {
  principal   = var.role_arn
  permissions = ["ALL"]

  table {
    database_name = var.dayforce_glue_db
    wildcard      = true
  }
}



resource "aws_lakeformation_resource" "register_s3" {
  arn = var.s3_location_arn
}


resource "aws_lakeformation_permissions" "glue_s3_access" {
  principal   = var.role_arn
  #  permissions = ["ALTER", "CREATE_TABLE", "DESCRIBE"]
  permissions = ["DATA_LOCATION_ACCESS"]

  data_location {
    arn = var.s3_location_arn
  }
  depends_on = [aws_lakeformation_resource.register_s3]
}


resource "aws_lakeformation_resource" "register_s3_raw_bucket" {
  arn = var.s3_raw_location_arn
}


resource "aws_lakeformation_permissions" "glue_s3_raw_bucket_access" {
  principal   = var.role_arn
  #  permissions = ["ALTER", "CREATE_TABLE", "DESCRIBE"]
  permissions = ["DATA_LOCATION_ACCESS"]

  data_location {
    arn = var.s3_raw_location_arn
  }
  depends_on = [aws_lakeformation_resource.register_s3_raw_bucket]
}

resource "aws_lakeformation_permissions" "glue_dayforce_db_access" {
  principal                     = var.role_arn
  permissions                   = ["ALTER", "CREATE_TABLE", "DESCRIBE"]
  permissions_with_grant_option = ["ALTER", "CREATE_TABLE", "DESCRIBE"]
  #  permissions = ["ALL"]

  database {
    name = var.dayforce_glue_db
  }
}