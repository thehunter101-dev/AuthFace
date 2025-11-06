import base64
import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from .opencv_module import generar_embeddings
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

class BionmetriaView(APIView):
    permission_classes = [AllowAny]
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

        user = User.objects.get(username="admin")
        embeding_prom = generar_embeddings(rostros)
        embeding_prom_save = Biometria(user = user,embedding=embeding_prom)
        embeding_prom_save.save()
        return Response({"mensaje":f"Rostro guardado"})