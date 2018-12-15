"""
Models for Instamojo Application

Author: Himanshu Shankar (https://himanshus.com)
"""

from django.db import models
from django.utils.text import gettext_lazy as _

from drfaddons.models import CreateUpdateModel


class InstamojoConfiguration(CreateUpdateModel):
    """
    Represents Instamojo's configurations.

    Only one of the configuration can have is_active set to True.

    Author: Himanshu Shankar (https://himanshus.com)
    """
    api_key = models.CharField(verbose_name=_("Private API Key"),
                               max_length=48, unique=True)
    auth_token = models.CharField(verbose_name=_("Private Auth Token"),
                                  max_length=48, unique=True)
    salt = models.CharField(verbose_name=_("Private Salt"), max_length=48,
                            unique=True)
    is_active = models.BooleanField(verbose_name=_("Is Active?"),
                                    default=False)
    base_url = models.URLField(verbose_name=_("API Based URL"),
                               default="https://www.instamojo.com/api/1.1/")

    def __str__(self):
        return str(self.api_key)

    def clean_fields(self, exclude=None):
        """
        Used to validate the value of is_active
        Parameters
        ----------
        exclude: list of fields that is to be excluded while checking

        Returns
        -------
        None

        Raises
        ------
        ValidationError: for is_active field.

        Author: Himanshu Shankar (https://himanshus.com)
        """
        from django.core.exceptions import ValidationError

        if 'is_active' not in exclude:
            try:
                ic = InstamojoConfiguration.objects.get(is_active=True)
            except InstamojoConfiguration.DoesNotExist:
                pass
            except InstamojoConfiguration.MultipleObjectsReturned:
                raise ValidationError(
                    {'is_active': _("Multiple configuration is active. Keep "
                                    "only 1 configuration active at a time.")})
            else:
                if ic.api_key is not self.api_key:
                    raise ValidationError(
                        {'is_active': _("Another configuration is active. "
                                        "Deactivate it first.")})
        super(InstamojoConfiguration, self).clean_fields(exclude=exclude)

    class Meta:
        verbose_name = _("Instamojo Configuration")
        verbose_name_plural = _("Instamojo Configurations")


