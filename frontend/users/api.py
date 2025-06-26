from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Action
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def by_filter(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add_activity/(?P<activity_id>[^/.]+)')
    def add_activity(self, request, pk=None, activity_id=None):
        user = self.get_object()
        action = Action.objects.get(pk=activity_id)
        user.actions.add(action)
        return Response(status=status.HTTP_204_NO_CONTENT)
