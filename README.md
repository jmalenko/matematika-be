# Backend for matematika


## Deplyment

To deploy the backend component of the application, follow these steps:

```bash
docker build -t matematika-be .
docker run -d --name matematika-be -p 8000:8000 matematika-be
```