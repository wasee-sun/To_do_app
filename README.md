# Todo List App

**Welcome to the Todo List App**, a fullstack web application built with **Next.js** for the frontend and **Django REST Framework** for the backend, utilizing **REST** APIs and a **Postgres** database. This project provides a simple and efficient way to manage tasks with a clean interface and robust backend functionality. One can create, update, delete, and track the completion status of todo items seamlessly. Moreover, one can also change the default background image.

For more details, visit the [GitHub repository](https://github.com/wasee-sun/To_do_app).

## Features

- **Task Management**: Create, update, delete, and retrieve todo items with ease.
- **Completion Tracking**: Mark todos as complete or incomplete with timestamps.
- **Filtering**: Filter todos by title (case-insensitive) and completion status.
- **RESTful API**: Built with Django REST Framework, adhering to REST standards.
- **Public Access**: No authentication required for API endpoints, making it accessible to all users.
- **Responsive Frontend**: Powered by Next.js for a fast and dynamic user experience.
- **Customizable Background**: One can change the default background image for the app.

## Usage

Key workflows include:

- **View Todos**: Retrieve all todos or filter them by title or completion status.
- **Add a Todo**: Create a new todo item with a title and optional completion status.
- **Update a Todo**: Modify the title or completion status of an existing todo.
- **Delete a Todo**: Remove a todo item by its ID.
- **Complete/Incomplete**: Mark a todo as completed or revert it to incomplete with dedicated endpoints.
- **Background Image**: Customize the default background image for the app.

## API Documentation

The API provides endpoints for managing todo items and background image efficiently. Below is a summary of the key endpoints:

### Todo Endpoints

- **GET /backend-api/todos/**  
  Retrieve a list of all todo items, optionally filtered by title or completion status.

  - **Parameters**: `title` (string, optional), `completed` (boolean, optional).
  - **Example**: `GET /backend-api/todos/?title=example&completed=true`
  - **Response**: List of todo objects (200 OK) or error (400, 500).

- **GET /backend-api/todos/{id}/**  
  Retrieve a single todo item by its ID.

  - **Example**: `GET /backend-api/todos/1/`
  - **Response**: Todo object (200 OK) or error (404, 500).

- **POST /backend-api/todos/**  
  Create a new todo item.

  - **Body**: `title` (string, required), `completed` (boolean, optional).
  - **Example**: `POST /backend-api/todos/` with `{"title": "New Todo", "completed": false}`
  - **Response**: Created todo object (201 Created) or error (400, 500).

- **PATCH /backend-api/todos/{id}/**  
  Partially update a todo item by its ID.

  - **Body**: `title` (string, optional), `completed` (boolean, optional).
  - **Example**: `PATCH /backend-api/todos/1/` with `{"completed": true}`
  - **Response**: Updated todo object (200 OK) or error (400, 404, 500).

- **DELETE /backend-api/todos/{id}/**  
  Delete a todo item by its ID.

  - **Example**: `DELETE /backend-api/todos/1/`
  - **Response**: No content (204 No Content) or error (404, 500).

- **POST /backend-api/todos/{id}/complete/**  
  Mark a todo item as completed, setting the `completed_at` timestamp.

  - **Example**: `POST /backend-api/todos/1/complete/`
  - **Response**: Updated todo object (200 OK) or error (404, 500).

- **POST /backend-api/todos/{id}/incomplete/**  
  Mark a todo item as incomplete, clearing the `completed_at` timestamp.
  - **Example**: `POST /backend-api/todos/1/incomplete/`
  - **Response**: Updated todo object (200 OK) or error (404, 500).

### Background Image Endpoints

- **GET /backend-api/bgimages/1/**  
  Retrieve the background image by its ID.

  - **Example**: `GET /backend-api/bgimages/1/` (only this api endpoint avaliable)
  - **Response**: Background image object (200 OK) or error (404, 500).

- **PATCH /backend-api/bgimages/1/**  
  Partially update the background image by its ID.

  - **Body**: `image` (string, optional)
  - **Example**: `PATCH /backend-api/bgimages/1//` (only this api endpoint avaliable)
  - **Response**: Updated todo object (200 OK) or error (400, 500).

### Best Practices

1. Use filters (`title`, `completed`) to minimize data retrieval for `/todos/`.
2. Handle errors gracefully with fallback mechanisms or user notifications.
3. Prefer `/complete/` and `/incomplete/` endpoints over PATCH for status updates to maintain semantic clarity.
4. Monitor server responses and retry on transient errors (e.g., 500 Internal Server Error).

For detailed request and response formats, refer to the [API Documentation](https://github.com/wasee-sun/To_do_app/blob/main/Api-docxs.pdf).

For the api schema file, refer to the [API Schema](https://github.com/wasee-sun/To_do_app/blob/main/todo_app_backend_schema.yaml).

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/wasee-sun/To_do_app/blob/main/LICENSE) file for details.
