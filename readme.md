# AuthFace
Sistema de autentificacion mediante reconocimiento facial.

## El sistema cuenta con 3 microservicios
- AuthBackend se encarga de servir los datos de resgistro de usuarios, sitios y embeddings de biometria a demas de hacer la verificacion de rostro, desarrollado con djangoRestFramework
- AuthFrontend es el frontend de un dashboard para la gestion de la cuenta de usuario es minimalista, esta desarrollada con fasthtml.
- AuthExtension una extencion de navegador que bloquea los inicios de sesion al menos que sea verificado con reconocimiento facial.

# Instalar dependencias
Para la instalacion de las dependencias debe ejecutar estos scripts:
## Linux
Para linux solo ejecute install.sh, secreara el entorno y instalara las dependencias necesarias.

## Windows
Cooming soon

# Ejecutar
Hay que mejorar el script de start.sh
