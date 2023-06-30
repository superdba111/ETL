### Generic Terraform Commands

#### 1. Terraform init.

`terraform init`

#### 2. Format files

`terraform fmt`

#### 3. Validate Results

`terraform validate`

#### 4. Deployment

`terraform apply`

#### 5. Inspect State

`terraform show`

#### 6. Managing state list

`terraform state list`

#### Troubleshooting

If terraform validate was successful and your apply still failed, you may be encountering one of these common errors.

* If you use a region other than us-west-2, you will also need to change your ami, since AMI IDs are region-specific.
  Choose an AMI ID specific to your region by following these instructions, and modify main.tf with this ID.
  Then re-run terraform apply.

* If you do not have a default VPC in your AWS account in the correct region, navigate to the AWS VPC Dashboard in the
  web UI,
  create a new VPC in your region, and associate a subnet and security group to that VPC. Then add the security group
  ID (vpc_security_group_ids)
  and subnet ID (subnet_id) arguments to your aws_instance resource, and replace the values with the ones from your new
  security group and subnet.

```
 resource "aws_instance" "app_server" {
   ami                    = "ami-830c94e3"
   instance_type          = "t2.micro"
+  vpc_security_group_ids = ["sg-0077..."]
+  subnet_id              = "subnet-923a..."
 }
```

#### Destroying including policy(issue)

Run `terraform plan`. You should see that there are no changes to be applied. This is to ensure that the selected
resources have been safely removed from your terraform state files and terraform code.
Run `terraform destroy`. This should destroy all other resources.

Save the changes to main.tf, and re-run terraform apply.

#### Rename a variable

`terraform apply -var "instance_name=YetAnotherName"`

### dev Run

1. Terraform Init

```shell
terraform init -input=false -upgrade=true \
-backend-config="key=dev/us-east-1/dev/dev.tfstate" \
-backend-config="bucket=terraform.reporting-development.e.inc" \
-backend-config="role_arn=arn:aws:iam::292923181097:role/Terraform" \
-var-file "environments/dev/us-east-1.tfvars" \
-var "terraform_environment_region=us-east-1" \
-var "terraform_repository_name=reporting" \
-var "terraform_repository_ref_name=dev"
```

Note that key can be custom name as such, `"key=reporting/us-east-1/development/dev_fuat_etl.tfstate"`

2. Terrafrom Plan and Apply for **Pre-Build** Module

```shell
terraform plan -no-color -input=false -out=terraform.plan -target module.pre_build \
-var-file "environments/dev/us-east-1.tfvars" \
-var "terraform_environment_region=us-east-1" \
-var "terraform_repository_name=reporting" \
-var "terraform_repository_ref_name=dev"
```

#\
#-var "terraform_workspace_name=dev"


```shell
terraform show \
-no-color \
terraform.plan
```

```shell
terraform apply \
-no-color \
-input=false \
-auto-approve \
terraform.plan
```

3. Terrafrom Plan and Apply for **Post-Build** Module

```shell
terraform plan -no-color -input=false -out=terraform_post_build.plan -target module.post_build \
-var-file "environments/dev/us-east-1.tfvars" \
-var "terraform_environment_region=us-east-1" \
-var "terraform_repository_name=reporting" \
-var "terraform_repository_ref_name=dev"
```

```shell
terraform show \
-no-color \
terraform_post_build.plan
```

```shell
terraform apply \
-no-color \
-input=false \
-auto-approve \
terraform_post_build.plan
```

4. Terraform Destroy

```shell
terraform  destroy \
-var-file "environments/dev/us-east-1.tfvars" \
-var "terraform_environment_region=us-east-1" \
-var "terraform_repository_name=reporting" \
-var "terraform_repository_ref_name=dev"
```

```shell
terraform  destroy \
-var-file "environments/dev/us-east-1.tfvars" \
-var "terraform_environment_region=us-east-1" \
-var "terraform_repository_name=reporting" \
-var "terraform_repository_ref_name=dev" \
-var "terraform_workspace_name=dev"
```

5. Terraform Output(Optional)

```shell
terraform output -no-color -json
```


### ------------------------------------------------------------------------
### PROD Run

1. Terraform Init

```shell
terraform init -input=false -upgrade=true \
-backend-config="key=prod/us-east-1/prod/prod.tfstate" \
-backend-config="bucket=terraform.reporting.e.inc" \
-backend-config="role_arn=arn:aws:iam::605516946663:role/Terraform" \
-var-file "environments/production/us-east-1.tfvars" \
-var "terraform_environment_region=us-east-1" \
-var "terraform_repository_name=reporting" \
-var "terraform_repository_ref_name=prod"
```
#aws sts get-caller-identity
Note that key can be custom name as such, `"key=reporting/us-east-1/development/dev_fuat_etl.tfstate"`

2. Terrafrom Plan and Apply for **Pre-Build** Module

```shell
terraform plan -no-color -input=false -out=terraform.plan -target module.pre_build \
-var-file "environments/production/us-east-1.tfvars" \
-var "terraform_environment_region=us-east-1" \
-var "terraform_repository_name=reporting" \
-var "terraform_repository_ref_name=prod"
```

```shell
terraform show \
-no-color \
terraform.plan
```

```shell
terraform apply \
-no-color \
-input=false \
-auto-approve \
terraform.plan
```

3. Terrafrom Plan and Apply for **Post-Build** Module

```shell
terraform plan -no-color -input=false -out=terraform_post_build.plan -target module.post_build \
-var-file "environments/production/us-east-1.tfvars" \
-var "terraform_environment_region=us-east-1" \
-var "terraform_repository_name=reporting" \
-var "terraform_repository_ref_name=prod"
```

```shell
terraform show \
-no-color \
terraform_post_build.plan
```

```shell
terraform apply \
-no-color \
-input=false \
-auto-approve \
terraform_post_build.plan
```

4. Terraform Destroy

```shell
terraform  destroy \
-var-file "environments/production/us-east-1.tfvars" \
-var "terraform_environment_region=us-east-1" \
-var "terraform_repository_name=reporting" \
-var "terraform_repository_ref_name=prod"
```
ZohoCRM.settings.ALL,ZohoCRM.modules.ALL,ZohoCRM.settings.ALL,ZohoCRM.users.ALL,ZohoCRM.org.ALL,ZohoCRM.settings.ALL,ZohoCRM.modules.Accounts.READ,ZohoCRM.modules.Leads.READ,ZohoCRM.modules.custom.ALL,ZohoCRM.notifications.ALL,ZohoCRM.modules.activities.ALL,ZohoCRM.modules.calls.ALL,ZohoCRM.modules.accounts.ALL,ZohoCRM.coql.READ

