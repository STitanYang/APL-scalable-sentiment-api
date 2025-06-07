# Sentiment Analysis API

This project is a FastAPI application that provides a RESTful API for sentiment analysis. It allows users to submit text, such as product reviews or social media comments, and receive feedback on whether the sentiment of the text is positive or negative. The sentiment analysis is powered by the Hugging Face Inference API using the DistilBERT model (`distilbert-base-uncased-finetuned-sst-2-english`).

## Project Structure

```
sentiment-api
├── src
│   ├── api
│   │   └── v1
│   │       └── sentiment.py      # API endpoints for sentiment analysis
│   ├── services
│   │   └── huggingface_client.py # Handles communication with Hugging Face API
│   ├── models
│   │   └── sentiment.py          # Data models for sentiment analysis results
│   ├── schemas
│   │   └── sentiment.py          # Pydantic schemas for request and response validation
│   └── utils
│       └── __init__.py           # Utility functions and classes
├── requirements.txt              # Project dependencies
├── README.md                     # Project documentation
├── venv                          # Virtual Environment
├── .env                          # Environment variables
├── main.py                       # Entry point for the FastAPI application
├── create_tables.py              # Creating Tables in database
├── fastapi-deployment.yaml       # Deployment of fastapi in docker
├── fastapi-service.yaml          # Service of fastapi in docker
├── postgres-deployment.yaml      # Deployment of postgres in docker
├── postgres-pvc.yaml             # PVC of postgres in docker
├── postgres-jog.yaml             # Job to tables in docker 
├── postgres-secret.yaml          # Secret username and password of postgres in docker
├── postgres-service.yaml         # Service of postgres in docker
├── redis-deployment.yaml         # Deployment of redis in docker
├── redis-service.yaml            # Service of redis in docker
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sentiment-api.git
   cd sentiment-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   
3. Create a `.env` file in the root directory and add your secret:
   ```
   HUGGINGFACE_API_KEY=your_api_key
   MODEL_NAME=your_model_name
   DATABASE_URL=your_database_url
   ```

4. Start Minikube:
   ```
   minikube start
   ```

5. Change your CLI directly to kubernetes:
   ```
   eval $(minikube -p minikube docker-env)
   ```

6. Build the docker:
   ```
   docker build -t sentiment-api:latest .
   ```

7. Deploy Redis:
   ```
   kubectl apply -f redis-deployment.yaml
   kubectl apply -f redis-service.yaml
   ```

8. Deploy the Load Balancer:
   ```
   kubectl apply -f fastapi-deployment.yaml
   kubectl apply -f fastapi-service.yaml
   ```

9. Deploy the Postgres
   ```
   kubectl apply -f postgres-secret.yaml
   kubectl apply -f postgres-deployment.yaml
   kubectl apply -f postgres-service.yaml
   kubectl apply -f postgres-pvc.yaml
   kubectl apply -f postgres-job.yaml
   ```

## Usage

To run the FastAPI application, execute the following command:
```
minikube service fastapi-service
```

You can access the API from the given port after running the command above

## API Endpoints

### POST /api/v1/analyze

- **Request Body**: 
  ```json
  {
    "text": "Your text here"
  }
  ```

- **Response**:
  ```json
  {
    "sentiment": "positive" or "negative",
    "score": 0.95
  }
  ```

### GET /api/v1/requests

- **Response**:
  ```json
  [
    {
        "id": 4,
        "user_id": 1,
        "comment_text": "Produk ini cukup mengecewakan!",
        "created_date": "2025-06-06"
    },
    {
        "id": 5,
        "user_id": 1,
        "comment_text": "Produk ini bagus!",
        "created_date": "2025-06-06"
    },
    ...
   ]
  ```

### GET /api/v1/requests/{id}

- **Response**:
  ```json
  {
    "id": 5,
    "user_id": 1,
    "comment_text": "Produk ini bagus!",
    "created_date": "2025-06-06",
    "result": {
        "label": "positive",
        "score": 0.966884195804596,
        "processed_time": "2025-06-06T13:06:55.297706"
    }
   }
  ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
