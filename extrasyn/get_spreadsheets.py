from urllib import request
import os
from extrasyn.paths import src_root
from datetime import datetime

DOWNLOAD_LINK_BASE = 'https://docs.google.com/spreadsheets/d/{}/export?format=xlsx'

sheet_specs = [
    ('monoamine_spreadsheet.xlsx', '1w2lzsbGU7pkZVq5YizaLdUZtoUjOWk-GhJrkt6THOOs'),
    ('neuropeptide_spreadsheet.xlsx', '1gA1_0p1xv0gmUCx3671FUwkeAA1fnVUpx6hwxJMu9Ns')
]


class SpreadsheetGetter:
    def __init__(self, filename, sheet_id):
        self.path = os.path.join(src_root, filename)
        self.meta_path = self.path + '.meta'
        self.download_link = DOWNLOAD_LINK_BASE.format(sheet_id)

    def download(self):
        response = request.urlopen(self.download_link)
        content = response.read()
        with open(self.path, 'wb') as f:
            f.write(content)

        with open(self.meta_path, 'w') as f:
            f.write(datetime.now().isoformat())


def main():
    for sheet_spec in sheet_specs:
        getter = SpreadsheetGetter(*sheet_spec)
        getter.download()


if __name__ == '__main__':
    main()