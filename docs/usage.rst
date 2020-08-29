=====
Usage
=====

Describes how to use ``drf_instamojo`` when it is installed and configured.

* Create a configuration via Django Admin in Instamojo Configuration
* Set ``is_active`` to True
* **Note**: Use sandbox mode credentials during local development


Integration With Apps
=====================

Use ``serializers`` to integrate with your custom apps.

Creating Payment Request
------------------------

* Create a view: PaymentView
* Use PaymentRequestSerializer to create a payment request.
* Check example code in serializers.py:

.. code-block:: python

    # serializers.py

    # Initialize serializer with proper data
    prs = PaymentRequestSerializer(data={'amount': 120.00, 'purpose': 'Test', 'send_sms': False,
                                        'redirect_url': 'http://127.0.0.1/api/test/'})

    # Check if data is valid
    prs.is_valid(raise_exception=True)

    instance = prs.save(created_by=user)


* Save instance as foreign key in app pointing to bill for which the payment request is made.
* Return longurl to client (instamojo) for making payment


Problems with .save() method
----------------------------

* **Note**: ``created_by`` is required in .save() serializer to link instance with user

* If app doesn't require user to login, use following logic:
    - Inside payment view, take following data from user:
       + Name of the customer: ``random_name``
       + Mobile Number of the customer mobile: ``1234567890``
       + Email of the customer email: ``test@abc.com``
    - Use following code to create a logic around getting an existing or creating a new user:

.. code-block:: python

    # example.py

    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    try:
        user = user_model.objects.get(email=email)
    except user_model.DoesNotExist:
        try:
            user = user_model.objects.get(mobile=mobile)
        except user_model.DoesNotExist:
            # Now you're dead sure that user does not exists.
            user = user_model.objects.create(name=name, mobile=mobile, email=email, password="RANDOM_PASSWORD")


* Otherwise, simply use user = request.user while calling .save() on serializer.
* Bonus Pointer: Check out our library for managing users, `Django REST Framework - User`_

.. _Django REST Framework - User: https://github.com/101loop/drf-user/


Payment Completion
------------------


* Use ``payment_done`` signal
* Create ``signals`` python directory with ``__init__.py, handlers.py`` in app
* In ``handlers.py``, create a function for handling ``payment_done`` signal
* For more info, see :ref:`extras-signals`

.. code-block:: python

    # handlers.py

    from django.dispatch import receiver

    from drf_instamojo.models import PaymentRequest
    from drf_instamojo.signals import payment_done


    @receiver(signal=payment_done, sender=PaymentRequest)
    def payment_done_handler(instance: PaymentRequest, sender, *args, **kwargs):
        ...
        # Your logic for handling payments
        # Payment completed
        # bill.paid()
        # item.dispatch()
        ...
