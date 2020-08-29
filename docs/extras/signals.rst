.. _extras-signals:

=======
Signals
=======
This page helps you to setup Django Signals in your project.

Directory Structure
-------------------
* We are assuming your app structure would be something like this::

    myapp
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py

* To use signals in your project, there are various methods. Method shown below is just one of them.
    * Add signals directory and add ``__init__.py & handlers.py`` file in your app directory like this::

        myapp
        ├── admin.py
        ├── apps.py
        ├── __init__.py
        ├── migrations
        │   └── __init__.py
        ├── models.py
        ├── signals
        │   ├── handlers.py
        │   └── __init__.py
        ├── tests.py
        └── views.py

    * You can write your custom logic in ``handlers.py``. Check out Django docs for more info on `Signals`_.

    .. _Signals: https://docs.djangoproject.com/en/dev/topics/signals/

    * In your ``myapp/app.py`` file import your signals like this:

    .. code-block:: python

        from django.apps import AppConfig


        class MyappConfig(AppConfig):
            name = 'myapp'

            def ready(self):
                from .signals.handlers import your_signal_name

    * Add ``default_app_config`` in your app's ``__init__.py`` file.

    .. code-block:: python

        default_app_config = 'myapp.apps.MyappConfig'

    * **Note:** The ``myapp/__init__.py`` bits are not required if you are already referring to your AppConfig in the INSTALLED_APPS settings.


* For other method to setup signals with your django project checkout this article on `How to create Django Signals`_.

.. _How to create Django Signals: https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
