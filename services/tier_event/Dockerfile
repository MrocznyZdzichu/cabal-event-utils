FROM python:3.12-slim

RUN ln -snf /usr/share/zoneinfo/Europe/Warsaw /etc/localtime && echo "Europe/Warsaw" > /etc/timezone

WORKDIR /app

ENV IN_DOCKER=Yes

COPY ["./DBManager", "/app/DBManager"]
COPY ["./services/tier_event/requirements.txt", "/app/"]
RUN ["pip", "install", "--no-cache-dir", "-r", "/app/requirements.txt"]

COPY ["./services/tier_event/Source", "/app/Source"]
COPY ["./services/tier_event/app.py", "/app/"]
COPY ["./services/tier_event/templates", "/app/templates"]

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "6001"]