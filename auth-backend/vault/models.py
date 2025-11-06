from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Extiende el modelo User para agregar imagen de perfil"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='users/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Biometria(models.Model):
    """
    Contiene los embeddings faciales de un usuario.
    Puede asociarse posteriormente a varios sitios.
    """
    bioId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='biometrias')
    embedding = models.JSONField()

    def __str__(self):
        return f"Biometría de {self.user.username}"


class Sitios(models.Model):
    """
    Sitios donde el usuario puede autenticarse.
    Un sitio puede usar una o varias biometrias.
    """
    sitioId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sitios')
    nombre = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    username = models.CharField(max_length=100)
    biometrias = models.ManyToManyField(Biometria, related_name='sitios', blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.user.username})"

class SimplePassword(models.Model):
    passwordId = models.AutoField(primary_key=True)
    sitio = models.ForeignKey(Sitios, on_delete=models.CASCADE, related_name='passwords')
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"Password de {self.sitio.nombre}"