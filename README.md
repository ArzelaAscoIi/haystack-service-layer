# EventHaystack 

Event based service invocation of haystack pipelines with Dapr. This project is a proof of concept and not intended for production use.

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
dapr publish --publish-app-id haystack --topic index --pubsub snssqs-pubsub --data  "{}"
```

'{"id":"7", "name":"Bob Jones"}'