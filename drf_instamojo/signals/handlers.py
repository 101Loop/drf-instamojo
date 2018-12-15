from django.db.models.signals import post_save

from django.dispatch import receiver

from drf_instamojo.models import Payment, PaymentRequest
from drf_instamojo.signals import payment_done


@receiver(signal=post_save, sender=Payment)
def payment_record_handler(instance: Payment, sender, **kwargs):
    """
    Each time a payment record is saved, signal will check and update
    other payment records and payment request.
    :param instance: Instance that is being saved
    :param sender: Payment model
    :param kwargs: other parameters
    :return: None
    """
    from drf_instamojo.serializers import PaymentSerializer

    from instamojo_wrapper import Instamojo

    pr: PaymentRequest = instance.payment_request

    imojo = Instamojo(api_key=pr.configuration.api_key,
                      auth_token=pr.configuration.auth_token,
                      endpoint=pr.configuration.base_url)

    pr_status = imojo.payment_request_status(id=pr.id)

    # Check if payment status request is successful
    if pr_status.get('success'):
        payment_request_imojo = pr_status.get('payment_request')

        if payment_request_imojo.get('modified_at') > pr.modified_at:
            # Update payment request
            pr.status = payment_request_imojo.get('status')
            pr.modified_at = payment_request_imojo.get('modified_at')
            pr.sms_status = payment_request_imojo.get('sms_status')
            pr.email_status = payment_request_imojo.get('email_status')
            pr.save()

        # Save other payment details, if not already saved.
        # This may trigger more signals.
        # TODO: Check if there is any better way to do this.
        for payment in payment_request_imojo.get('payments'):
            id = payment.get('payment_id')
            try:
                Payment.objects.get(id=payment.get('payment_id'))
            except Payment.DoesNotExist:
                ps = PaymentSerializer(data={'id': id,
                                             'payment_request': pr.id})
                ps.is_valid(raise_exception=True)
                ps.save()


@receiver(signal=post_save, sender=PaymentRequest)
def payment_completed_handler(instance: PaymentRequest,
                              sender, **kwargs):
    """
    Checks if payment is completed and triggers payment_done signal.
    :param instance: PaymentRequest instance
    :param sender: PaymentRequest
    :param kwargs: Other params
    :return: None

    Author: Himanshu Shankar (https://himanshus.com)
    """

    from drf_instamojo.variables import COMPLETED

    if instance.status == COMPLETED:
        payment_done.send(sender=sender, instance=instance)
