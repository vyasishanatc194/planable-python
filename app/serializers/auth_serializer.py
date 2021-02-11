from rest_framework import fields, serializers
from ..models import User, City
from rest_framework.authtoken.models import Token


class CityListingSerializer(serializers.ModelSerializer):
    """
    City serializer
    """

    class Meta:
        model = City
        fields = ["id", "city"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User Profile serializer
    """

    email = serializers.EmailField()
    token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    full_name = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    date_of_birth = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "token",
            "password",
            "city",
            "date_of_birth",
        ]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        custom 'create' so that password gets hashed!
        """
        password = validated_data.pop("password", None)
        city = validated_data.pop("city", None)
        check_city = City.objects.filter(pk=city)
        if not check_city:
            return "invalid city selected"

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.city = check_city.first()
        instance.save()
        return instance

    def get_token(self, obj):
        return f"Token {Token.objects.get_or_create(user=obj)[0]}"


class UserViewSerializer(serializers.ModelSerializer):
    """
    User View serializer
    """

    class Meta:
        model = User
        fields = ["id", "email", "full_name"]
