"""
NOTE: This is well out of date!
"""


from openpyxl import load_workbook
from collections import defaultdict, namedtuple
from itertools import product


def main():
    path = '/home/cbarnes/data/connectome/Neuropeptide_2015-04-20.xlsx'
    pep_sht_name = 'Peptide Expr'
    rec_sht_name = 'Receptor Expr'
    pep_to_rec_name = 'Peptides'
    rec_to_pep_name = 'Receptors'
    wb = load_workbook(path, read_only=True)
    pep_expr_sht = wb.get_sheet_by_name(pep_sht_name)
    rec_expr_sht = wb.get_sheet_by_name(rec_sht_name)
    pep_to_rec_sht = wb.get_sheet_by_name(pep_to_rec_name)
    rec_to_pep_sht = wb.get_sheet_by_name(rec_to_pep_name)

    def gene_cell_sheet_to_dict(sheet):
        gene_to_cell = defaultdict(list)
        last_gene = ''
        for row in sheet.iter_rows('A3:B{}'.format(sheet.get_highest_row())):
            if not row:
                continue
            if row[0].value:
                val = row[0].value.strip() if 'nlp-37' not in row[0].value else 'pdf-2'
                last_gene = val
            if row[1].value:
                if '?' in row[1].value:
                    continue

                gene_to_cell[last_gene].append(row[1].value.strip())

        return gene_to_cell

    pep_expr = gene_cell_sheet_to_dict(pep_expr_sht)
    rec_expr = gene_cell_sheet_to_dict(rec_expr_sht)

    def pep_rec_sheet_to_dict(sheet):
        d = defaultdict(list)
        for row in sheet.iter_rows('A3:M{}'.format(sheet.get_highest_row())):

            try:
                if row[0].value and row[1].value:
                    pass
                else:
                    continue
            except IndexError:
                continue

            head, *tail = [cell.value.strip() for cell in row if cell.value is not None and '?' not in cell.value]
            if 'nlp-37' in head:
                head = 'pdf-2'

            d[head] = tail

        return d

    pep_to_rec = pep_rec_sheet_to_dict(pep_to_rec_sht)
    rec_to_pep = pep_rec_sheet_to_dict(rec_to_pep_sht)

    def generate_edges():
        Edge = namedtuple('Edge', ['src', 'tgt', 'transmitter', 'receptor'])
        for transmitter, src_nodes in pep_expr.items():
            for receptor in pep_to_rec[transmitter]:
                for src, tgt in product(src_nodes, rec_expr[receptor]):
                    yield Edge(src, tgt, transmitter, receptor)

    with open('np_edgelist_classes.csv', 'w') as f:
        for edge in generate_edges():
            f.write('{},{},{},{}\n'.format(edge.src, edge.tgt, edge.transmitter, edge.receptor))


if __name__ == '__main__':
    main()
    print('done')