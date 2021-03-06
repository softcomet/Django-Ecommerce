from django.contrib import admin
from defaults.admin import DefaultAdmin, DefaultInline

from .models import *
from .helpers import print_purchase_order_report, mark_confirmed, \
    mark_as_awaiting_for_confirmation, mark_as_awaiting_delivery

##############
### Inines ###
##############
class PurchaseOrderItemInline(DefaultInline):
    readonly_fields = ['sku_supplier']
    model = PurchaseOrderItem

class PurchaseOrderConfirmationAttachmentInline(DefaultInline):
    model = PurchaseOrderConfirmationAttachment

class DeliveryItemInline(DefaultInline):
    model = DeliveryItem

class DeliveryAttachmentInline(DefaultInline):
    model = DeliveryAttachment

#####################
### Custom Admins ###
#####################
class PurchaseOrderAdmin(DefaultAdmin):
    readonly_fields = ['order_value', 'created_at', 'updated_at', 'id']
    list_display = ['__unicode__', 'status','created_at', 'est_delivery']
    list_filter = ['status', 'supplier', 'est_delivery']
    inlines = [PurchaseOrderItemInline, PurchaseOrderConfirmationAttachmentInline]
    actions = [print_purchase_order_report, mark_as_awaiting_for_confirmation, mark_as_awaiting_delivery]


class PurchaseOrderItemAdmin(DefaultAdmin):
    list_display = ['__unicode__', 'purchase_order','material', 'unit_price']
    search_fields = ['material__sku_supplier']
    # list_filter = []

class DeliveryAdmin(DefaultAdmin):
    list_display = ['__unicode__', 'status', 'delivered']
    inlines = [DeliveryItemInline, DeliveryAttachmentInline]
    readonly_fields = ['_is_confirmed']
    actions = [mark_confirmed]


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderItem, PurchaseOrderItemAdmin)
admin.site.register(Delivery, DeliveryAdmin)