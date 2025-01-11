from rest_framework import viewsets
from .models import Tag
from .serializers import TagSerializer
from rest_framework.permissions import IsAuthenticated


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]