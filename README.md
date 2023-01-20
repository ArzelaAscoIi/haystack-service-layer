# Event base service layer for haystack pipeline invocation




# Start application

```sh
dapr run --app-id haystack --components-path ./components --app-port 30212 -- python3 main.py 
```

### Setup SQS
Run localstack to provision AWS services. This will enable dapr to to connect and invoke services via AWS SQS and SNS.
```sh
docker run --rm -it -p 4566:4566 -p 4571:4571 -e SERVICES="sts,sns,sqs" -e AWS_DEFAULT_REGION="us-east-1" localstack/localstack
```

After starting localstack and the dapr app you should see the following output in the terminal:

```bash
2023-01-20T10:03:24.364  INFO --- [   asgi_gw_4] localstack.request.aws     : AWS sqs.ReceiveMessage => 200
2023-01-20T10:03:26.405  INFO --- [   asgi_gw_0] localstack.request.aws     : AWS sqs.ReceiveMessage => 200
2023-01-20T10:03:28.434  INFO --- [   asgi_gw_1] localstack.request.aws     : AWS sqs.ReceiveMessage => 200
```
