FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY models /app/models
COPY Load_Model.py /app

EXPOSE 8501

CMD ["streamlit", "run", "Load_Model.py", "--server.port=8501", "--server.address=0.0.0.0"]