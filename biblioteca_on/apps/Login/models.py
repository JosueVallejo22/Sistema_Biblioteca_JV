from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.


class Usuario(AbstractUser):
    class Condicion(models.TextChoices):
        HABILITADO = 'Habilitado', 'Habilitado'
        SUSPENDIDO = 'Suspendido', 'Suspendido'
        BLOQUEADO = 'Bloqueado', 'Bloqueado'

    dni = models.CharField(max_length=10, verbose_name="DNI")
    telefono = models.CharField(max_length=10, verbose_name="Teléfono")
    direccion = models.CharField(max_length=20, verbose_name="Dirección")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil' ,verbose_name="Foto Perfil", null=True, blank=True)
    condicion = models.CharField(max_length=20,
                                 choices=Condicion.choices,
                                 default=Condicion.HABILITADO,
                                 verbose_name="Condición")
    saldo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Saldo", default=0)
    estado = models.BooleanField(default=True, verbose_name="Estado")

    # Definiendo los related_name para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_groups',  # Este es el cambio
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Y aquí el otro cambio
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def clean(self):
        super().clean()
        # Validamos que el DNI tenga la longitud correcta
        if len(self.dni) != 10:
            raise ValidationError("El DNI debe tener 10 caracteres.")

        # Implementamos la validación del DNI
        suma = 0
        cedula = self.dni
        for i in range(len(cedula) - 1):
            x = int(cedula[i])
            if i % 2 == 0:
                x = x * 2
                if x > 9:
                    x = x - 9
            suma += x
        if suma % 10 != 0:
            result = 10 - (suma % 10)
            if int(cedula[-1]) != result:
                raise ValidationError(f"La cédula {cedula} no es ecuatoriana.")
        else:
            if int(cedula[-1]) != int(cedula[-1]):
                raise ValidationError(f"La cédula {cedula} no es ecuatoriana.")


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name' ,'dni', 'email', 'telefono']

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
