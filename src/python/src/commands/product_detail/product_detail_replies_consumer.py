# -*- coding: utf-8 -*-
from rmq.commands import Consumer

from sqlalchemy import update, null
from database.models import ProductDetail


class ProductDetailRepliesConsumer(Consumer):
    def __init__(self):
        super().__init__()
        self.queue_name = self.project_settings.get("PRODUCT_DETAIL_REPLIES")

    def build_message_store_stmt(self, message_body):
        upd_stmt = (
            update(ProductDetail)
            .where(ProductDetail.id == message_body["id"])
            .values(
                {
                    "status": message_body["status"],
                    "exception": message_body["exception"] or null()
                }
            )
        )
        return upd_stmt
