# Instamojo | Django REST Framework

**A package for Instamojo integration in Django REST Framework**<br>

`Instamojo | Django REST Framework` is a Django packaged app that provides necessary `views` based in Django REST 
Framework. It enables easy integration of Instamojo Payment Gateway with Web/Mobile Application with a RESTful API 
based server.

Contributors: **WE'RE LOOKING FOR SOMEONE WHO CAN CONTRIBUTE IN DOCS**
- **[Civil Machines Technologies Private Limited](https://github.com/civilmahines)**: For providing me platform and
funds for research work. This project is hosted currently with `CMT` only. 
- **[Himanshu Shankar](https://github.com/iamhssingh)**: Himanshu Shankar has initiated this project and worked on this
project to collect useful functions and classes that are being used in various projects.

#### Installation

- Download and Install via `pip`
```
pip install drf_instamojo
```
or<br>
Download and Install via `easy_install`
```
easy_install drf_instamojo
```
- Add, if wanted, `drfaddons` in `INSTALLED_APPS` (This is although not required!)
```
INSTALLED_APPS = [
    ...
    'drf_instamojo',
    ...
]
```
- Also add other dependencies in `INSTALLED_APPS`<br>
```
INSTALLED_APPS = [
    ...
    'drfaddons',
    ...
]
```
- Include urls of `drf_instamojo` in `urls.py`
```
urlpatterns = [
    ...
    path('api/instamojo/', include('drf_instamojo.urls')),
    ...
]

# or

urlpatterns = [
    ...
    url(r'^api/instamojo/', include('drf_instamojo.urls')),
    ...
]
```
- Run migrate command:
```
python manage.py migrate
```

### MODELS
The application has three models:

- `InstamojoConfiguration`: You need to define your Instamojo configurations in this model. Only one object can have
`is_active` set to `True` which will be used with Instamojo API.
- `PaymentRequest`: This will contain all the Instamojo Payment Request that one will create with Instamojo.
- `Payment`: This will contain all the responses received from Instamojo API against payment.

### VIEWS
The application has following views:

- `ListAddPaymentRequestView`: All payment request should be made on this view. Requires a logged in user.
It'll provide user with required data, including `longurl` that will be used to make payment.
- `ListAddPaymentView`: All response data should be posted on this view. Doesn't requires a logged in user.

### URLS
- `request/`: All payment request to be made via this URL.
- `payment/`: All payment reponses to be posted on this URL.

### Quickstart Guide

- Complete `Installation Steps` (mentioned above)
- Create a configuration via `Django Admin` in `Instamojo Configuration`
- Set `is_active` to `True`
- Note: Use sandbox mode credential at first

### How to integrate with apps

- Use `serializers` to integrate with custom apps.

#### Creating Payment Request
##### Example
- Create a view: `PaymentView`
- Use `PaymentRequestSerializer` to create a payment request.
- Check example code in `serializers.py`:
```
# Initialize serializer with proper data
prs = PaymentRequestSerializer(data={'amount': 120.00, 'purpose': 'Test', 'send_sms': False,
                                     'redirect_url': 'http://127.0.0.1/api/test/'})

# Check if data is valid
prs.is_valid(raise_exception=True)

instance = prs.save(created_by=user)
```
- Save `instance` as foreign key in app pointing to bill for which the payment request is made.
- Return `longurl` to client for making payment

##### Problem with created_by requirement in .save() of serializer
- If app doesn't require user to login, use following logic: 
    - Inside payment view, take following data from user:
        - Name of the customer
        - Mobile Number of the customer `mobile: 9987987345`
        - Email of the customer `email: test@abc.com`
    - Use following code to create a logic around getting an existing or creating a new user:
```
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

```
- Otherwise, simply use `user = request.user` as user while calling `.save()` on serializer.
- *Bonus Pointer*: Check out **[Django REST Framework - User](https://github.com/101loop/drf-user/)**

#### Payment Completion
- Use `payment_done` signal
- Create `signals` python directory with `__init__.py, handlers.py` in app
- In `handlers.py`, create a function for handling `payment_done` signal
```
from django.dispatch import receiver

from drf_instamojo.models import PaymentRequest
from drf_instamojo.signals import payment_done


@receiver(signal=payment_done, sender=PaymentRequest)
def payment_done_handler(instance: PaymentRequest, sender, *args, **kwargs):
    ...
    # Payment completed
    # bill.paid()
    # item.dispatch()
    ...
```
