import uvicorn
from dapr.ext.fastapi import DaprApp
from pydantic import BaseModel

from rest_api.application import app

from rest_api.controller.search import query
from rest_api.schema import QueryRequest

dapr_app = DaprApp(app, router_tags=["health", "search"])

class CloudEventModel(BaseModel):
    data: QueryRequest
    datacontenttype: str
    id: str
    pubsubname: str
    source: str
    specversion: str
    topic: str
    traceid: str
    traceparent: str
    tracestate: str
    type: str


# dapr publish --publish-app-id haystack --topic query --pubsub snssqs-pubsub --data '{"query": "who?"}'
@dapr_app.subscribe(pubsub="snssqs-pubsub", topic="query")
def cloud_event_handler(event_data: CloudEventModel):
    result_status = query(event_data.data)
    print(result_status)
    # TODO: emit message to service xy


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30212)
