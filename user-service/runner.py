"""A simple class that can be used to publish events to a designated sink"""

from python_outbox.sqlalchemy_outbox.sqlalchemy_storage_box import (
    SQLAlchemyPydanticStorageBox,
)
from python_outbox.sqlalchemy_outbox.sqlalchemy_producer import (
    SQLAlchemyStorageBoxProducer,
    SQLAlchemyStorageBoxSource,
)
from python_outbox.base.mapper import AbstractMapper
from python_outbox.generic.runner import SimpleRunner
from python_outbox.generic.publisher import CloudEventHTTPPublisher
from app.dependencies import get_db
from os import environ as env
from cloudevents.pydantic import CloudEvent

HTTP_CLOUD_EVENT_SINK = env.get("HTTP_CLOUD_EVENT_SINK")

if HTTP_CLOUD_EVENT_SINK is None:
    raise "You must use this runner with HTTP_CLOUD_EVENT_SINK set to the sink."


class SABoxPydanticToCEMapper(AbstractMapper[SQLAlchemyPydanticStorageBox, CloudEvent]):
    def convert(self, source: SQLAlchemyPydanticStorageBox) -> CloudEvent:
        value = source.payload.dict()
        if "source" not in value or "type" not in value:
            raise ValueError(
                "Cannot map this object because it has not declared source and type value, which is required for a CE event"
            )
        ce_source = value["source"]
        ce_type = value["type"]
        ce_data = value
        ce_data.pop("type")
        ce_data.pop("source")
        return CloudEvent(source=ce_source, type=ce_type, data=ce_data)


session = next(get_db())

source = SQLAlchemyStorageBoxSource(
    orm_class=SQLAlchemyPydanticStorageBox, session=session
)
mapper = SABoxPydanticToCEMapper()
publisher = CloudEventHTTPPublisher(HTTP_CLOUD_EVENT_SINK)
producer = SQLAlchemyStorageBoxProducer(
    mapper=mapper, publisher=publisher, source=source
)

runner = SimpleRunner(producer=producer)

runner.start()
