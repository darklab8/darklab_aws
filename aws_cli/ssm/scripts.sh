export ROLE_ARN=$(aws iam create-role --role-name AWSCookbook106SSMRole --assume-role-policy-document file://assume-role-policy.json --output text --query Role.Arn)

aws iam attach-role-policy --role-name AWSCookbook106SSMRole --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore

aws iam create-instance-profile --instance-profile-name AWSCookbook106InstanceProfile

aws iam add-role-to-instance-profile --role-name AWSCookbook106SSMRole --instance-profile-name AWSCookbook106InstanceProfile

export AMI_ID=$(aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2 --query 'Parameters[0].[Value]' --output text)

export INSTANCE_ID=$(aws ec2 run-instances --image-id $AMI_ID \
--count 1 \
--instance-type t3.nano \
--iam-instance-profile
Name=AWSCookbook106InstanceProfile \
--subnet-id $SUBNET_1 \
--security-group-ids $INSTANCE_SG \
--metadata-options \
HttpTokens=required,HttpPutResponseHopLimit=64,HttpEndpoint=enabled \
--tag-specifications \
'ResourceType=instance,Tags=[{Key=Name,Value=AWSCookbook106}]' \
'ResourceType=volume,Tags=[{Key=Name,Value=AWSCookbook106}]' \
--query Instances[0].InstanceId \
--output text)

export INSTANCE_ID=$(aws ec2 run-instances --image-id $AMI_ID \
--count 1 \
--instance-type t3.nano \
--iam-instance-profile Name=AWSCookbook106InstanceProfile \
--metadata-options \
HttpTokens=required,HttpPutResponseHopLimit=64,HttpEndpoint=enabled \
--tag-specifications \
'ResourceType=instance,Tags=[{Key=Name,Value=AWSCookbook106}]' \
'ResourceType=volume,Tags=[{Key=Name,Value=AWSCookbook106}]' \
--query Instances[0].InstanceId \
--output text)

aws ssm describe-instance-information \
--filters Key=ResourceType,Values=EC2Instance \
--query "InstanceInformationList[].InstanceId" --output text
