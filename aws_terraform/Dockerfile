FROM python:3.9-slim

COPY ["aws_terraform/inference.py", "aws_terraform/model.pkl", "./"]

WORKDIR .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir flask joblib numpy scikit-learn

EXPOSE 8000
CMD ["python", "inference.py"]