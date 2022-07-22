Repository to learn all kind of AWS stuff.

# Achieved things

- EC2 instance exposed for SSH login and having published busybox for inboud traffic

# Notes to try

- [X] Also, figure out session manager, then never expose SSH to the internet again
- [x] Deploying containers with Amazon Lightsail
- [X] S3!
- [X] What is IAM?
- [ ] Working with RDS
- [ ] Working with Lambdas
- [ ] What is Amazon Fargate
- [ ] Working with ECS
- [ ] Working with EKS
- [ ] Working with SQS? 🤔
- [ ] Auto scaling group ?
- [ ] Cloudwatch with cron job for automatic stop/enables?
- [ ] Find a book about AWS or roadmap
- [ ] Load balancer?
- [ ] Route 53?

# Tips:

- If you comment out the calls to the module, then it will just create VPC, subnets and an ECW instance running a postgres container
  https://github.com/dwp/terraform-aws-kong-gateway/blob/main/examples/hybrid_amazon_linux/hybrid_amazon_linux.png
