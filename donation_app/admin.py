from django.contrib import admin
from .models import (
    InsideDonation, OutsideDonation, ReplaceDonation,
    DonorProfile, InstituteProfile, Derivation
)


class DerivationInline(admin.StackedInline):
    """
    used for display parent field in more readable way
    """
    model = Derivation
    extra = 0
    fk_name = "child"


class InsideDonationAdmin(admin.ModelAdmin):
    inlines = (DerivationInline,)


admin.site.register(InsideDonation, InsideDonationAdmin)
admin.site.register(OutsideDonation)
admin.site.register(ReplaceDonation)
admin.site.register(DonorProfile)
admin.site.register(InstituteProfile)
