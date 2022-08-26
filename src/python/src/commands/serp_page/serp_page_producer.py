# -*- coding: utf-8 -*-
from sqlalchemy import select, update
from scrapy.utils.project import get_project_settings
from rmq.commands import Producer
from rmq.utils import TaskStatusCodes
from database.models import SerpPage


class SerpPageProducer(Producer):
    def __init__(self):
        super().__init__()
        settings = get_project_settings()
        self.task_queue_name = settings.get("SERP_PAGE_TASKS")
        self.reply_to_queue_name = settings.get("SERP_PAGE_REPLIES")

    def build_task_query_stmt(self, chunk_size):
        stmt = select([SerpPage.id, SerpPage.url, SerpPage.brand, SerpPage.model, SerpPage.category, SerpPage.subcategory]).where(
            SerpPage.status == TaskStatusCodes.NOT_PROCESSED.value
        ).order_by(SerpPage.id.asc()).limit(chunk_size)
        return stmt

    def build_task_update_stmt(self, db_task, status):
        return (
            update(SerpPage)
            .where(SerpPage.id == db_task["id"])
            .values({"status": status})
        )
