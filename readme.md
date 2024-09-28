# Django Developer -- Data Science Focus -- Remote

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose
- Python 3.x
- Django

### Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-repo-url.git
    cd your-repo-url
    ```

2. **Set Up the Environment:**
    - Create a virtual environment and activate it:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

    - Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```

3. **Create an .env file:**
    - Create a file named `.env` in the root of the project using the `env_example` file as a template.

4. **Docker:**
    - Build and start the Docker containers:
    ```bash
    docker-compose up --build -d
    ```

5. **Run Migrations:**
    ```bash
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    ```

6. **Load Initial Data:**
    - Unzip the dataset and place the JSON files in the `data` directory.
    - Run the population script:
        ```bash
        docker-compose exec web python django_project_core/api/scripts/populate_db.py
        ```

7. **Run the Development Server:**
    ```bash
    docker-compose exec web python manage.py runserver 0.0.0.0:8000
    ```
