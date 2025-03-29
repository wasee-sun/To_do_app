from django.db import models


# Create your models here.
class Todo(models.Model):
    """Todo model."""

    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """String representation of the Todo model."""
        return f"{self.title}"


class BgImage(models.Model):
    """Background image model."""

    image = models.ImageField(upload_to="others/", default="others/bg-white.jpg")

    def __str__(self):
        """String representation of the BgImage model."""
        return f"{self.image}"
