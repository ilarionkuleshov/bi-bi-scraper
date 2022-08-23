# -*- coding: utf-8 -*-
import traceback

from rmq.commands import Consumer
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import insert

from database.models import SerpPage


class SitemapResultsConsumer(Consumer):
    def __init__(self):
        super().__init__()
        self.queue_name = self.project_settings.get("SITEMAP_RESULTS")

    def process_message(self, transaction, message_body):
        try:
            stmt = insert(SerpPage).values(
                {
                    "url": message_body["url"],
                    "brand": message_body["brand"],
                    "model": message_body["model"],
                    "category": message_body["category"],
                }
            ).prefix_with("IGNORE")
            transaction.execute(str(stmt.compile(dialect=mysql.dialect())),
                                tuple(stmt.compile(dialect=mysql.dialect()).params.values()))
        except Exception as e:
            self.logger.warning(str(e))
            self.logger.debug(traceback.format_exc())
        return True

    def build_message_store_stmt(self, message_body):
        pass
