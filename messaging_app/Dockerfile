FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# To run this container, use the command: docker run -p 8000:8000 <image_name>
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]