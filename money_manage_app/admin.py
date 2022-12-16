from django.contrib import admin

from donation_app.models import OutsideDonation

from .models import Bill, Prices, Receipt


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
