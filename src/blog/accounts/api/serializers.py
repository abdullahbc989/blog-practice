from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    EmailField,
)

User = get_user_model()


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email Address")
    email2 = EmailField(label="Confirm Email")

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'email2',
            'password',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    # def validate(self, data):
    #    email = data['email']
    #    user_qs = User.objects.filter(email=email)
    #    if user_qs.exists():
    #       raise ValidationError("This user is already registered")
    #    return data

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match")
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("A user with this email has already registered")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data
