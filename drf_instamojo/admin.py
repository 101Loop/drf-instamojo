"""
Admin interfaces for models.

Author: Himanshu Shankar (https://himanshus.com)
"""
from django.contrib import admin
from drfaddons.admin import CreateUpdateAdmin

from drf_instamojo.models import InstamojoConfiguration
from drf_instamojo.models import Payment
from drf_instamojo.models import PaymentRequest


class InstamojoConfigurationAdmin(CreateUpdateAdmin):
    """
    Admin interface for InstamojoConfiguration

    Author: Himanshu Shankar (https://himanshus.com)
    """

    list_display = ("id", "api_key", "is_active")
    search_fields = ("auth_token", "api_key")


class PaymentRequestAdmin(CreateUpdateAdmin):
    """
    Admin interface for Payment Request model.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    list_display = ("id", "amount", "purpose", "status", "created_by", "is_enabled")
    search_fields = ("id", "amount", "purpose")
    list_filter = ("status", "is_enabled")

    def has_add_permission(self, request):
        """Did PaymentRequestAdmin has add permission enabled"""

        return False

    def has_change_permission(self, request, obj=None):
        """Did PaymentRequestAdmin has change permission enabled"""

        return False


class PaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for Payments.

    Author: Himanshu Shankar (https://himanshus.com)
    """

    list_display = (
        "id",
        "status",
        "amount",
        "currency",
    )
    search_fields = ("id",)
    list_filter = ("status", "payment_request")

    def has_add_permission(self, request):
        """Did PaymentRequestAdmin has add permission enabled"""

        return False

    def has_change_permission(self, request, obj=None):
        """Did PaymentRequestAdmin has change permission enabled"""

        return False


admin.site.register(InstamojoConfiguration, InstamojoConfigurationAdmin)
admin.site.register(PaymentRequest, PaymentRequestAdmin)
admin.site.register(Payment, PaymentAdmin)
