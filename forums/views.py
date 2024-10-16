from rest_framework import viewsets
from .models import Category, Thread, Responses, Tag
from rest_framework import status
from rest_framework.response import Response
from .serializers import CategorySerializer, ThreadSerializer, ResponseSerializer, TagSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


    def create(self, request, *args, **kwargs):
        user = request.user
        tags_data = request.data.pop('tags', [])

        if 'category_id' not in request.data:
            return Response({"error": "category_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        thread = serializer.save(user=user)

        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            thread.tags.add(tag)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Responses.objects.all()
    serializer_class = ResponseSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
