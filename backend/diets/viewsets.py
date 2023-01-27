from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import DietSerializer, CreateDietSerializer
from .models import Diet
from django.db import transaction


class DietViewSet(ModelViewSet):
    serializer_class = DietSerializer
    queryset = Diet.objects.select_related("creator")
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == 'create':
            return CreateDietSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(is_public=True)
        elif self.action == 'user_diets':
            return self.queryset.filter(creator=self.request.user)
        return self.queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'Diet': 'Diet successfully created'}
        return response

    @action(detail=False, methods=['get'])
    def user_diets(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

