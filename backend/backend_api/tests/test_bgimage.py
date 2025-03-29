import os
import io
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core_db.models import BgImage


BGIMAGE_URL = reverse("bgimage-list")


def detail_url(bg_id):
    """Create and return a user detail URL"""
    return reverse("bgimage-detail", args=[bg_id])


class PublicBgImageApiImageTests(APITestCase):
    """
    Test user profile image
    All methods except get and patch will return 405 Method Not Allowed
    """

    def setUp(self):
        """Environment Setup"""
        # Create a 10x10 black image using Pillow
        black_image = Image.new("RGB", (10, 10), "black")
        image_bytes = io.BytesIO()
        black_image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)

        # Create a test image file
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=image_bytes.read(),
            content_type="image/jpeg",
        )

        self.bgImage = BgImage.objects.create()
        self.client = APIClient()
        self.upload_url = detail_url(self.bgImage.id)

    def tearDown(self):
        """Delete test image from media storage after test"""
        bgImage = BgImage.objects.get(id=self.bgImage.id)
        if bgImage.image and bgImage.image.name != "others/bg-white.jpg":
            image_path = os.path.join(settings.MEDIA_ROOT, bgImage.image.name)
            if os.path.exists(image_path):
                os.remove(image_path)
        self.bgImage.delete()

    def test_get_bgimage(self):
        """Test getting a background image"""
        response = self.client.get(BGIMAGE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn("Method not allowed", response.data["error"])

    def test_get_bgimage_1(self):
        """Test getting a background image"""
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("image", response.data)

    def test_upload_valid_image(self):
        """Test uploading a valid image"""
        response = self.client.patch(
            self.upload_url, {"image": self.image}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)

    def test_upload_invalid_file_type(self):
        """Test uploading a valid GIF image to trigger file type validation error"""

        # Create a GIF image
        gif_image = Image.new("RGB", (10, 10), "red")
        image_bytes = io.BytesIO()
        gif_image.save(image_bytes, format="GIF")
        image_bytes.seek(0)

        invalid_file = SimpleUploadedFile(
            name="test_image.gif",
            content=image_bytes.read(),
            content_type="image/gif",
        )

        response = self.client.patch(
            self.upload_url, {"image": invalid_file}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Background image type should be JPEG, PNG",
            response.data["image"][0],
        )
