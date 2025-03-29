from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core_db.models import BgImage, Todo
from .filters import TodoFilter
from .serializers import BgImageSerializer, TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """Todo ViewSet"""

    permission_classes = [AllowAny]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter
    http_method_names = ["get", "post", "patch", "delete"]

    @extend_schema(
        summary="List All Todos",
        description="""Retrieve a list of all todo items, optionally
                        filtered by title or completed status.""",
        parameters=[
            OpenApiParameter(
                name="title",
                description="Filter by title (case-insensitive)",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="completed",
                description="Filter by completion status",
                required=False,
                type=bool,
            ),
        ],
        responses={
            200: TodoSerializer(many=True),
            400: OpenApiResponse(
                description="Bad Request - Invalid parameters",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "string",
                            "example": "Invalid filter parameters",
                        }
                    },
                },
            ),
            500: OpenApiResponse(
                description="Internal Server Error",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Internal Server Error"}
                    },
                },
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get Single Todo",
        description="Retrieve details of a single todo item by ID.",
        responses={
            200: TodoSerializer,
            404: OpenApiResponse(
                description="Not Found - Todo item does not exist",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Todo not found"}
                    },
                },
            ),
            500: OpenApiResponse(
                description="Internal Server Error",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Internal Server Error"}
                    },
                },
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create Todo",
        description="Create a new todo item.",
        request=TodoSerializer,
        responses={
            201: TodoSerializer,
            400: OpenApiResponse(
                description="Bad Request - Invalid data",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Invalid request data"}
                    },
                },
            ),
            500: OpenApiResponse(
                description="Internal Server Error",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Internal Server Error"}
                    },
                },
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Partial Update Todo",
        description="""Partially update an existing
                        todo item by ID using PATCH (PUT is not supported).""",
        request=TodoSerializer,
        responses={
            200: TodoSerializer,
            400: OpenApiResponse(
                description="Bad Request - Invalid data",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Invalid request data"}
                    },
                },
            ),
            404: OpenApiResponse(
                description="Not Found - Todo item does not exist",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Todo not found"}
                    },
                },
            ),
            500: OpenApiResponse(
                description="Internal Server Error",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Internal Server Error"}
                    },
                },
            ),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete Todo",
        description="Delete a todo item by ID.",
        responses={
            204: None,
            404: OpenApiResponse(
                description="Not Found - Todo item does not exist",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Todo not found"}
                    },
                },
            ),
            500: OpenApiResponse(
                description="Internal Server Error",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Internal Server Error"}
                    },
                },
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Mark Todo as Complete",
        description="Mark a todo item as completed, setting completed_at to the current time.",
        request=None,
        responses={
            200: TodoSerializer,
            404: OpenApiResponse(
                description="Not Found - Todo item does not exist",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Todo not found"}
                    },
                },
            ),
            500: OpenApiResponse(
                description="Internal Server Error",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Internal Server Error"}
                    },
                },
            ),
        },
    )
    @action(detail=True, methods=["POST"], url_path="complete")
    def complete(self, request, pk):
        """Marks a To-Do item as complete"""
        todo = get_object_or_404(Todo, id=pk)
        todo.completed = True
        todo.completed_at = now()
        todo.save()
        return Response(TodoSerializer(todo).data, status=200)

    @extend_schema(
        summary="Mark Todo as Incomplete",
        description="Mark a todo item as incomplete, clearing the completed_at timestamp.",
        request=None,
        responses={
            200: TodoSerializer,
            404: OpenApiResponse(
                description="Not Found - Todo item does not exist",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Todo not found"}
                    },
                },
            ),
            500: OpenApiResponse(
                description="Internal Server Error",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Internal Server Error"}
                    },
                },
            ),
        },
    )
    @action(detail=True, methods=["POST"], url_path="incomplete")
    def incomplete(self, request, pk):
        """Marks a To-Do item as incomplete"""
        todo = get_object_or_404(Todo, id=pk)
        todo.completed = False
        todo.completed_at = None
        todo.save()
        return Response(TodoSerializer(todo).data, status=200)


class BgImageViewSet(viewsets.ModelViewSet):
    """Viewset for BgImage model"""

    queryset = BgImage.objects.all()
    serializer_class = BgImageSerializer
    http_method_names = ["get", "patch"]

    @extend_schema(
        summary="Get All BgImages(Not Supported)",
        description="""This endpoint is not supported.
        Use GET with an ID to retrieve a specific BgImage.""",
        responses={
            405: OpenApiResponse(
                description="Method Not Allowed",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "string",
                            "example": """Method not allowed. 
                            Use GET with an ID to retrieve a specific BgImage.""",
                        }
                    },
                },
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return Response(
            {
                "error": "Method not allowed. Use GET with an ID to retrieve a specific BgImage."
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @extend_schema(
        summary="Get Single BgImage",
        description="Retrieve details of a single BgImage item by ID.",
        responses={
            200: BgImageSerializer,
            404: OpenApiResponse(
                description="Not Found - BgImage item does not exist",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "BgImage not found"}
                    },
                },
            ),
            500: OpenApiResponse(
                description="Internal Server Error",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Internal Server Error"}
                    },
                },
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Partial Update BgImage",
        description="""Partially update an existing
                        BgImage item by ID using PATCH (PUT is not supported).""",
        request=BgImageSerializer,
        responses={
            200: BgImageSerializer,
            400: OpenApiResponse(
                description="Bad Request - Invalid data",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Invalid request data"}
                    },
                },
            ),
            404: OpenApiResponse(
                description="Not Found - BgImage item does not exist",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "BgImage not found"}
                    },
                },
            ),
            500: OpenApiResponse(
                description="Internal Server Error",
                response={
                    "type": "object",
                    "properties": {
                        "errors": {"type": "string", "example": "Internal Server Error"}
                    },
                },
            ),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        bg_image = self.get_object()

        if not request.data:
            return Response(
                {"error": "No profile image provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        default_image_path = "others/bg-white.jpg"  # Define the default image path

        # Check if the bg_image has an existing image that is not the default image
        if bg_image.image and bg_image.image.name != default_image_path:
            # Remove the previous image file
            bg_image.image.delete(save=False)

        image = request.data.get("image")

        if image.name == "bg-white.jpg":
            bg_image.image = default_image_path  # Set the image to the default image
            bg_image.save()
            return Response(
                {"success": "Image uploaded successfully."}, status=status.HTTP_200_OK
            )

        serializer = self.get_serializer(
            bg_image, data=request.data, partial=True  # Only updating image
        )
        serializer.is_valid(raise_exception=True)  # returns 400 if fails
        serializer.save()

        return Response(
            {"success": "Image uploaded successfully."}, status=status.HTTP_200_OK
        )
