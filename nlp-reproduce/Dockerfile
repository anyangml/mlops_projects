FROM python:3.11

COPY ["requirements_prod.txt", "app.py", "data.py", "onnx_inference.py", "./"]
COPY ["models/model.onnx.dvc", "./models/"]

WORKDIR .

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

# aws credentials configuration
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY


# install requirements
RUN pip install -r requirements_prod.txt \
    pip install "dvc[s3]" 

WORKDIR ./models/
# initialize dvc
RUN dvc init --no-scm 
RUN dvc remote add -d model-store s3://anyang-mlops-dvc/trained_models/ 
RUN dvc pull model.onnx.dvc

WORKDIR ..
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]