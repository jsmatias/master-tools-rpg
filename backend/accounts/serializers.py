from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(
        max_length=100, required=True, write_only=True, validators=[validate_password])
    username = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        # extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        """It validates if the email is already registered for another user
        """
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError([
                "A user with this email already registered."])

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["email"], validated_data["password"])
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            f"Credentials not valid.")


# Update Serializer
class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    # first_name = serializers.CharField(max_length=100)
    # last_name = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ("username", "email",)

    def validate_email(self, value):
        """It validates if the email is already registered for another user
        """
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError([
                "A user with this email already exists."])

        return value

    def validate_username(self, value):
        """It validates if the email is already registered for another user
        """
        # This method is overwritten by the default and it's not being used
        user = self.context['request'].user
        # user = self.request.user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already in use."})

        return value

    def update(self, instance, validate_data):
        """
        """
        instance.username = validate_data["username"]
        # instance.last_name = validate_data["last_name"]
        # instance.first_name = validate_data["first_name"]
        instance.email = validate_data["email"]

        instance.save()

        return instance


class UpdatePassSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)
    old_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("username", "old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError([
                "The new password fields didn't match."
            ])

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError([
                "Old password is not correct."
            ])

        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
