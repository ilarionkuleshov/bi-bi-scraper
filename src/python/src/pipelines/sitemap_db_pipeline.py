# -*- coding: utf-8 -*-
import logging
from twisted.enterprise import adbapi

from MySQLdb.cursors import DictCursor

from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import insert

from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DontCloseSpider

from items import SitemapItem
from database.models.sitemap import Sitemap


class SitemapDBPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_idle, signal=signals.spider_idle)
        return o

    def __init__(self, crawler):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.crawler = crawler
        self.__spider = None
        self.project_settings = get_project_settings()

        self.db_connection_pool = None
        self.pending_items_number = 0

    def spider_opened(self, spider):
        """execute on spider_opened signal and initialize connection, callbacks, start consuming"""
        """Set current spider instance"""
        self.__spider = spider

        self.db_connection_pool = adbapi.ConnectionPool(
            "MySQLdb",
            host=self.project_settings.get("DB_HOST"),
            port=self.project_settings.getint("DB_PORT"),
            user=self.project_settings.get("DB_USERNAME"),
            passwd=self.project_settings.get("DB_PASSWORD"),
            db=self.project_settings.get("DB_DATABASE"),
            charset="utf8mb4",
            use_unicode=True,
            cursorclass=DictCursor,
            cp_reconnect=True,
            cp_max=1,
        )

    def spider_idle(self, spider):
        if self.pending_items_number > 0:
            raise DontCloseSpider

    def _item_stored(self, _result):
        self.pending_items_number -= 1

    def _save_sitemap_interaction(self, transaction, item):
        stmt = insert(Sitemap).values(url=item["url"]).prefix_with("IGNORE")
        transaction.execute(self._compile_and_stringify_statement(stmt))
        return

    @staticmethod
    def _compile_and_stringify_statement(stmt):
        return str(
            stmt.compile(
                compile_kwargs={"literal_binds": True}, dialect=mysql.dialect()
            )
        )

    def process_item(self, item, spider):
        if isinstance(item, SitemapItem):
            d = self.db_connection_pool.runInteraction(
                self._save_sitemap_interaction, dict(item)
            )
            d.addCallback(self._item_stored)
            self.pending_items_number += 1
        return item
