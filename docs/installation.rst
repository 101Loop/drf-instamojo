============
Installation
============

Each of the following steps needs to be configured for the `drf instamojo` to be fully functional.

Getting the code
----------------

Install from PyPI (recommended) with ``pip``::

    pip install drf_instamojo

Or Install via ``easy_install``::

    pip install drf_instamojo

Or Install from ``source code``::

    pip install -e git+https://github.com/101Loop/drf-instamojo#egg=drf_instamojo


Prerequisites
-------------

Add ``drf_instamojo`` to your INSTALLED_APPS setting and Add, if wanted, `drfaddons`_ in INSTALLED_APPS (This is although not required!):

.. _drfaddons: https://github.com/101loop/drfaddons

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'drf_instamojo',
        'drfaddons',
        ...
    ]

Setting up URLconf
------------------

Add ``drf_instamojo's`` URLs to your project’s URLconf as follows:

.. code-block:: python

    from django.urls import path

    urlpatterns = [
        ...
        path('api/instamojo/', include('drf_instamojo.urls')),
        ...
    ]

    # or

    from django.urls import re_path

    urlpatterns = [
        ...
        re_path(r'^api/instamojo/', include('drf_instamojo.urls')),
        ...
    ]


Sync Database
-------------

Run migrate command:

.. code-block:: python

    python manage.py migrate
