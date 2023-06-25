from rest_framework.serializers import HyperlinkedModelSerializer

from sport_events.models import Event, Team, Payment
from telegram.models import TelegramUser


class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = TelegramUser
        fields = "__all__"


class EventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class TeamSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class PaymentSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
