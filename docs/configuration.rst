=============
Configuration
=============

Configuration about how ``drf_instamojo`` is working.


Models
------

The application has three models:

* ``InstamojoConfiguration``: You need to define your Instamojo configurations in this model. Only one object can have is_active set to True which will be used with Instamojo API.

* ``PaymentRequest``: This will contain all the Instamojo Payment Request that one will create with Instamojo.

* ``Payment``: This will contain all the responses received from Instamojo API against payment.


Views
-----

The application has following views:

* ``ListAddPaymentRequestView``: All payment request should be made on this view. Requires a logged in user. It'll provide user with required data, including ``longurl`` that will be used to make payment.

* ``ListAddPaymentView``: All response data should be posted on this view. Doesn't requires a logged in user.


Urls
----

* ``request/``: All payment request to be made via this URL.
* ``payment/``: All payment reponses to be posted on this URL.
