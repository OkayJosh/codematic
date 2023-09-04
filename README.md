# Star Wars Film API

This project implements a RESTful API([OPENAPI](https://codematicapi.onrender.com/docs/?format=openapi)) for retrieving information about Star Wars films and adding comments to them. The API uses data from the Star Wars API (SWAPI) and provides endpoints to get a list of films, add comments to films, and retrieve comments for a specific film. Additionally, it includes automated deployment to a cloud platform.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Usage](#usage)
- [Automated Deployment](#automated-deployment)
- [Contributing](#contributing)

## Introduction

This project aims to demonstrate software development competence by creating a REST API that interacts with the SWAPI. The API provides functionality to list films, add comments, and retrieve comments for films. It also ensures that comments are limited to 500 characters and follows best practices for API design and error handling.

## Features

- Get a list of films with details (id, title, release date, comment count) sorted by release date.
- Add comments to films with a maximum length of 500 characters.
- Get a list of comments for a specific film, sorted by creation date.
- Automated deployment to a cloud platform.

## API Endpoints

- `GET /films/`: Get a list of films sorted by release date.
- `POST /comment_add/`: Add a comment to a film.
- `GET /<film_id>/comments_for_film/`: Get a list of comments for a specific film.
- `GET /comments/`: Get a list of comments.

For detailed API documentation, please visit the [API Documentation](https://codematicapi.onrender.com/docs/) section below.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/OkayJosh/codematic/.git
   cd codematic

2. Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate

3. Run the build script
    ```bash
    chmod +x ./build.sh
    ./build.sh

4. Run the development server:
    ```bash
     python manage.py runserver

5. Start the celery beat:
    ```bash
     celery -A codematic beat -l INFO

6. Start the celery worker:
    ```bash
     celery -A codematic worker -l INFO

## Usage 
To interact with the API, you can use tools like curl, Postman, or any HTTP client. Below are some example requests:

1. Get a list of films:

    ```bash
    curl -X GET http://127.0.0.1:8000/films/
    
2. Add a comment to a film:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"text": "Great film form my view!", "film": "aca1fc94-156e-4500-be4c-418be419cd0a"}' http://127.0.0.1:8000/comment_add/
    
3.  Get comments for a specific film (replace <film_id> with the actual film ID):

    ```bash
    curl -X GET http://127.0.0.1:8000/<film_id>/comments_for_film/
    
4.  Automated Deployment
This project is deployed to a Render using continuous deployment. You can access the live API [here](https://codematicapi.onrender.com/). For API documentation, visit [API Documentation](https://codematicapi.onrender.com/docs/).

5.  Contributing
If you'd like to contribute to this project, please follow the guidelines in the Contributing document.
