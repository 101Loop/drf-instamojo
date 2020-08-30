"""
App Config for DrfInstamojo
"""
from django.apps import AppConfig


class DrfInstamojoConfig(AppConfig):
    """Base AppConfig for DrfInstamojoConfig"""

    name = "drf_instamojo"
    verbose_name = "Instamojo | Django REST Framework"

    def ready(self):
        """
        Registers all signal handler
        Returns
        -------
        None
        """
        from .signals.handlers import payment_completed_handler  # noqa
        from .signals.handlers import payment_record_handler  # noqa

        super(DrfInstamojoConfig, self).ready()
