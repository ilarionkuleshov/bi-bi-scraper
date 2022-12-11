# -*- coding: utf-8 -*-
import datetime
from os import path
from typing import List, Dict, Union

from sqlalchemy import select, or_
from sqlalchemy.dialects.mysql import dialect
from sqlalchemy.sql.base import Executable as SQLAlchemyExecutable
from twisted.enterprise.adbapi import Transaction
from twisted.internet import reactor, defer

from commands.base import BaseCSVExporter
from database.models import ProductDetail


class BaseExporter(BaseCSVExporter):

    def __init__(self):
        super(BaseExporter, self).__init__()
        self.table = ProductDetail
        self.file_timestamp_format = "%Y_%m_%d_%H_%M_%S_%f"
        self.excluded_columns = ["exception", "status", "created_at", "updated_at", "sent_to_customer"]
        self.filename_prefix = "result_"
        self.exported_records = 0
        self.exported_to_file = 0

    def add_options(self, parser) -> None:
        super().add_options(parser)

        parser.add_option(
            "-n",
            "--number_of_records",
            dest="number_of_records",
            default=None,
            help="number of records to export"
        )

        parser.add_option(
            "-r",
            "--records_in_file",
            dest="records_in_file",
            default=1000,
            help="max records in result file"
        )

        parser.add_option(
            "-p",
            "--path",
            dest="path",
            default="data",
            help="export path for result file"
        )

        parser.add_option(
            "-c",
            "--chunk_size",
            dest="chunk_size",
            default=None,
            help="chunk size"
        )

        opts, _ = parser.parse_args()

        self.number_of_records = int(opts.number_of_records) if opts.number_of_records else None
        self.records_in_file = int(opts.records_in_file)
        self.export_path = opts.path
        self.chunk_size = int(opts.chunk_size) if opts.chunk_size else self.chunk_size

        if self.chunk_size > self.records_in_file:
            self.chunk_size = self.records_in_file

    def get_data(self, transaction: Transaction, chunk_size: int = None) -> Union[tuple, Dict]:
        if chunk_size is None:
            chunk_size = self.chunk_size

        if self.number_of_records is None or self.number_of_records - self.exported_records >= chunk_size:
            current_chunk_size = chunk_size
        elif self.number_of_records != self.exported_records:
            current_chunk_size = self.number_of_records - self.exported_records
        else:
            current_chunk_size = None

        if current_chunk_size is not None:
            stmt = self.build_select_query_stmt(current_chunk_size)
            self.exported_records += current_chunk_size

            if isinstance(stmt, SQLAlchemyExecutable):
                stmt_compiled = stmt.compile(compile_kwargs={"literal_binds": True}, dialect=dialect())
                transaction.execute(str(stmt_compiled))
            return transaction.fetchone() if chunk_size == 1 else transaction.fetchall()
        else:
            return None

    def export(self, rows: Union[tuple, Dict]) -> None:
        if not rows:
            if self.file_exists:
                self.logger.debug(f'Export finished successfully to {path.basename(self.file_path)}.')
            elif self.exported_records > 0:
                self.logger.info("export finished successfully")
            else:
                self.logger.info("exportable records not found in DB")
            reactor.stop()
        else:
            if self.chunk_size == 1:
                rows = [rows]
            else:
                rows = list(rows)
            rows = self.map_columns(rows)
            self.get_headers(rows[0])
            self.save(rows)
            deferred_interactions = []
            for row in rows:
                deferred_interactions.append(self.db_connection_pool.runInteraction(self.update, row))
            deferred_list = defer.DeferredList(deferred_interactions, consumeErrors=True)
            deferred_list.addCallback(self._on_row_update_completed)
            deferred_list.addErrback(self._on_row_update_error)

    def save(self, rows: List[Dict]) -> None:
        if self.exported_to_file == 0:
            self.file_path = self.get_file_path()

        rows_num = len(rows)
        not_exported_to_file = self.records_in_file - self.exported_to_file
        if not_exported_to_file >= rows_num:
            self.write_to_file(rows)
            self.exported_to_file += rows_num
        elif self.records_in_file != self.exported_to_file:
            self.write_to_file(rows[:not_exported_to_file])
            self.exported_to_file = 0
            self.save(rows[not_exported_to_file:])
        else:
            self.exported_to_file = 0
            self.save(rows)

    def get_file_path(self, timestamp_format=None, prefix=None, postfix=None, extension=None):
        if timestamp_format is None:
            timestamp_format = self.file_timestamp_format
        if prefix is None:
            prefix = self.filename_prefix
        if postfix is None:
            postfix = self.filename_postfix
        if extension is None:
            extension = self.file_extension
        export_path = path.abspath(self.export_path)
        file_name = f'{prefix}{datetime.datetime.now().strftime(timestamp_format)}{postfix}.{extension}'
        return path.join(export_path, file_name)

    def build_select_query_stmt(self, chunk_size: int) -> SQLAlchemyExecutable:
        if columns := self.specify_columns():
            return select(*columns).limit(chunk_size).where(
                self.table.sent_to_customer == None, or_(self.table.status == 2, self.table.status == 21))
        else:
            return select(self.table).limit(chunk_size).where(
                self.table.sent_to_customer == None, or_(self.table.status == 2, self.table.status == 21))
