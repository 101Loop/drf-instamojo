.. drf-instamojo documentation master file, created by
   sphinx-quickstart on Sun Aug 23 14:06:10 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=========================================
Welcome to drf-instamojo's documentation!
=========================================

A package for Instamojo integration in Django REST Framework.
Based on `Instamojo Wrapper`_ by `Instamojo`_.

.. _Instamojo Wrapper: https://github.com/Instamojo/instamojo-py
.. _Instamojo: https://github.com/Instamojo

========
Overview
========

``Instamojo | Django REST Framework`` is a Django packaged app that provides necessary views based in Django REST Framework.
It enables easy integration of Instamojo Payment Gateway with Web/Mobile Application with a RESTful API based server.


.. |check_| raw:: html

    <input checked=""  disabled="" type="checkbox">

.. |uncheck_| raw:: html

    <input disabled="" type="checkbox">

============
Feature List
============

|check_| Create Payment Request

|check_| Handle Payment Record

|check_| Verify payment record from Instamojo Server

|check_| Update payment request from Instamojo Server

|check_| Dispatch payment_done signal for external app integration

|uncheck_| Webhook for server-to-server payment record

|uncheck_| Raise refund

|uncheck_| Update refund status

|uncheck_| Dispatch refund_done signal

========
Contents
========

.. toctree::
   :maxdepth: 3

   installation
   configuration
   usage

.. toctree::
    :maxdepth: 2

    extras/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
