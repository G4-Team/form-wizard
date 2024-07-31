import traceback

from rest_framework import serializers

from accounts.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone",
            "first_name",
            "last_name",
            "password",
        ]

    def validate_phone(self, value):
        if len(value) != 11 or not value.startswith("09"):
            raise serializers.ValidationError("please enter a valid phone number")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("password must be at least 8 char")
        return value

    def create(self, validated_data):
        ModelClass = self.Meta.model
        try:
            instance = ModelClass._default_manager.create_user(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                "Got a `TypeError` when calling `%s.%s.create()`. "
                "This may be because you have a writable field on the "
                "serializer class that is not a valid argument to "
                "`%s.%s.create()`. You may need to make the field "
                "read-only, or override the %s.create() method to handle "
                "this correctly.\nOriginal exception was:\n %s"
                % (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb,
                )
            )
            raise TypeError(msg)

        return instance

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data.pop("password"))
        return super().update(instance, validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone",
            "first_name",
            "last_name",
            "email_verified",
        ]
        read_only_fields = [
            "email",
            "phone",
            "first_name",
            "last_name",
            "email_verified",
        ]
