data "aws_redshift_cluster" "cluster_name" {
  cluster_identifier = var.cluster_name
}
data "aws_secretsmanager_secret" "redshift_creds" {
  name = var.redshift_credentials
}
data "aws_secretsmanager_secret_version" "current" {
  secret_id = data.aws_secretsmanager_secret.redshift_creds.id
}

resource "aws_glue_connection" "redshift_connection" {
  connection_properties = {
    JDBC_CONNECTION_URL = format("%s://%s:%s/%s", "jdbc:redshift", data.aws_redshift_cluster.cluster_name.endpoint, "5439", var.redshift_jdbc_url_name)
    PASSWORD            = jsondecode(data.aws_secretsmanager_secret_version.current.secret_string)["password"]
    USERNAME            = jsondecode(data.aws_secretsmanager_secret_version.current.secret_string)["username"]
  }

  name = var.redshift_glue_connector
  tags = var.tags

  physical_connection_requirements {
    availability_zone      = var.availability_zone
    security_group_id_list = data.aws_redshift_cluster.cluster_name.vpc_security_group_ids
    subnet_id              = var.subnet_id
  }
}
