# data "terraform_remote_state" "prebuild_state" {
#   backend = "s3" 
#   config = {
#     bucket         = "terraform.shared-services.e.inc"
#     key            = var.terraform_state_path
#     region         = "us-east-1"
#   }
# }