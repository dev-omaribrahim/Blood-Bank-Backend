from django.contrib import admin
from .models import Bill, Receipt, Prices
from donation_app.models import OutsideDonation


class ReceiptStackedAdmin(admin.StackedInline):
    model = OutsideDonation
    fields = ("receipt",)
    fk_name = "receipt"
    extra = 0


class ReceiptAdmin(admin.ModelAdmin):
    inlines = [ReceiptStackedAdmin]


admin.site.register(Bill)
admin.site.register(Prices)
admin.site.register(Receipt, ReceiptAdmin)
