from .api import MagentoServer


import logging
logger = logging.getLogger(__name__)

def comparable_dict(dict_original, dict_to_reduce):
    '''reduce a dict to a comparable item'''
    dict_to_return = {}
    for k in dict_original.keys():
        try:
            dict_to_return[k] = dict_to_reduce[k]
        except KeyError:
            dict_to_return[k] = None

    return dict_to_return


def extract_filename(path):
    return path.split('/')[-1]
    

class CompileMagentoProduct:
    def __init__(self, price_list_item):
        self.umbrella_product = price_list_item.product.umbrella_product
        self.product = price_list_item.product
        self.price_list_item = price_list_item
        self.magento = MagentoServer()
        self.product_type = self.product.umbrella_product.\
            umbrella_product_model.get_product_type_display()

    def _get_attribute_set_id(self):
        product_type = self.product_type
        attribute_set_id = None

        for a in self.magento.attribute_set_list():
            if product_type.lower() == a['name'].lower():
                attribute_set_id = a['set_id']
                logger.debug('Matched set {}'.format(attribute_set_id))
            
        if attribute_set_id is None:
            attribute_set_id = 4 #Default
            logger.debug('Setting fallback'.format(attribute_set_id))

        logger.debug('Detected attribute_set_id {} for product_type: {}.'.format(
            attribute_set_id, product_type))
        return attribute_set_id

    def _compile_status_enabled(self, status=True):
        if status:
            return '1'
        else:
            return '2'

    def _compile_tax_class_id(self):
        return '2'

    def _compile_website_ids(self, website='Suzys'):
        return ['1']

    def _compile_visibility(self, search=True, catalog=True):
        if search and catalog:
            return '4'
        elif search and not catalog:
            return '3'
        elif catalog and not search:
            return '2'
        else:
            return '1'

    def _compile_config_price(self):
        ''' return lowest rrp price from umbrella_product.product_set pricelist items '''
        products_ordered = self.price_list_item.price_list.pricelistitem_set.filter(
            product__sku__startswith=self.umbrella_product.base_sku).order_by('rrp')
        return products_ordered[0].rrp

    def _compile_associated_skus(self):
        return [i.sku for i in self.umbrella_product.product_set.all()]

    def _compile_size(self):
        return self.product.product_model.size_description

    def _compile_categories(self):
        ''' return categories to assign and create them if needed'''

        # Check for product_type info:
        product_type = self.product_type
        product_type_parent_category_id = '99' # limit the search for cats
        product_type_category_found = None
        
        for child in self.magento.category_children(product_type_parent_category_id):
            if child['name'].lower() == product_type.lower() or\
                    child['name'][0:-1].lower() == product_type.lower():
                product_type_category_found = child['category_id']
                logger.debug('Found product type category {}'.format(product_type_category_found))

        if product_type_category_found == None:
            product_type_category_found = self.magento.category_create(
                product_type_parent_category_id, product_type.capitalize())
            logger.debug('Created product type category {}'.format(product_type_category_found))

        # Check for collection info:
        collection = self.umbrella_product.collection.name
        collection_parent_category_id = '105'
        collection_category_found = None

        for child in self.magento.category_children(collection_parent_category_id):
            if child['name'].lower() == collection.lower():
                collection_category_found = child['category_id']
                logger.debug('Found collection type category {}'.format(collection_category_found))

        if collection_category_found == None:
            collection_category_found = self.magento.category_create(
                collection_parent_category_id, collection.capitalize())
            logger.debug('Created collection type category {}'.format(collection_category_found))

        return [product_type_category_found, collection_category_found]

    def config_item(self):
        return ['configurable', self._get_attribute_set_id(), self.umbrella_product.base_sku, {
            'name': self.umbrella_product.name,
            # 'short_description': self.umbrella_product.description,
            'status': self._compile_status_enabled(True),
            'tax_class_id': self._compile_tax_class_id(),
            'websites': self._compile_website_ids(),
            'visibility': self._compile_visibility(search=True, catalog=True),
            'price': self._compile_config_price(),
            'categories': self._compile_categories(),
            'associated_skus': self._compile_associated_skus(),
            'options_container': 'container1',

        }]

    def config_item_update(self):
        ptype, set_id, sku, data = self.config_item()
        del data['name']

        return [sku, data]

    def config_item_image_url_list(self):
        compiler.umbrella_product.umbrellaproductimage_set.all()
        return 

    def simple_item(self):
        return ['simple', self._get_attribute_set_id(), self.product.sku, {
            'name': self.product.name,
            'price': self.price_list_item.rrp,
            'status': self._compile_status_enabled(True),
            'visibility': self._compile_visibility(catalog=False, search=False),
            'tax_class_id': self._compile_tax_class_id(),
            'websites': self._compile_website_ids(),
            'size': self.product.product_model.size.short_size,
            'size_chart': self._compile_size(),
        }]

    def simple_item_last(self):
        all_products = [i.sku for i in self.umbrella_product.product_set.all()]
        return self.product.sku == all_products[-1]