import requests
import xmltodict
import os
import base64

from django.template.loader import render_to_string
from django.conf import settings

from .exceptions import UnkownError, WrongFileTypeError
from xml.parsers.expat import ExpatError

import logging
logger = logging.getLogger(__name__)

class SprintClient:
    def __init__(self):
        self.webshopcode = settings.SPRINTPACK['webshopcode'] 
        self.url = settings.SPRINTPACK['url'] 
        self.connect_to_server = settings.SPRINTPACK['connect_to_server'] 
        self.headers = {
            # 'content-type': 'text/xml',
            'content-type': 'application/soap+xml',
        }
        logger.debug('Initialising SprintClient with webshopcode {} and connect_to_server {}'.format(
            self.webshopcode, 
            self.connect_to_server))
    @staticmethod
    def parse_xml(data):
        try:
            return xmltodict.parse(data, dict_constructor=dict)[u'soap:Envelope'][u'soap:Body'][u'SoapRequestResult']
        except ExpatError as e:
            import sys
            raise Exception('{}\n{}'.format(e, data)), None, sys.exc_info()[2]

    def render_xml(self, data, template_name):
        '''render and return xml from the given data with the given template_name'''
        path = os.path.join('sprintpack', template_name)
        post_data = {
            'webshopcode': self.webshopcode,
            'post_data': data,
        }
        return render_to_string(path, post_data)

    @staticmethod
    def encode_file_to_base64(path):
        '''encode a file to base64 data from either local path or http(s) url'''

        extension = path[-3:].lower()
        if extension != 'pdf':
            raise WrongFileTypeError('{} is not supported.  Only PDF.'.format(extension))

        if path.startswith('http'):
            file_content = requests.get(path).content
        else:
            with open(path, 'rb') as f:
                file_content = f.read()

        return base64.b64encode(file_content)


    def post(self, soapaction, data=False):
        '''
        Post the request to the sprintpack server, with the given webshopcode.
        - headers will add the SoapAction
        - data will be send raw
        Return: response content xml, unprocessed
        '''
        headers = self.headers.copy()
        headers['SoapAction'] = soapaction
        xml_template_name = '{}.xml'.format(soapaction)

        xml_data = self.render_xml(data, xml_template_name)
        if self.connect_to_server:
            response = self.parse_xml(requests.post(url=self.url, data=xml_data, headers=headers).content)
            try:
                if response[u'Status'] == u'Error':
                    raise Exception('ErrorCode {} for {} with message: {}'.format(
                        response['ErrorCode'],
                        soapaction,
                        response['Reason']))
                elif response[u'Status'] == u'OK':
                    return response
                else:
                    raise UnkownError('Status contained value {} instead of Error'.format(response['Status']))
            except KeyError:
                return response
        else:
            return xml_data

    def create_pre_advice(self, expected_date_of_delivery, product_list):
        ''' create a pre-advice / aka announce goods to be delivered 
        :param date_of_delivery: datetime object
        'param product_list: list of dicts [{'ean_code':0000, 'qty':3}]
        :return: pre-advice id
        '''
        ##TODO: Test
        xml_data = {
            'date_of_delivery': expected_date_of_delivery.strftime('%Y%m%d'),
            'product_list': product_list,
        }
        
        response = self.post('CreatePreAdvice', xml_data)
        if type(response) == dict:
            return response[u'PreAdviceID']
        else:
            return response

    def create_order(self, order_number, order_reference, company_name,
        contact_name, address1, address2, postcode, city, country, phone,
        product_order_list, attachment_file_list):
        '''Create an order:
        :param order_number: order-number of the order 
        :param order_reference: Customer reference of the order
        :param company_name:
        :param contact_name: full name of the customer/contact
        :param address1:
        :param address2: False or None if not needed
        :param postcode:
        :param city:
        :param country: 2 Digit ISO code
        :param phone: full international phone
        :param product_order_list: Items ordered in following format: [{'ean_code': 333333, 'qty': 3}]
        :param attachment_file_list: List of file-attachments ['/link/to/file.pdf', 'http://link.to.file']
        :return: Sprintpack OrderID
        '''
        ## TODO: Test
        xml_data = {
            'order_number': order_number,
            'order_reference':order_reference,
            'customer': {
                'company_name': company_name,
                'contact_name': contact_name,
                'address1': address1,
                'address2': address2,
                'postcode': postcode, 
                'city': city,
                'country': country, ## 2 letter ISO format
                'phone': phone,
            },
            'orderlines': product_order_list,
        }

        xml_data['orderlines'] = product_order_list

        xml_data['additional_documents'] = []
        for f in attachment_file_list:
            xml_data['additional_documents'].append(self.encode_file_to_base64(f))

        response = self.post('CreateOrder', xml_data)
        if type(response) == dict:
            return response[u'OrderID']
        else:
            return response

    def change_pre_advice_status(self, pre_advice_data):
        ''' change a pre-advice status '''
        ##TODO
        return self.post(converted_pre_advice_data, 'ChangePreAdviceStatus')

    def cancel_order(self, order_number):
        '''cancel the order.  Currently only cancel is avilable at the api.  Original name ChangeOrderStatus'''
        xml_data = {
            'order_number': order_number,
        }
        return self.post('ChangeOrderStatus', xml_data)

    def create_product(self, ean_code, sku, description):
        '''create one product'''
        data = {
            'ean_code': ean_code,
            'sku': sku, 
            'description': description,
        }
        return self.create_products([data])

    def create_products(self, product_list):
        '''create a list of dicts with product_data'''
        ##TODO: Cut description to max 60chars
        xml_data = {
            'products': product_list
        }
        return self.post('CreateProducts', xml_data)

    def request_inventory(self, ean_code=False):
        '''Request the data about the available stock
        :param ean_code: ean_code of the poduct of False
        :return: inventory of requested ean_code, or list of inventory of all products known
        '''
        xml_data = {
            'ean_code': ean_code,
            'inventory': 'True',
        }
        response = self.post('RequestInventory', xml_data)
        if type(response) == dict:
            return response[u'Inventory']
        else:
            return response
         
    def request_order_status(self, order_number):
        '''request the status of an order'''
        ## FIXME: client.request_order_status(2222) >> Throws expat-error on BPOST link - invalid excaping of &
        ## Request sent to Orlando on 30/09/2017
        xml_data = {
            'order_number': order_number
        }
        return self.post('RequestOrderStatus', xml_data)
