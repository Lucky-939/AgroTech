from django.apps import AppConfig
<<<<<<< HEAD
import threading
=======

>>>>>>> 05f56bc7 (Initial commit for AgroTech)

class DiseaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'disease'
<<<<<<< HEAD

    def ready(self):
        # Warm up the model in a background thread so it doesn't block server start
        # This makes the first detection instant instead of taking 10+ seconds
        from .cnn_model import _get_model
        # Use threading to avoid double-loading issues with runserver's StatReloader
        threading.Thread(target=_get_model, daemon=True).start()
=======
>>>>>>> 05f56bc7 (Initial commit for AgroTech)
