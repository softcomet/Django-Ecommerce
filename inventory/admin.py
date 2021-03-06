from django.contrib import admin
from defaults.admin import DefaultAdmin, DefaultInline

from .models import *
from .helpers import product_mark_inactive,\
    product_mark_active,\
    print_box_barcode_label,\
    print_stock_label_38x90, \
    print_washinglabel, \
    print_sample_washinglabel, \
    print_production_notes_for_umbrella_product_EN, \
    print_production_notes_for_umbrella_product_CZ

###############
### Inlines ###
###############
class SizeBreedsInline(DefaultInline):
    model = SizeBreed

class MaterialImageInline(DefaultInline):
    model=MaterialImage

class MaterialDataSheetInline(DefaultInline):
    model=MaterialDataSheet

class StockLocationItemInline(DefaultInline):
    model=StockLocationItem

class ProductModelPatternInline(DefaultInline):
    model=ProductModelPattern
    exclude = ['description', 'name']

class UmbrellaProductModelImageInline(DefaultInline):
    model=UmbrellaProductModelImage

class UmbrellaProductModelProductionDescriptionInline(DefaultInline):
    model=UmbrellaProductModelProductionDescription

class ProductModelInline(DefaultInline):
    model=ProductModel

class UmbrellaProductInline(DefaultInline):
    model=UmbrellaProduct  
    extra=0
    fields = ('name', 'umbrella_product_model',)  
    exclude = ('description', 'complete', 'active')
    readonly_fields = ('colour',)
    can_delete = False

class UmbrellaProductBillOfMaterialInline(admin.TabularInline):
    model = UmbrellaProductBillOfMaterial
    extra = 0
    readonly_fields = ['cost']

class UmbrellaProductImageInline(DefaultInline):
    model = UmbrellaProductImage 

class ProductInline(DefaultInline):
    model=Product  
    extra=0
    # fields = ('name', 'umbrella_product_model',)  
    # exclude = ('description', 'complete', 'active')
    readonly_fields = ['cost']
    # can_delete = False 

class ProductBillOfMaterialInline(admin.TabularInline):
    model = ProductBillOfMaterial
    extra = 0    
    readonly_fields = ['cost']

#####################
### Custom Admins ###
#####################

class CollectionAdmin(admin.ModelAdmin):
    inlines = [UmbrellaProductInline]
    list_display = ['name', 'number','range_type', 'production_location']
    # readonly_fields = ()

class SizeAdmin(DefaultAdmin):
    inlines = [SizeBreedsInline]

class StockLocationAdmin(admin.ModelAdmin):
    inlines = [StockLocationItemInline]

class StockLocationItemAdmin(admin.ModelAdmin):
    list_display = ['material', 'quantity_in_stock', 'quantity_on_its_way', 'location']
    list_filter = ['location']
    search_fields = ['material', 'comment']
    ordering = ('material', 'location')

class MaterialAdmin(DefaultAdmin):
    list_display = ['name', 'sku', 'supplier', 'cost_per_usage_unit', 'usage_units_on_stock']
    list_filter = ['supplier', 'mat_type']
    search_fields = ['name', 'supplier__business_name', 'sku_supplier', 'sku']
    actions = [print_stock_label_38x90]
    inlines = [MaterialImageInline, MaterialDataSheetInline, StockLocationItemInline]

class UmbrellaProductModelAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'product_type', 'number', 'product_images_present']
    list_filter = ['product_type', 'number', 'product_images_present']
    inlines = [ProductModelInline, UmbrellaProductModelImageInline, UmbrellaProductModelProductionDescriptionInline]
    search_fields = ['name']

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'all_patterns_present', 'get_umbrella_poroduct_model_number', 'total_pattern_surface_area', 'number_of_patterns']
    list_filter = ['all_patterns_present', 'umbrella_product_model__number']
    inlines = [ProductModelPatternInline]

    def get_umbrella_poroduct_model_number(self, obj):
        return obj.umbrella_product_model.number
    get_umbrella_poroduct_model_number.admin_order_field  = 'Model Number'  #Allows column order sorting
    get_umbrella_poroduct_model_number.short_description = 'Model Number'  #Renames column head


class ProductModelPatternAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'product']
    list_filter = ['product__umbrella_product_model__number']


class UmbrellaProductAdmin(admin.ModelAdmin):    
    list_display = ['__unicode__','base_sku', 'active', 'complete', 'get_umbrella_product_model_number', 'number_of_sizes']
    list_filter = ['collection', 'collection__number','colour', 'umbrella_product_model__product_type', 'umbrella_product_model__number', 'complete']
    inlines = [ProductInline, UmbrellaProductBillOfMaterialInline, UmbrellaProductImageInline]
    readonly_fields = ['cost']
    actions = [print_production_notes_for_umbrella_product_EN, print_production_notes_for_umbrella_product_CZ]    

    def get_umbrella_product_model_number(self, obj):
        return obj.umbrella_product_model.number
    get_umbrella_product_model_number.admin_order_field = 'Model Number'
    get_umbrella_product_model_number.short_description= 'Model Number'


class UmbrellaProductBillOfMaterialAdmin(admin.ModelAdmin):
    readonly_fields = []


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('sku', 'available_stock', 'cost', '_created_in_sprintpack') 
    list_display = ['name','sku', 'active', 'complete', 'ean_code', 'available_stock', 'next_available']  
    list_filter = ['umbrella_product__collection', 'umbrella_product__colour', 
        'umbrella_product__umbrella_product_model__product_type', 'product_model__size',  
        'product_model__umbrella_product_model__number', 'complete', 'active']
    inlines = [ProductBillOfMaterialInline]
    search_fields = ['sku',]
    actions = [product_mark_inactive, product_mark_active, print_box_barcode_label, print_washinglabel, print_sample_washinglabel]


class ProductBillOfMaterialAdmin(admin.ModelAdmin):
    readonly_fields = []


admin.site.register(StockLocation, StockLocationAdmin)
admin.site.register(StockLocationMovement)
admin.site.register(Material, MaterialAdmin)
admin.site.register(MaterialDataSheet)
admin.site.register(MaterialImage)
admin.site.register(StockLocationItem, StockLocationItemAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Colour)
admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(ProductModelPattern, ProductModelPatternAdmin)
admin.site.register(UmbrellaProductModel, UmbrellaProductModelAdmin)
admin.site.register(UmbrellaProductModelImage)
admin.site.register(UmbrellaProductModelProductionNote)
admin.site.register(UmbrellaProductModelProductionIssue)
admin.site.register(UmbrellaProduct, UmbrellaProductAdmin)
admin.site.register(UmbrellaProductImage)
admin.site.register(UmbrellaProductBillOfMaterial, UmbrellaProductBillOfMaterialAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductBillOfMaterial, ProductBillOfMaterialAdmin)
