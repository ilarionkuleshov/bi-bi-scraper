# -*- coding: utf-8 -*-
import re
import json
import traceback
from furl import furl

from scrapy import Request
from scrapy.utils.project import get_project_settings
from rmq.utils.decorators import rmq_callback

from spiders import BaseRMQSpider
from items import SerpPageItem


class SitemapSpider(BaseRMQSpider):
    name = 'sitemap'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.task_queue_name = settings.get("SITEMAP_TASKS")
        self.result_queue_name = settings.get("SITEMAP_RESULTS")

    def next_request(self, _delivery_tag, msg_body):
        data = json.loads(msg_body)
        return Request(
            data["url"],
            meta={
                "delivery_tag": _delivery_tag,
            },
            callback=self.parse,
            errback=self._errback,
            dont_filter=True,
        )

    @rmq_callback
    def parse(self, response):
        try:
            urls = re.findall(r'<loc>(.*?)</loc>', response.text)
            if urls:
                for url in urls:
                    url = url.replace("%2520", "-")
                    url_details = self.get_url_details(url)
                    if url_details is not None:
                        yield SerpPageItem(
                            {
                                "url": url,
                                "brand": url_details["brand"],
                                "model": url_details["model"],
                                "category": url_details["category"],
                                "subcategory": url_details["subcategory"]
                            }
                        )
            else:
                raise Exception(f"Failed to get urls from {response.url}")
        except Exception as e:
            self._inject_exception_to_task(
                response.meta.get("delivery_tag"), e
            )
            self.logger.warning(traceback.format_exc())

    def get_url_details(self, url):
        try:
            segments = [s.lower() for s in furl(url).path.segments]
            if "topcategory" in segments[0] and segments[1].isdigit() and not "group-" in segments[2] and "group-" in segments[4]:
                if len(segments) > 6:
                    subcategory = segments[-1]
                else:
                    subcategory = None
                return {
                    "brand": segments[2],
                    "model": segments[3],
                    "category": segments[5],
                    "subcategory": subcategory
                }
            else:
                return None
        except:
            return None
