from rest_framework.generics import GenericAPIView

from src.notify_service.notify.serializers import PersonalNotifySerializer
from src.notify_service.notify.tasks import send_auth_message

class CreatePersonalNotify(GenericAPIView):
    serializer_class = PersonalNotifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)