import base64
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated,BasePermission
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from vault import serializers
from vault.serializers import BiometriaSerializer, UserSerializer
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
        return Response({"username":user.username,"email":user.email,"id":user.id})

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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

    def get(self,request):
        biometria = Biometria.objects.filter(user=request.user).first()
        if biometria:
            return Response({"add":True,"bioId":biometria.bioId})
        else:
            return Response({"add":False})

    def post(self, request):
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
        return Response({"verific": verificacion})

class BiometriaViewSet(viewsets.ModelViewSet):
    queryset = Biometria.objects.all()
    serializer_class = BiometriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Biometria.objects.all()
        return Biometria.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Extraemos solo los embeddings
        embeddings = [b.embedding for b in queryset]

        backup_data = {
            "user_id": request.user.id,
            "username": request.user.username,
            "embeddings": embeddings
        }
        return Response(backup_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        imgs = request.data.get("rostros", [])
        if not imgs:
            return Response(
                {"error": "No se recibió ninguna imagen"},
                status=status.HTTP_400_BAD_REQUEST
            )

        rostros = []
        for i, img in enumerate(imgs):
            format, imgstr = img.split(";base64")
            ext = format.split("/")[-1]
            rostro = ContentFile(base64.b64decode(imgstr), name=f"captura_{i}.{ext}")
            rostros.append(rostro)

        # Generas embedding
        embedding_prom = generar_embeddings(rostros)

        # Pasas los demás datos al serializer
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(
            instance,
            data={**request.data, "embedding": embedding_prom},
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        # Guardar
        serializer.save()

        return Response({
            "message": "Biometría actualizada correctamente",
            "biometria": serializer.data
        })