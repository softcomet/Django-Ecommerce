from defaults.helpers import dynamic_file_httpresponse
from defaults.rounding import ROUND_DIGITS

from xero_local import api as xero_api

def get_correct_sales_order_item_price(pricelist_item, qty):
    '''Return the price that matches the right qty for the product'''
    ## Filter available price tiers
    tier_identifier = 'per_'
    price_tiers = []
    for key in pricelist_item.__dict__.keys():
        if key.startswith(tier_identifier):
            price_tiers.append(int(key.split('_')[-1]))
    price_tiers.sort(reverse=True)

    ## try to match one
    for tier in price_tiers:
        if qty >= tier:
            price = getattr(pricelist_item, '{}{}'.format(tier_identifier, tier))
            if not price or price == None or price == '':
                pass
            else:
                return price


def print_picking_list_admin(sales_order_shipments):
    items = {'{} {}.pdf'.format(pr.__unicode__(), pr.sales_order.client): pr.picking_list() for pr in sales_order_shipments}
    return dynamic_file_httpresponse(items, 'picking_lists')


def print_customs_invoice_admin(sales_order_shipments):
    items = {'Commercial Invoice {}.pdf'.format(pr.id): pr.customs_invoice() for pr in sales_order_shipments}
    return dynamic_file_httpresponse(items, 'Commercial_invoices')

def ship_with_sprintpack_admin(shipments):
    for shipment in shipments:
        shipment.ship_with_sprintpack()

def cancel_sprintpack_shipment_admin(shipments):
    for shipment in shipments:
        shipment.cancel_sprintpack_shipment()


# def export_datafile_for_pricelist_admin(pricelists):
#     exported_files = {}
#     for pricelist in pricelists:
#         exported_files['{}.csv'.format(pricelist)] = export_product_datafile(pricelist)

#     return exported_files


## Admin helper ##
def create_sales_invoice(modeladmin, request, queryset):
    for q in queryset:
        invoice_number, invoice_id, created = xero_api.create_invoice(q)
        if created:
            q.invoice_number = invoice_number
            q._xero_invoice_id = invoice_id
        
        q.save()
create_sales_invoice.short_description = 'Generate sales invoice in Xero'

def print_picking_lists(modeladmin, request, queryset):
    return print_picking_list_admin(queryset)
print_picking_lists.short_description = 'Print Picking lists' 


def print_customs_invoice(modeladmin, request, queryset):
    return print_customs_invoice_admin(queryset)
print_customs_invoice.short_description = 'Print Customs Invoice'

def ship_with_sprintpack(modeladmin, request, queryset):
    return ship_with_sprintpack_admin(queryset)
ship_with_sprintpack.short_description = 'Ship with sprintpack'


def cancel_shipment_with_sprintpack(modeladmin, request, queryset):
    return cancel_sprintpack_shipment_admin(queryset)
cancel_shipment_with_sprintpack.short_description = 'Cancel sprintpack shipment'


# def export_datafile_for_pricelist(modeladmin, request, queryset):
#     return export_datafile_for_pricelist_admin(queryset)
# export_datafile_for_pricelist.short_description = 'Print product data-files'