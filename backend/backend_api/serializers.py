from rest_framework import serializers
from django.utils.timezone import now
from core_db.models import Todo, BgImage


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"
        read_only_fields = ("id", "created_at")

    def update(self, instance, validated_data):
        validated_data["created_at"] = now()

        return super().update(instance, validated_data)


class BgImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BgImage
        fields = ("id", "image")
        read_only_fields = ("id",)

    def validate_image(self, value):
        """Validate profile image"""
        if not value:
            raise serializers.ValidationError("Background image is required.")

        max_size = 2 * 1024 * 1024  # 2MB
        valid_file_types = ["image/jpeg", "image/png"]  # valid image types

        if value.size > max_size:
            raise serializers.ValidationError(
                "Background image size should not exceed 2MB."
            )

        if (
            hasattr(value, "content_type")
            and value.content_type not in valid_file_types
        ):
            raise serializers.ValidationError(
                "Background image type should be JPEG, PNG"
            )

        return value
