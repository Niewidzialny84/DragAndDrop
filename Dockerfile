FROM python:3.9
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]