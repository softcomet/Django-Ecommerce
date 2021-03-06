from __future__ import unicode_literals

from django.db import models
from django.core.files.base import ContentFile

import datetime

from inventory.models import Product, StockLocation
from contacts.models import Relation, RelationAddress, Agent
from sprintpack.api import SprintClient

from contacts.countries import COUNTRY_CHOICES
from contacts.currencies import CURRENCY_CHOICES
from contacts.customer_types import CUSTOMER_TYPE_CHOICES

from pricelists.models import PriceList, PriceListItem, PriceTransport

from .helpers import get_correct_sales_order_item_price
from .documents import picking_list, customs_invoice, commission_report

import logging
logger = logging.getLogger(__name__)

class PriceListAssignment(models.Model):
    FORMAT_CHOICES = (
        ('csv', 'csv'),
        ('pdf', 'pdf'),
        ('json', 'json'),
    )
    relation = models.ForeignKey(Relation, blank=True, null=True)
    price_list = models.ForeignKey(PriceList, blank=True, null=True)
    agent = models.ForeignKey(Agent, blank=True, null=True)
    active = models.BooleanField(default=True)
    email_to = models.CharField(blank=True, null=True, max_length=100)
    email_to_name = models.CharField(blank=True, null=True, max_length=100)
    format = models.CharField(choices=FORMAT_CHOICES, max_length=4, default='pdf')

    def __unicode__(self):
        name, email = self.receiver
        return u'{} <{}>'.format(name, email)
    
    @property
    def receiver(self):
        if self.email_to:
            email = self.email_to
        elif self.relation:
            email = self.relation.contact_email
        elif self.agent:
            email = self.agent.contact_email

        if self.email_to_name:
            name = self.email_to_name
        elif self.relation:
            name = self.relation.contact_full_name
        elif self.agent:
            name = self.agent.contact_full_name

        return name, email
        

