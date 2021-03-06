from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus.tables import Table

from printing_tools.documents import SuzysDocument
from django.http import HttpResponse
from django.conf import settings

from .reports_helpers import *

from io import BytesIO
from StringIO import StringIO
import csv
import json
import datetime

import logging
logger = logging.getLogger(__name__)



def export_pricelist_csv(pricelist, include_cost=False, active_only=True):
    ''' export a pricelist to csv'''
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pricelist_suzys.csv"'

    data = get_pricelist_price_data(pricelist, include_cost=include_cost, active_only=active_only)

    c = csv.DictWriter(response, fieldnames=data[0].keys(), delimiter=';')
    c.writeheader()
    [c.writerow(i) for i in data]

    return response


def export_pricelist_pdf(pricelist, include_stock=False, active_only=True):
    ''' export a pricelist to pdf '''
    # Create the HttpResponse object with the appropriate PDF headers.
    document = SuzysDocument()

    if include_stock:
        document.add_title(
            'Price- and Stocklist {} {}'.format(pricelist.name, 
                datetime.date.today().strftime('%d/%m/%Y'))
            )
    else:
        document.add_title(
            'Pricelist {} {}'.format(pricelist.name, datetime.date.today().strftime('%d/%m/%Y'))
        )

    document.add_heading('Products available')
    table_data_dict = get_pricelist_price_data(pricelist, include_stock=include_stock, active_only=active_only)
    table_data = []
    table_data.append(table_data_dict[0].keys())
    logger.debug('header looks like {}'.format(table_data))
    [table_data.append(i.values()) for i in table_data_dict]
    logger.debug('full table_data looks like {}'.format(table_data))
    if include_stock:
        table_columns_width = [0.2, 0.35, 0.10, 0.10, 0.10, 0.10, 0.10]
    else:
        table_columns_width = [0.2, 0.47, 0.11, 0.11, 0.11, 0.11]

    document.add_table(table_data, table_columns_width)

    document.add_paragraph('''If the item you wish is not on stock, please consult us for
        delivery times.'''.strip().replace('\n',''))

    # document.add_heading('Shipping prices')
    # table_data = get_transport_costs()
    # document.add_table(table_data, [0.33]*3)


    return document.print_document()
