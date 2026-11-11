FROM python:3.11-slim
WORKDIR /app
COPY main.py .
ENV PYTHONUNBUFFERED=1
EXPOSE 10000
CMD ["python", "main.py"]
