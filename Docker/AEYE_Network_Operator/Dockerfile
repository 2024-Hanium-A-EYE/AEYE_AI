FROM python:3.6-slim


#############################################################
# Install Dependencies
WORKDIR /app
COPY dependencies_AI.txt /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r dependencies_AI.txt


#############################################################
# Clean

#############################################################
# Copy DIR
WORKDIR /app/

COPY ../../AEYE_Network_Operator/ /app/

#############################################################
# Result


EXPOSE 3000

CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
