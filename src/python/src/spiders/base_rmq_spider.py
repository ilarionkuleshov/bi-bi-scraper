# -*- coding: utf-8 -*-
import json
import traceback

from scrapy.spidermiddlewares.httperror import HttpError

from rmq.pipelines import ItemProducerPipeline
from rmq.spiders import TaskToMultipleResultsSpider
from rmq.utils import get_import_full_name
from rmq.utils.decorators import rmq_errback
from rmq.utils import TaskStatusCodes


class BaseRMQSpider(TaskToMultipleResultsSpider):
    name = "base_rmq"
    custom_settings = {
        "ITEM_PIPELINES": {get_import_full_name(ItemProducerPipeline): 310},
    }

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        base_item_pipelines = BaseRMQSpider.custom_settings.get("ITEM_PIPELINES")
        item_pipelines = settings.getdict("ITEM_PIPELINES")
        item_pipelines.update(base_item_pipelines)
        downloader_middlewares = settings.getdict("DOWNLOADER_MIDDLEWARES")

        if hasattr(cls, 'custom_settings'):
            for custom_setting, value in (cls.custom_settings or {}).items():
                if custom_setting == "DOWNLOADER_MIDDLEWARES":
                    downloader_middlewares = {**downloader_middlewares, **value}
                elif custom_setting == "ITEM_PIPELINES":
                    item_pipelines = {**item_pipelines, **value}
                else:
                    settings.set(custom_setting, value)
        settings.set("DOWNLOADER_MIDDLEWARES", downloader_middlewares)
        settings.set("ITEM_PIPELINES", item_pipelines)

    def _inject_exception_to_task(self, delivery_tag, exception):
        self._inject_status_to_task(delivery_tag, TaskStatusCodes.ERROR.value)
        self.processing_tasks.set_exception(
            delivery_tag,
            json.dumps(
                {
                    "message": str(exception),
                    "traceback": traceback.format_exc(),
                }
            ),
        )
        self.logger.warning(exception)
        self.logger.debug(traceback.format_exc())

    def _inject_status_to_task(self, delivery_tag, status):
        self.processing_tasks.set_status(delivery_tag, status)

    def _inject_soft_exception_to_task(self, delivery_tag, status, message):
        self._inject_status_to_task(delivery_tag, status)
        self.processing_tasks.set_exception(
            delivery_tag, json.dumps({"message": message, "traceback": None})
        )

    @rmq_errback
    def _errback(self, failure):
        delivery_tag = failure.request.meta.get("delivery_tag")
        if failure.check(HttpError):
            response = failure.value.response
            error_message = f"HttpError. URL: {response.url} (status: {response.status})"
        else:
            error_message = "Failed to reach 200 response after retries"

        self._inject_soft_exception_to_task(
            delivery_tag,
            TaskStatusCodes.ERROR.value,
            error_message,
        )
        self.logger.warning(f"IN ERRBACK: {repr(failure)}")
