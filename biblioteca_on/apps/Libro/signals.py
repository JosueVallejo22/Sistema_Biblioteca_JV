from django.db.models.signals import post_save
from django.dispatch import receiver
"""from .models import Ejemplar, Libro

@receiver(post_save, sender=Ejemplar)
def actualizar_ejemplar(sender, instance, created, **kwargs):
    if created:
        libro = instance.id_libro

        cantidad_ejemplares = Ejemplar.objects.filter(id_libro=libro).count()
        libro.ejemplares = cantidad_ejemplares
        libro.save()"""