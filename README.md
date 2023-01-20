# EventHaystack 

EventHaystack is a proof-of-concept project that uses Dapr to invoke haystack pipelines as a service for event-based tasks. The motivation behind this project is to provide a solution for long-running, distributed, and eventually consistent inference tasks that focus on throughput rather than latency.

The architecture of this project involves using Dapr, a portable, event-driven runtime for building distributed applications across cloud and edge, and Haystack, an open-source framework for building production-ready NLP pipelines. The Dapr application runs as a sidecar to the Haystack pipeline, which is invoked through a REST API.

## Motivation 
Long running inference tasks need to be run in a distrubuted manner and should be able to scale up and down based on the load. Additionally, 
these tasks need to be eventually consistent and focus on throughput rather than latency.

This project aims to provide a solution for this problem by using Dapr to invoke haystack pipelines as a service.


## Architecture
[Dapr](https://dapr.io/) is a portable, event-driven, runtime for building distributed applications across cloud and edge. 
[Haystack](https://haystack.deepset.ai/) is an open source framework for building production-ready NLP pipelines.

The dapr application can be run as a sidecar to the haystack pipeline. The haystack pipeline is invoked via a REST API. 
![](/docs/arch.png)


# Start application

```sh
docker-compose build && docker-compose up
```

from within the haystack container we can run the following command to start the haystack pipeline:


```sh
dapr run --app-id haystack --components-path ./components --app-port 30212 -- python3 main.py 
```

We can now invoke the haystack pipeline via the dapr api:

```sh
dapr publish --publish-app-id haystack --topic query --pubsub snssqs-pubsub --data '{"query": "who?"}'
```


# Dapr vs Celery 
To me, dapr feels like a better way to invoke distributed tasks than celery, what we have used before 

Dapr and Celery are both open-source tools that can be used to build distributed systems. However, they serve different purposes and are used in different ways.

### Dapr: 
-  is a portable, event-driven runtime for building microservices
- Provides a set of building blocks for service-to-service invocation, state management, and pub-sub messaging
- Can be used with any programming language
- Can be easily integrated into existing applications
- Dapr is designed to make it easy to build distributed systems
- Building blocks for creating distributed systems such as service-to-service invocation, state management, and pub-sub messaging are provided by Dapr.

### Celery:
- Celery is a task queue for Python
- It is used to run background tasks like sending emails or processing images
- Allows you to send tasks to be executed asynchronously
- Can be used to distribute tasks across multiple worker nodes
- Typically used in conjunction with a message broker like RabbitMQ or Redis
- Message broker handles communication between the workers and the client
- Celery allows for running tasks in the background, handling them asynchronously, and distributing them among multiple worker nodes.

In summary, Dapr is a general-purpose tool for building microservices, while Celery is a Python library for running background tasks. They can be used together, but they serve different purposes.