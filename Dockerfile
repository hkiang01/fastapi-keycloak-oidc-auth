FROM python:3.7

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/ /app/

RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser
RUN chown -R appuser:appuser /app

USER appuser

CMD ["python", "app/main.py"]]