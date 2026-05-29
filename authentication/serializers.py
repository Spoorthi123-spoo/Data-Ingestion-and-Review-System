import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # ---------------------------
        # USERNAME VALIDATION
        # ---------------------------
        if not re.match(r"^[A-Za-z]+$", username):
            raise serializers.ValidationError(
                "Username must contain only letters (no numbers or symbols)"
            )

        # ---------------------------
        # PASSWORD VALIDATION
        # ---------------------------
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError("Password must contain uppercase letter")

        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError("Password must contain lowercase letter")

        if not re.search(r"[0-9]", password):
            raise serializers.ValidationError("Password must contain a number")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise serializers.ValidationError("Password must contain special character")

        return super().validate(attrs)