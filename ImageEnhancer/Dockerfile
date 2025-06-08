FROM photoenhancer-base:latest
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /usr/app

COPY . .
RUN rm -rf frontend

CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--workers", "3"]