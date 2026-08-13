FROM python:3.11-slim AS base
WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt 

FROM base AS build
COPY . /backend
EXPOSE 8000
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]