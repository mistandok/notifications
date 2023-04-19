from rest_framework import serializers


class PersonalNotifySerializer(serializers.Serializer):
    NOTIFY_TYPE_CHOICES = (("AU", "Авторизация"),)
    PROVIDER_TYPE_CHOICES = (("MA", "Почта"),)
    notify_type = serializers.ChoiceField(choices=NOTIFY_TYPE_CHOICES, required=True)
    name = serializers.CharField(required=True)
    provider = serializers.ChoiceField(choices=PROVIDER_TYPE_CHOICES, required=True)
    address = serializers.CharField(required=True)
    data = serializers.JSONField(required=False, allow_null=True)
