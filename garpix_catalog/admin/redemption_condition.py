from django.contrib import admin
from ..models import RedemptionCondition, SizeRangePack, Minimum, Pack
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter


class RedemptionConditionChildAdmin(PolymorphicChildModelAdmin):
    base_model = RedemptionCondition
    exclude = ['rc_type', ]


@admin.register(SizeRangePack)
class SizeRangePackAdmin(RedemptionConditionChildAdmin):
    base_model = SizeRangePack


@admin.register(Minimum)
class MinimumAdmin(RedemptionConditionChildAdmin):
    base_model = Minimum


@admin.register(Pack)
class PackAdmin(RedemptionConditionChildAdmin):
    base_model = Pack


@admin.register(RedemptionCondition)
class RedemptionConditionParentAdmin(PolymorphicParentModelAdmin):
    base_model = RedemptionCondition
    child_models = (SizeRangePack, Minimum, Pack)
    list_filter = (PolymorphicChildModelFilter,)
    list_display = ['__str__', 'rc_type']
    exclude = ['rc_type', ]
