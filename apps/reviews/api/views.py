from django.shortcuts import render
from rest_framework import viewsets, permissions
from apps.reviews.domain.models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrAdmin

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-data_avaliacao')
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
