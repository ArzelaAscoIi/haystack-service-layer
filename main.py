from typing import Any, Dict, Optional
from fastapi import Form, UploadFile
import uvicorn
from dapr.ext.fastapi import DaprApp
from pydantic import BaseModel

from rest_api.application import app
from rest_api.utils import get_pipelines
from rest_api.controller.search import query
from rest_api.controller.file_upload import upload_file
from rest_api.schema import QueryRequest
from rest_api.pipeline import setup_pipelines

dapr_app = DaprApp(app, router_tags=["health", "search"])


class CloudEventModel(BaseModel):
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


class QueryEvent(BaseModel):
    data: QueryRequest


# dapr publish --publish-app-id haystack --topic query --pubsub snssqs-pubsub --data '{"query": "who?"}'
@dapr_app.subscribe(pubsub="snssqs-pubsub", topic="query")
def cloud_event_handler(event_data: QueryEvent):
    result_status = query(event_data.data)
    print(result_status)
    # TODO: emit message to service xy


class FileUploadContent(BaseModel):
    file_name: str
    text: str
    meta: Optional[Dict[Any,Any]] = None


class UploadEvent(BaseModel):
    data: FileUploadContent


def _convert_text_to_file(file_name: str, text: str) -> UploadFile:
    file = UploadFile(filename=file_name, content_type="plain/text")
    file.file.write(text.encode("utf-8"))
    file.file.seek(0)
    return file


class FileConverterParams(BaseModel):
    pass

class PreprocessorParams(BaseModel):
    pass

# dapr publish --publish-app-id haystack --topic upload --pubsub snssqs-pubsub --data '{"file_name": "example.txt", "text":"This is an example content", "meta":{"key":"value"}}'
@dapr_app.subscribe(pubsub="snssqs-pubsub", topic="upload")
def cloud_event_handler(event_data: UploadEvent):
    setup_pipelines()
    pipelines = get_pipelines()
    print("aaaaadsfdsdfasdfasdfasdf")
    print(pipelines["indexing_pipeline"])

    to_upload_file = _convert_text_to_file(
        file_name=event_data.data.file_name, text=event_data.data.text
    )
    result_status = upload_file(files=[to_upload_file], meta='{}', fileconverter_params=FileConverterParams(), preprocessor_params=PreprocessorParams())

    print(result_status)
    # TODO: emit message to service xy


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30212)
