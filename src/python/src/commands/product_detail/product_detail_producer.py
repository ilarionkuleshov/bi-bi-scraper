# -*- coding: utf-8 -*-
from sqlalchemy import select, update
from scrapy.utils.project import get_project_settings
from rmq.commands import Producer
from rmq.utils import TaskStatusCodes
from database.models import ProductDetail


class ProductDetailProducer(Producer):
    def __init__(self):
        super().__init__()
        settings = get_project_settings()
        self.task_queue_name = settings.get("PRODUCT_DETAIL_TASKS")
        self.reply_to_queue_name = settings.get("PRODUCT_DETAIL_REPLIES")

    def build_task_query_stmt(self, chunk_size):
        stmt = select([ProductDetail.id, ProductDetail.url]).where(
            ProductDetail.status == TaskStatusCodes.NOT_PROCESSED.value
        ).order_by(ProductDetail.id.asc()).limit(chunk_size)
        return stmt

    def build_task_update_stmt(self, db_task, status):
        return (
            update(ProductDetail)
            .where(ProductDetail.id == db_task["id"])
            .values({"status": status})
        )
