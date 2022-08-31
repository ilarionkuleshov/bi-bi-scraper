# -*- coding: utf-8 -*-
from os import path
from typing import List, Dict
import pandas as pd

from . import BaseExporter


class XlsxExporter(BaseExporter):

    def __init__(self):
        super(XlsxExporter, self).__init__()
        self.file_extension = "xlsx"

    def write_to_file(self, rows: List[Dict]) -> None:
        if self.exported_to_file == 0:
            df = pd.DataFrame.from_records(rows)
            df.columns = self.headers
            df.to_excel(self.file_path, sheet_name="product_details", index=False)
        else:
            file_df = pd.read_excel(self.file_path)
            df = pd.DataFrame.from_records(rows)
            pd.concat([file_df, df]).to_excel(self.file_path, sheet_name="product_details", index=False)
        self.logger.info(f'export {len(rows)} records to {path.basename(self.file_path)}')
