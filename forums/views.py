from rest_framework import viewsets
from .models import Category, Thread, Responses, Tag
from rest_framework import status
from rest_framework.response import Response
from .serializers import CategorySerializer, ThreadSerializer, ResponseSerializer, TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        tags_data = request.data.pop('tags', [])

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
