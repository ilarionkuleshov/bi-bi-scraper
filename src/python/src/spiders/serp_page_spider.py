# -*- coding: utf-8 -*-
import json
import traceback

from scrapy import Request
from scrapy.utils.project import get_project_settings
from rmq.utils.decorators import rmq_callback

from spiders import BaseRMQSpider
from items import ProductDetailItem


class SerpPageSpider(BaseRMQSpider):
    name = 'serp_page'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.task_queue_name = settings.get("SERP_PAGE_TASKS")
        self.result_queue_name = settings.get("SERP_PAGE_RESULTS")

    def next_request(self, _delivery_tag, msg_body):
        data = json.loads(msg_body)
        return Request(
            data["url"],
            meta={
                "serp_brand": data["brand"],
                "serp_model": data["model"],
                "serp_category": data["category"],
                "delivery_tag": _delivery_tag,
            },
            callback=self.parse,
            errback=self._errback,
            dont_filter=True,
        )

    @rmq_callback
    def parse(self, response):
        try:
            urls = response.xpath("//a[contains(@href, '/Product/Details/')]/@href").getall()
            for url in urls:
                yield ProductDetailItem(
                    {
                        "url": f"https://bi-bi.com.ua{url}",
                        "brand": response.meta.get("serp_brand"),
                        "model": response.meta.get("serp_model"),
                        "category": response.meta.get("serp_category"),
                    }
                )
            next_page_href = response.xpath("//a[@rel='next']/@href").get()
            if next_page_href:
                yield Request(
                    f"https://bi-bi.com.ua{next_page_href}",
                    meta={
                        "serp_brand": response.meta.get("serp_brand"),
                        "serp_model": response.meta.get("serp_model"),
                        "serp_category": response.meta.get("serp_category"),
                        "delivery_tag": response.meta.get("delivery_tag"),
                    },
                    callback=self.parse,
                    errback=self._errback,
                    headers={
                        "referer": response.url,
                    },
                )
        except Exception as e:
            self._inject_exception_to_task(
                response.meta.get("delivery_tag"), e
            )
            self.logger.warning(traceback.format_exc())
