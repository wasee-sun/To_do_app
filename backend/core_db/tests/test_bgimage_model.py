import os
import io
from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from core_db.models import BgImage


class UserModelImageTests(TestCase):
    """Testing Image upload."""

    def setUp(self):
        "Environment Setup"
        # Create a 10x10 black image using Pillow
        black_image = Image.new("RGB", (10, 10), "black")

        # Save the image to BytesIO object
        image_bytes = io.BytesIO()
        black_image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)

        # Create the image
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=image_bytes.read(),
            content_type="image/jpeg",
        )

        # Create bgImage object
        self.bgImage = BgImage.objects.create()

        # Create image path
        self.image_path = None

    def tearDown(self):
        if self.image_path and os.path.exists(self.image_path):
            os.remove(self.image_path)
        self.bgImage.delete()

    def test_user_with_profile_image(self):
        """Test creating a background image"""
        self.bgImage.image = self.image
        self.bgImage.save()
        self.image_path = os.path.join(settings.MEDIA_ROOT, self.bgImage.image.name)

        self.assertTrue(self.bgImage.image)
        self.assertEqual(self.bgImage.image, "others/test_image.jpg")
        self.assertTrue(os.path.exists(self.image_path))
