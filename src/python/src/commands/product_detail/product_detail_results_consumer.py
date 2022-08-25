# -*- coding: utf-8 -*-
import traceback

from rmq.commands import Consumer
from sqlalchemy.dialects import mysql
from sqlalchemy import update

from database.models import ProductDetail


class ProductDetailResultsConsumer(Consumer):
    def __init__(self):
        super().__init__()
        self.queue_name = self.project_settings.get("PRODUCT_DETAIL_RESULTS")

    def process_message(self, transaction, message_body):
        try:
            stmt = (
                update(ProductDetail)
                .where(ProductDetail.id == message_body["id"])
                .values(
                    {
                        "name": message_body["name"],
                        "images": message_body["images"],
                        "price": message_body["price"],
                        "parameters": message_body["parameters"],
                        "description": message_body["description"],
                        "original_number": message_body["original_number"],
                        "condition": message_body["condition"],
                        "amount": message_body["amount"],
                        "manufacturer": message_body["manufacturer"],
                    }
                )
            )
            transaction.execute(str(stmt.compile(dialect=mysql.dialect())),
                                tuple(stmt.compile(dialect=mysql.dialect()).params.values()))
        except Exception as e:
            self.logger.warning(str(e))
            self.logger.debug(traceback.format_exc())
        return True

    def build_message_store_stmt(self, message_body):
        pass
