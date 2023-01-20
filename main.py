from typing import Any
import uvicorn
from dapr.ext.fastapi import DaprApp, DaprActor
from pydantic import BaseModel


from dapr.actor import ActorInterface, actormethod, Actor

from rest_api.application import app

dapr_app = DaprApp(app, router_tags=["health", "search"])


class User(BaseModel):
    id: int
    name = "Jane Doe"


class CloudEventModel(BaseModel):
    data: User
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


class DemoActor(Actor, ActorInterface):
    async def __init__(self):
        self.count = 0

    @actormethod
    async def get_count(self):
        return self.count

    @actormethod
    async def set_count(self, count: int):
        self.count = count

# Add Dapr Actor Extension
actor = DaprActor(app)


@app.on_event("startup")
async def startup_event():
    # Register DemoActor
    await actor.register_actor(DemoActor)
    actor.init_routes(app.router)


@app.get("/GetMyData")
def get_my_data():
    return "{'message': 'myData'}"


# # Handle events sent with CloudEvents
# # dapr publish --publish-app-id sample --topic cloud_topic --pubsub pubsub --data '{"id":"7", "name":"Bob Jones"}'
# @dapr_app.subscribe(pubsub="snssqs-pubsub", topic="health")
# def cloud_event_handler(event_data: CloudEventModel):
#     print(event_data)


# Handle events sent with CloudEvents
# dapr publish --publish-app-id sample --topic cloud_topic --pubsub pubsub --data '{"id":"7", "name":"Bob Jones"}'
@dapr_app.subscribe(pubsub="snssqs-pubsub", topic="health")
def cloud_event_handler(event_data: CloudEventModel):
    print(event_data)


@dapr_app.subscribe(pubsub="snssqs-pubsub", topic="health")
def cloud_event_handler(event_data: CloudEventModel):
    print(event_data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30212)


# app = FastAPI()
# dapr_app = DaprApp(app)

# # Handle events sent with CloudEvents
# # dapr publish --publish-app-id sample --topic cloud_topic --pubsub pubsub --data '{"id":"7", "name":"Bob Jones"}'
# @dapr_app.subscribe(pubsub="snssqs-pubsub", topic="cloud_topic")
# def cloud_event_handler(event_data: CloudEventModel):
#     print(event_data)
