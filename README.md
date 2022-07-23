Repository to learn all kind of AWS stuff.

# Achieved things

- EC2 instance exposed for SSH login and having published busybox for inboud traffic

# Notes to try

- [X] [Find a book about AWS or roadmap](https://www.amazon.com/AWS-Cookbook-Recipes-Success/dp/1492092606)
- [X] Also, figure out session manager, then never expose SSH to the internet again
- [X] Deploying containers with Amazon Lightsail
- [X] S3!
- [X] What is IAM?
- [X] [Billing](https://calculator.aws/#/addService) + Costs for traffic at least
- [ ] Security
- [ ] VPC + Subnets
- [ ] Working with RDS
- [ ] Working with Lambdas
- [ ] Working with Step Functions - Pipeline of Lambdas? +optionally other services 🤔
- [ ] What is Amazon Fargate
- [ ] Working with ECS
- [ ] Working with EKS
- [ ] Working with SQS? 🤔 (+SNS?)
- [ ] Auto scaling group ?
- [ ] Cloudwatch with cron job for automatic stop/enables?
- [ ] Load balancer?
- [ ] Route 53?
- [ ] Secret Manager
- [ ] Options Manager?
- [ ] AWS Cloud Trail - a tool for architect to debug infra

# Tips:

- If you comment out the calls to the module, then it will just create VPC, subnets and an ECW instance running a postgres container
  https://github.com/dwp/terraform-aws-kong-gateway/blob/main/examples/hybrid_amazon_linux/hybrid_amazon_linux.png
- OIDC? https://auth0.com/docs/authenticate/protocols/openid-connect-protocol
