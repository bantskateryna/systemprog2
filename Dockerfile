FROM python:3.11-slim

WORKDIR /app

COPY lab2ex1.py ./  
COPY test/ ./test/

RUN pip install pytest

ENTRYPOINT ["bash"]
