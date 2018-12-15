from django.apps import AppConfig


class DrfInstamojoConfig(AppConfig):
    name = 'drf_instamojo'
    verbose_name = 'Instamojo | Django REST Framework'

    def ready(self):
        """
        Registers all signal handler
        Returns
        -------
        None
        """
        from .signals.handlers import payment_completed_handler
        from .signals.handlers import payment_record_handler

        super(DrfInstamojoConfig, self).ready()
