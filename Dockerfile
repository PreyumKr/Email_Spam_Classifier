FROM python:3.10-slim

ARG PYTORCH_VARIANT=

WORKDIR /app

COPY requirements${PYTORCH_VARIANT:+-$PYTORCH_VARIANT}.txt requirements.txt
RUN if [ -z "$PYTORCH_VARIANT" ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    else \
      pip install --no-cache-dir -r requirements.txt; \
      pip install torch torchvision --index-url https://download.pytorch.org/whl/cu132; \
    fi

COPY models /app/models
COPY Load_Model.py /app

EXPOSE 8501

CMD ["streamlit", "run", "Load_Model.py", "--server.port=8501", "--server.address=0.0.0.0"]