class PaymentRequest(CreateUpdateModel):
    """
    Represents an instamojo payment request

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .variables import SENT_STATUS_CHOICES, STATUS_CHOICES, PENDING

    id = models.CharField(verbose_name=_('Payment Request ID'), max_length=254,
                          primary_key=True)
    amount = models.DecimalField(verbose_name=_('Amount'), decimal_places=2,
                                 max_digits=10)
    purpose = models.CharField(verbose_name=_('Purpose'), max_length=254)

    buyer_name = models.CharField(verbose_name=_("Buyer Name"), max_length=254,
                                  null=True, blank=True)
    email = models.EmailField(verbose_name=_("Buyer Email"), max_length=254,
                              null=True, blank=True)
    phone = models.CharField(verbose_name=_("Buyer Mobile"), max_length=15,
                             null=True, blank=True)

    send_email = models.BooleanField(verbose_name=_("Send Mail?"),
                                     default=False)
    send_sms = models.BooleanField(verbose_name=_("Send SMS?"), default=False)

    email_status = models.CharField(verbose_name=_("Email Sent Status"),
                                    max_length=48,
                                    choices=SENT_STATUS_CHOICES,
                                    null=True, blank=True)
    sms_status = models.CharField(verbose_name=_("SMS Sent Status"),
                                  max_length=48, choices=SENT_STATUS_CHOICES,
                                  null=True, blank=True)

    redirect_url = models.URLField(verbose_name=_('Redirect URL'))
    webhook = models.URLField(verbose_name=_('Webhook URL'), null=True,
                              blank=True)

    allow_repeated_payments = models.BooleanField(
        verbose_name=_('Allow Repeated Payment'), default=True)

    instamojo_raw_response = models.TextField(
        verbose_name=_('Payment Request Raw Response'), null=True, blank=True)

    longurl = models.URLField(verbose_name=_('Long URL'))
    shorturl = models.URLField(verbose_name=_('Long URL'), null=True,
                               blank=True)

    expires_at = models.CharField(verbose_name=_('Expires at'), max_length=30,
                                  blank=True, null=True)
    status = models.CharField(verbose_name=_('Status'), max_length=10,
                              choices=STATUS_CHOICES, default=PENDING)

    configuration = models.ForeignKey(to=InstamojoConfiguration,
                                      verbose_name=_("Instamojo Config"),
                                      on_delete=models.PROTECT)

    is_enabled = models.BooleanField(verbose_name=_("Is Enabled?"),
                                     default=True)

    customer_id = models.CharField(verbose_name=_("Customer ID"),
                                   max_length=254, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_("Created At by "
                                                     "Instamojo"),
                                      blank=True, null=True)
    modified_at = models.DateTimeField(verbose_name=_("Updated At by "
                                                      "Instamojo"),
                                       blank=True, null=True)

    class Meta:
        verbose_name = _('Payment Request')
        verbose_name_plural = _('Payment Request')

    def __str__(self):
        return self.id


class Payment(models.Model):
    """
    Represents an Instamojo payment

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from .variables import PAYMENT_STATUS_CHOICES

    id = models.CharField(verbose_name=_('Payment ID'), max_length=254,
                          primary_key=True)

    instamojo_raw_response = models.TextField(
        null=True, blank=True, verbose_name=_('Payment Raw Response'))

    payment_request = models.ForeignKey(to=PaymentRequest,
                                        on_delete=models.PROTECT,
                                        verbose_name=_("Payment Request"))
    mac = models.CharField(verbose_name=_('Message Authentication Code'),
                           null=True, blank=True, max_length=154)

    status = models.CharField(verbose_name=_('Status'), max_length=12,
                              choices=PAYMENT_STATUS_CHOICES)

    fees = models.DecimalField(verbose_name=_('Fees by Instamojo'), blank=True,
                               decimal_places=3, null=True, max_digits=10)
    affiliate_commission = models.DecimalField(_('Affiliate Commission'),
                                               max_digits=10, blank=True,
                                               decimal_places=3, null=True)
    currency = models.CharField(verbose_name=_('Currency'), null=True,
                                max_length=50, blank=True)
    amount = models.DecimalField(verbose_name=_('Amount'), decimal_places=2,
                                 max_digits=10)

    buyer_name = models.CharField(verbose_name=_("Buyer Name"),
                                  null=True, blank=True, max_length=254)
    buyer_email = models.EmailField(verbose_name=_("Buyer Email"),
                                    null=True, blank=True, max_length=254)
    buyer_phone = models.CharField(verbose_name=_("Buyer Mobile"),
                                   null=True, blank=True, max_length=15)

    shipping_address = models.CharField(verbose_name=_("Shipping Address"),
                                        max_length=255, null=True, blank=True)
    shipping_city = models.CharField(verbose_name=_("Shipping City"),
                                     max_length=255, null=True, blank=True)
    shipping_state = models.CharField(verbose_name=_("Shipping State"),
                                      max_length=255, null=True, blank=True)
    shipping_country = models.CharField(verbose_name=_("Shipping Country"),
                                        max_length=255, null=True, blank=True)
    shipping_zip = models.CharField(verbose_name=_("Shipping ZIP"),
                                    max_length=255, null=True, blank=True)

    quantity = models.DecimalField(verbose_name=_("Quantity"),
                                   decimal_places=2, max_digits=5,
                                   null=True, blank=True)
    unit_price = models.DecimalField(verbose_name=_('Unit Price'),
                                     decimal_places=2,
                                     max_digits=10, null=True, blank=True)

    instrument_type = models.CharField(verbose_name=_("Instrument Type"),
                                       null=True, blank=True, max_length=64)
    billing_instrument = models.CharField(verbose_name=_("Billing Instrument"),
                                          null=True, blank=True, max_length=64)
    tax_invoice_id = models.CharField(verbose_name=_("Tax Invoice ID"),
                                      null=True, blank=True, max_length=64)
    failure_message = models.CharField(verbose_name=_("Failure Message"),
                                       null=True, blank=True, max_length=255)
    failure_reason = models.CharField(verbose_name=_("Failure Reason"),
                                      null=True, blank=True, max_length=127)
    payout = models.CharField(verbose_name=_("Payout"), null=True, blank=True,
                              max_length=255)

    webhook_verified = models.BooleanField(verbose_name=_("Verified via "
                                                          "WebHook?"),
                                           default=False)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = _('Instamojo Payment')
        verbose_name_plural = _('Instamojo Payment')
