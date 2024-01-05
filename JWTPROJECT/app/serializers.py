from djoser.serializers import UserCreateSerializer
from app.models import User

class userCreateSerializer(UserCreateSerializer):
    class Meat(UserCreateSerializer.Meta):
        model=User
        fields=("id","email","password")
        