class SalesOrder(models.Model):
    STATUS_CHOICES = (
        ('DR', 'Draft'),
        ('WC', 'Waiting for client approval'),
        ('WA', 'Waiting for approval'),
        ('PM', 'Pending Materials'),
        ('PR', 'In Production'),
        ('PS', 'Pending Shipping'),
        ('PD', 'Partially Shipped'),
        ('SH', 'Shipped'),
        ('CA', 'Cancelled'),
        ('RF', 'Refunded'),
    )

    client = models.ForeignKey(Relation,  limit_choices_to={'is_client': True})
    client_reference = models.CharField(max_length=15, blank=True, null=True)
    ship_to = models.ForeignKey(RelationAddress, related_name='ship_to')
    transport_cost = models.FloatField(blank=True, null=True)
    sample_order = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateField(blank=True, null=True)
    partial_delivery_allowed = models.BooleanField(default=False)

    status = models.CharField(choices=STATUS_CHOICES, max_length=2, default='DR')

    discount_pct = models.FloatField(blank=True, null=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    _xero_invoice_id = models.CharField(max_length=100, blank=True, null=True)

    is_paid = models.BooleanField(default=False)
    paid_commission = models.BooleanField(default=False)
    paid_on_date = models.DateField(blank=True, null=True)

    price_list = models.ForeignKey(PriceList, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if self.status == 'DR' and self.transport_cost is None:
            self.transport_cost = self.get_tranport_price()

        if self.price_list is None:
            self.price_list = self.client.price_list

        super(SalesOrder, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Order #{} for {}'.format(self.id, self.client)

    @property
    def total_order_value(self):
        value = 0
        for i in self.salesorderproduct_set.all():
            value += i.total_price

        if self.discount_pct:
            value -= value * (self.discount_pct / 100)
            
        return value

    @property 
    def payment_terms(self):
        if self.client.payment_days == 0:
            return u'Advance Payment'
        else:
            return u'Net {} days'.format(self.client.payment_days)

    def mark_as_paid(self):
        self.paid_on_date = datetime.date.today()
        self.is_paid = True
        self.status = 'WA'
        return self.save()


    def get_tranport_price(self):
        try:
            return PriceTransport.objects.filter(
                country=self.ship_to.country,
                order_from_price__gte=self.total_order_value).order_by(
                    'order_from_price')[0].shipping_price
        except (PriceTransport.DoesNotExist, IndexError):
            return 0.0


class SalesOrderProduct(models.Model):
    sales_order = models.ForeignKey(SalesOrder)
    input_sku = models.CharField(max_length=20, blank=True, null=True)
    price_list_item = models.ForeignKey(PriceListItem, blank=True, null=True)
    qty = models.IntegerField()
    unit_price = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return u'{}x {}, order: {}'.format(self.qty, self.price_list_item, self.sales_order)

    @property
    def total_price(self):
        try:
            return self.qty * self.unit_price
        except TypeError:
            return 0

    def save(self, *args, **kwargs):
        ## Find the right price.
        if self.price_list_item is None:
            try:
                if self.sales_order.price_list is not None:
                    self.price_list_item = PriceListItem.objects.filter(
                        product__sku=self.input_sku, price_list=self.sales_order.price_list)[0]
                else:
                    self.price_list_item = PriceListItem.objects.filter(product__sku=self.input_sku)[0]
            except Exception:
                pass

        if self.unit_price is None or self.unit_price == '':
            self.unit_price = get_correct_sales_order_item_price(self.price_list_item, self.qty)
        super(SalesOrderProduct, self).save(*args, **kwargs)


class SalesOrderNote(models.Model):
    salesorder = models.ForeignKey(SalesOrder)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalesOrderDeliveryItem(models.Model):
    sales_order_delivery = models.ForeignKey('SalesOrderDelivery')
    product = models.ForeignKey(Product)
    qty = models.IntegerField()

    class Meta:
        unique_together = ('product', 'sales_order_delivery')

    def __unicode__(self):
        return '{} {} {}'.format(
            self.sales_order_delivery,
            self.product,
            self.qty)


class SalesOrderDelivery(models.Model):
    STATUS_CHOICES = (
        ('AUTO', 'Automatic Shipment'),
        ('MANU', 'Manual Change'),
    )
    sales_order = models.ForeignKey(SalesOrder)
    _sprintpack_order_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='AUTO', max_length=4)

    class Meta:
        verbose_name_plural = "Sales order deliveries"

    def __unicode__(self):
        return u'Shipment #{}'.format(self._shipment_reference())

    def save(self, *args, **kwargs):
        if not self.id:
            ## Auto-Add products to deliver
            super(SalesOrderDelivery, self).save(*args, **kwargs)
            products_to_add = {}
            for pr in self.sales_order.salesorderproduct_set.all():
                product = pr.price_list_item.product
                products_to_add[product] = pr.qty

            for delivery in self.sales_order.salesorderdelivery_set.all():
                for pr in delivery.salesorderdeliveryitem_set.all():
                    product = pr.product
                    products_to_add[product] -= pr.qty

            for product, qty in products_to_add.items():
                SalesOrderDeliveryItem.objects.create(
                   sales_order_delivery=self,
                   product=product,
                   qty=qty)
        super(SalesOrderDelivery, self).save(*args, **kwargs)

    def _sales_order_shipment_id(self):  
        return SalesOrderDelivery.objects.filter(sales_order=self.sales_order,
            id__lt=self.id).order_by('id').count() + 1  ## +1 since queryset starts with 0 

    def _shipment_reference(self):
        return u'{}-{}'.format(self.sales_order.id, self._sales_order_shipment_id())

    def picking_list(self):
        '''create picking_list for a sales-order shipment'''
        return picking_list(self)

    def customs_invoice(self):
        '''create an invoice for customs which always includes a shipping-cost'''
        return customs_invoice(self)


    def ship_with_sprintpack(self):
        '''ship with sprintpack'''
        client = self.sales_order.client
        sales_order = self.sales_order
        product_order_list = [{'ean_code': prod.product.ean_code, 'qty': prod.qty} \
            for prod in self.salesorderdeliveryitem_set.all()]

        # attachment_file_list = [self.picking_list()]
        attachment_file_list = []
        if not sales_order.ship_to.is_eu_country:
            ## We need 3 copies
            attachment_file_list.append(self.customs_invoice())

        response = SprintClient().create_order(
            order_number=self.id, ## Provide shipment id instead of order-id for uniqueness .
            order_reference=self._shipment_reference(),  ## used combined reference for uniqueness.
            company_name=client.business_name,
            contact_name=client.contact_full_name, 
            address1=client.address1, 
            address2=client.address2, 
            postcode=client.postcode, 
            city=client.city, 
            country=client.country, 
            phone=client.contact_phone,
            product_order_list=product_order_list, 
            attachment_file_list=attachment_file_list,
            partial_delivery=sales_order.partial_delivery_allowed
            )
        logger.debug(response)
        self._sprintpack_order_id = response
        self.save()

    @property 
    def request_sprintpack_order_status(self):
        try:
            return SprintClient().request_order_status(self._sprintpack_order_id)
        except Exception:
            return False

    @property
    def request_sprintpack_order_status_label(self):
        try:
            return SprintClient().request_order_status_label(self._sprintpack_order_id)
        except Exception:
            return False

    def cancel_sprintpack_shipment(self):
        return SprintClient().cancel_order(self._sprintpack_order_id)


class CommissionNote(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT)
    commission_paid = models.BooleanField(default=False)
    sales_report = models.FileField(blank=True,
        null=True,
        upload_to='media/sales/sales_reports/%Y/%m/%d')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        

    def __unicode__(self):
        return u'Commission Note {} {}'.format(
            self.agent,
            self.created_at.strftime('%d-%m-%Y'))

    def save(self, *args, **kwargs):
        if not self.pk:
            super(CommissionNote, self).save(*args, **kwargs)
            self.create_items()
            self.create_and_set_sales_report()
        
        return super(CommissionNote, self).save(*args, **kwargs)

    @property 
    def calculate_commission(self):
        return self.agent.return_commission(self.sales_total())

    def sales_total(self):
        sales = 0.0

        for s in self.commissionnoteitem_set.all():
            sales += s.sales_order.total_order_value

        return sales

    def create_items(self):
        for relation in self.agent.relation_set.all().filter(salesorder__is_paid=True, 
                salesorder__paid_commission=False, salesorder__sample_order=False):
            for order in relation.salesorder_set.filter(is_paid=True, paid_commission=False):
                CommissionNoteItem.objects.create(
                    commission_note=self,
                    sales_order=order)


    def create_and_set_sales_report(self):
        commission_jtems = []
        sales_total = self.sales_total()
        commission_total = self.calculate_commission

        orders = []
        for item in self.commissionnoteitem_set.all():
            order = item.sales_order

            try:
                date_paid = order.paid_on_date.strftime('%d/%m/%Y')
            except AttributeError:
                date_paid = u'Unkown'            

            commision_item = {u'order #': order.id,
                u'order data': order.created_at.strftime('%d/%m/%Y'),
                u'client name': order.client.business_name,
                u'sale total': order.total_order_value,
                u'date paid':  date_paid}
            commission_jtems.append(commision_item)

        report = commission_report(agent=self.agent,
            commission_items=commission_jtems,
            sales_total=sales_total, 
            commission_total=commission_total,
            report_date=self.created_at)

        filename = '{}.pdf'.format(self.__unicode__())
        self.sales_report.save(filename, ContentFile(report))
    

class CommissionNoteItem(models.Model):
    commission_note = models.ForeignKey(CommissionNote, on_delete=models.PROTECT)
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'Order {} for {}'.format(
            self.sales_order.id,
            self.commission_note)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.sales_order.paid_commission = True
            self.sales_order.save()
        return super(CommissionNoteItem, self).save(*args, **kwargs)

