# -*- coding: utf-8 -*-
from sqlalchemy import select, update
from scrapy.utils.project import get_project_settings
from rmq.commands import Producer
from rmq.utils import TaskStatusCodes
from database.models import Sitemap


class SitemapProducer(Producer):
    def __init__(self):
        super().__init__()
        settings = get_project_settings()
        self.task_queue_name = settings.get("SITEMAP_TASKS")
        self.reply_to_queue_name = settings.get("SITEMAP_REPLIES")

    def build_task_query_stmt(self, chunk_size):
        stmt = select([Sitemap.id, Sitemap.url]).where(
            Sitemap.status == TaskStatusCodes.NOT_PROCESSED.value
        ).order_by(Sitemap.id.asc()).limit(chunk_size)
        return stmt

    def build_task_update_stmt(self, db_task, status):
        return (
            update(Sitemap)
            .where(Sitemap.id == db_task["id"])
            .values({"status": status})
        )
