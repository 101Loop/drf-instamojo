import django.dispatch


payment_done = django.dispatch.Signal(providing_args=['instance'])
