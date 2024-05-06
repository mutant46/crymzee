from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.users.models import UserFile
from app.users.serializers import UserFileSerializer


class DashboardView(LoginRequiredMixin, ListView):
    model = UserFile
    template_name = 'dashboard.html'
    queryset = UserFile.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        search_query = self.request.GET.get('search', None)

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(file_field__icontains=search_query))

        return queryset


class CreateUserFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_424_FAILED_DEPENDENCY)
