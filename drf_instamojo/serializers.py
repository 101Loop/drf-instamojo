"""
Serializers related to Instamojo API

Use serializer to communicate with instamojo using drf_instamojo
from other apps in Django. Check Examples for reference.

Author: Himanshu Shankar (https://himanshus.com)
"""
import json

from rest_framework import serializers
from rest_framework.exceptions import APIException

from django.utils.text import gettext_lazy as _


class PaymentRequestSerializer(serializers.ModelSerializer):
    """
    Payment Request Serializer. Use for creating payment requests.

    Examples
    --------
    >>> from drf_instamojo.serializers import PaymentRequestSerializer

    Initialize serializer with proper data
    >>> prs = PaymentRequestSerializer(
    >>>     data={'amount': 120.00, 'purpose': 'Test', 'send_sms': False,
    >>>           'redirect_url': 'http://127.0.0.1/api/test/'})

    Check if data is valid
    >>> prs.is_valid(raise_exception=True)

    Save Payment Request by supplying created_by_id or created_by
    created_by_id: ID of a user object
    created_by: User instance
    >>> prs.save(created_by_id=1)

    Finally, use data for further processing.
    >>> prs.data # Contains all the data
    >>> prs.data.get('longurl') # URL where payment needs to completed

    Author: Himanshu Shankar (https://himanshus.com)
    """

    def validate_send_sms(self, value):
        """
        If phone is not supplied, value should be false.

        Parameters
        ----------
        value: bool

        Returns
        -------
        bool

        Raises
        ------
        serializers.ValidationError

        Author: Himanshu Shankar (https://himanshus.com)
        """
        if 'phone' not in self.initial_data and value:
            raise serializers.ValidationError(_("Send SMS should be False "
                                                "if no phone number is "
                                                "given."))
        return value

    def validate_send_email(self, value):
        """
        If email is not supplied, value should be false.

        Parameters
        ----------
        value: bool

        Returns
        -------
        bool

        Raises
        ------
        serializers.ValidationError

        Author: Himanshu Shankar (https://himanshus.com)
        """

        if 'email' not in self.initial_data:
            raise serializers.ValidationError(_("Send Email should be False "
                                                "if no email is given."))
        return value

    def validate(self, attrs):
        """
        Attach configuration with attribute
        Parameters
        ----------
        attrs: dict

        Returns
        -------
        dict

        Author: Himanshu Shankar (https://himanshus.com)
        """

        from .models import InstamojoConfiguration

        try:
            ic = InstamojoConfiguration.objects.get(is_active=True)
        except InstamojoConfiguration.DoesNotExist:
            raise APIException(_("No default configuration present in the "
                                 "system."))
        attrs['configuration'] = ic
        return attrs

    def create(self, validated_data):
        """
        Create payment request with Instamojo server and save proper
        data in database.

        Parameters
        ----------
        validated_data: OrderedDict

        Returns
        -------
        instance

        Author: Himanshu Shankar (https://himanshus.com)
        """
        from instamojo_wrapper import Instamojo

        from django.db.utils import IntegrityError
        from django.contrib.auth import get_user_model

        # Extract configuration (Also, it's not required by
        # instamojo_wrapper)
        ic = validated_data.pop('configuration')

        # Initialize created_by with None (Will raise an error while
        # saving)
        created_by = None

        # Check if created_by or created_by_id is provided. If so,
        # set created_by and remove it from validated_data
        # Again, its not required by instamojo_wrapper
        if 'created_by' in validated_data:
            created_by = validated_data.pop('created_by')
        elif 'created_by_id' in validated_data:
            user_model = get_user_model()
            id = validated_data.pop('created_by_id')
            try:
                created_by = user_model.objects.get(pk=id)
            except user_model.DoesNotExist:
                raise serializers.ValidationError(_(f"User with ID: {id} does "
                                                    "not exists."))

        # Initialize instamojo wrapper
        imojo = Instamojo(api_key=ic.api_key, auth_token=ic.auth_token,
                          endpoint=ic.base_url)

        # Try to create a payment request with processed validated_data
        try:
            response = imojo.payment_request_create(**validated_data)
        except ConnectionError as err:
            raise APIException(_("Server error occurred while creating "
                                 "payment request with Instamojo: {err}"
                                 .format(err=str(err))))

        if not response['success']:
            raise APIException(_("Server error occurred while creating "
                                 "payment request with Instamojo: {err}"
                                 .format(err=str(response['message']))))

        # Make a copy of successful payment_request
        data = response['payment_request'].copy()

        # Set created_by and configuration again
        if created_by:
            data['created_by'] = created_by
        data['configuration'] = ic

        # Create json dump of original response
        data['instamojo_raw_response'] = json.dumps(response)

        # Call super function to save data
        try:
            return super(PaymentRequestSerializer, self).create(
                validated_data=data)

        # Saving may throw error related to created_by, handle it and
        # throw APIException as this needs to handled at coding level
        # while calling .save()
        except IntegrityError as err:
            raise APIException(_("Server error: {}".format(str(err))))

    class Meta:
        from .models import PaymentRequest

        model = PaymentRequest
        fields = ('id', 'amount', 'purpose', 'buyer_name', 'email', 'phone',
                  'redirect_url', 'webhook', 'allow_repeated_payments',
                  'send_email', 'send_sms', 'expires_at',

                  'email_status', 'sms_status', 'shorturl', 'status',
                  'instamojo_raw_response', 'longurl', 'is_enabled')
        read_only_fields = ('id', 'email_status', 'sms_status', 'shorturl',
                            'status', 'instamojo_raw_response', 'longurl',
                            'is_enabled')


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer used to add a payment record

    This will trigger payment_record_handler which will check for other
    payment records, check if payment request is completed and will
    trigger payment_done signal.

    Example
    -------
    >>> from drf_instamojo.serializers import PaymentSerializer
    >>> from drf_instamojo.models import InstamojoConfiguration

    >>> from instamojo_wrapper import Instamojo

    Get the active Instamojo Configuration
    >>> ic = InstamojoConfiguration.objects.get(is_active=True)

    Create an Instamojo object (from instamojo_wrapper)
    >>> imojo = Instamojo(api_key=ic.api_key, auth_token=ic.auth_token,
    >>>                   endpoint=ic.base_url)

    Initialize serializer with proper data
    >>> ps = PaymentSerializer(data={'id': 'PAYMENT_ID',
    >>>                              'payment_request': 'PAYMENT_REQUEST_ID'})

    Validate Payment Serializer
    >>> ps.is_valid(raise_exception=True)

    Save Payment record
    >>> ps.save()
    If payment is completed, payment_done signal will be triggered.

    Author: Himanshu Shankar (https://himanshus.com)
    """
    def validate(self, attrs):
        """
        Validates the payment ID from Instamojo Server
        Parameters
        ----------
        attrs: dict

        Returns
        -------
        data: dict

        Author: Himanshu Shankar (https://himanshus.com)
        """

        from instamojo_wrapper import Instamojo

        from .models import PaymentRequest, InstamojoConfiguration

        # Initialize required variables
        pr: PaymentRequest = attrs.get('payment_request')
        ic: InstamojoConfiguration = pr.configuration

        imojo = Instamojo(api_key=ic.api_key, auth_token=ic.auth_token,
                          endpoint=ic.base_url)

        # Try to fetch payment status
        try:
            response = imojo.payment_request_payment_status(
                id=pr.id, payment_id=attrs.get('id'))
        except ConnectionError as err:
            err = str(err)
            raise APIException(_(f"Server error occurred while getting "
                                 f"payment status from Instamojo: {err}"))
        if not response['success']:
            # Instamojo server returned with False success flag.
            raise serializers.ValidationError(_("Could not validate payment!"))

        # Initialize data with payment information
        data = response['payment_request']['payment'].copy()

        # Set variables as per model
        data['id'] = data.pop('payment_id')
        data['instamojo_raw_response'] = json.dumps(response)
        data['payment_request'] = pr

        # Extract and set failure variables as per model
        if 'failure' in data and data.get('failure'):
            data['failure_reason'] = data.get('failure').get('reason')
            data['failure_message'] = data.get('failure').get('message')

        # Convert possible non-str data to str as per model fields
        non_str_fields = ('payment_request', )

        for k, v in data.copy().items():

            # If key is not in fields, delete it
            if k not in self.Meta.fields:
                del data[k]

            # If key is not a non-string field and is not None and is
            # not an instance of string, convert it to string
            elif k not in non_str_fields and v and not isinstance(v, str):
                data[k] = str(v)

        # Return data
        return data

    class Meta:
        from .models import Payment

        model = Payment
        fields = ('id', 'instamojo_raw_response', 'payment_request', 'mac',
                  'status', 'fees', 'currency', 'affiliate_commission',
                  'amount', 'buyer_name', 'buyer_email', 'buyer_phone',
                  'shipping_address', 'shipping_city', 'shipping_state',
                  'shipping_country', 'shipping_zip', 'quantity', 'payout',
                  'unit_price', 'instrument_type', 'billing_instrument',
                  'tax_invoice_id', 'failure_message', 'failure_reason',
                  'webhook_verified')
        read_only_fields = ('instamojo_raw_response',
                            'status', 'fees', 'currency', 'buyer_phone',
                            'affilite_commission', 'mac', 'shipping_state',
                            'amount', 'buyer_name', 'buyer_email', 'payout',
                            'shipping_address', 'shipping_city',
                            'shipping_country', 'shipping_zip', 'quantity',
                            'unit_price', 'instrument_type', 'failure_reason',
                            'webhook_verified', 'tax_invoice_id',
                            'billing_instrument', 'failure_message')
