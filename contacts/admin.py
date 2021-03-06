from django.contrib import admin
from defaults.admin import DefaultInline, DefaultAdmin

from .models import Relation, RelationAddress, OwnAddress, Agent, AgentCommission
from .helpers import print_address_label, export_datafile_for_customer, \
	export_datafile_for_customer_inactive_only, export_pricelist_for_customer

### Inlines ###

class AgentCommissionInline(DefaultInline):
    model = AgentCommission

### Admins ###

class AgentAdmin(DefaultAdmin):
    inlines = [AgentCommissionInline]

class AgentCommissionAdmin(DefaultAdmin):
    pass

class RelationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'contact_full_name', 'contact_phone')
    list_filter = ['is_supplier', 'is_client', 'country', 'agent']
    actions = [print_address_label, export_datafile_for_customer, \
    	export_datafile_for_customer_inactive_only, export_pricelist_for_customer]

class OwnAddressAdmin(admin.ModelAdmin):
    actions = [print_address_label]

admin.site.register(Agent, AgentAdmin)
admin.site.register(AgentCommission, AgentCommissionAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(OwnAddress, OwnAddressAdmin)
admin.site.register(RelationAddress)