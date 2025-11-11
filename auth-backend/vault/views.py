import base64
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from vault.serializers import UserSerializer
from .opencv_module import generar_embeddings, comparar_rostros, encode_embedding
from .models import Biometria
from django.contrib.auth.models import User
# Create your views here.

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response(status=200)

class UserInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        print(user)
        return Response({"username":user.username,"email":user.email})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]


class BionmetriaView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        imgs = request.data.get("rostros",[])
        rostros = []
        if not imgs:
            return Response({"Error":"No se recibio ninguna imagen"},status=status.HTTP_400_BAD_REQUEST)

        for i, img in enumerate(imgs):
            format, imgstr = img.split(';base64')
            ext = format.split('/')[-1]
            rostro = ContentFile(base64.b64decode(imgstr),name=f"captura_{i}.{ext}")
            rostros.append(rostro)

        user = User.objects.get(username=request.user.username)
        embeding_prom = generar_embeddings(rostros)
        embeding_prom_save = Biometria(user = user,embedding=embeding_prom)
        embeding_prom_save.save()
        return Response({"mensaje":f"Rostro guardado"})

class BiometriacheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Aquí recibirás los datos enviados desde la extensión
        image_data = request.data.get("image")
        embeding_p = Biometria.objects.get(user=request.user).embedding
        if not image_data:
            return Response({"error": "No se envió la imagen"}, status=400)
        format, imgstr = image_data.split(';base64')
        ext = format.split('/')[-1]
        data_bytes = base64.b64decode(imgstr)
        rostro = ContentFile(base64.b64decode(imgstr),name=f"captura_0.{ext}")
        embeding_n = encode_embedding(ContentFile(data_bytes, name=f"captura_0.{ext}"))
        verificacion = comparar_rostros(embeding_n,embeding_p)
        if verificacion:
        # Ejemplo: siempre autorizado (solo para test)
            return Response({"message": "Biometría verificada"})
        else: return Response({"message":"Biometria incorrecta"})