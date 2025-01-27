from random import choices

from django.db import models
from django.db.models import PROTECT

from apps.Login.models import Usuario


# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=30, verbose_name='Categoria')
    descripcion = models.CharField(max_length=150, verbose_name='Descripcion')
    estado = models.BooleanField(default=True, verbose_name='Estado')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.categoria


class Autor(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Nombre')
    descripcion = models.CharField(max_length=150, verbose_name='Descripción')
    estado = models.BooleanField(default=True, verbose_name='Estado')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autors'

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    class Condicion(models.TextChoices):
        DISPONIBLE = ('Disponible', 'Disponible')
        SIN_EJEMPLARES = ('Sin Ejemplares', 'Sin Ejemplares')

    categoria = models.ForeignKey(Categoria,on_delete=PROTECT, verbose_name='Categoría')
    autor = models.ForeignKey(Autor,on_delete=PROTECT, verbose_name='Autor')
    titulo = models.CharField(max_length=120, verbose_name='Titulo')
    descripcion = models.CharField(max_length=150, verbose_name='Descripción')
    isbn = models.CharField(max_length=20, verbose_name='ISBN', null=True, blank=True)
    fecha_publicacion = models.DateField(verbose_name='Fecha Publicación')
    portada = models.ImageField(upload_to='libros/', verbose_name='Portada', null=True, blank=True)
    ejemplares = models.IntegerField(verbose_name='Ejemplares')
    recomendaciones = models.PositiveIntegerField(verbose_name='Recomendaciones', default=0)
    condicion = models.CharField(
        max_length=20,
        choices=Condicion.choices,
        default=Condicion.DISPONIBLE,
        verbose_name='Condición'
    )
    estado = models.BooleanField(default=True, verbose_name='Estado')

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return f'{self.titulo} {self.autor.nombre}'

    def save(self, *args, **kwargs):
        if self.ejemplares == 0:
            self.condicion = self.Condicion.SIN_EJEMPLARES
        else:
            self.condicion = self.Condicion.DISPONIBLE
        super().save(*args, **kwargs)


class Recomendacion(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=PROTECT, verbose_name='Usuario')
    libro = models.ForeignKey(Libro,on_delete=PROTECT, verbose_name='Libro')
    fecha_recomendacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Recomendacion'
        verbose_name_plural = 'Recomendaciones'
        unique_together = (('usuario', 'libro'),)

    def __str__(self):
        return f'{self.usuario.first_name} {self.usuario.last_name} recomendó {self.libro.titulo}'