FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Conditionally install the requested DB driver (defaults to postgres)
ARG DB_DRIVER="psycopg2-binary"
RUN if [ -n "$DB_DRIVER" ]; then pip install --no-cache-dir ${DB_DRIVER}; fi

# Copy the application code
COPY . .

EXPOSE 8080

# Set the default execution mode
ENV APP_MODE="web"

# Conditionally run standalone or web API based on APP_MODE
CMD if [ "$APP_MODE" = "standalone" ]; then \
        exec python opentow.py standalone; \
    else \
        exec gunicorn -w 4 -b 0.0.0.0:8080 lib.api.app:app; \
    fi