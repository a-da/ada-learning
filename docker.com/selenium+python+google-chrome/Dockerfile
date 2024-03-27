ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}

COPY . /app
WORKDIR /app

RUN make google-chrome chrome-driver

# Set display port as an environment variable
ENV DISPLAY=:99

RUN pip install --upgrade pip wheel
RUN pip install -r requirements.txt

CMD ["./app.py"]
