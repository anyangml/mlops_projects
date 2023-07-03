FROM huggingface/transformers-pytorch-cpu:latest
COPY ["requirements_prod.txt", "app.py", "data.py", "onnx_inference.py", "./"]
COPY ["models/model.onnx", "./models/"]
WORKDIR .
RUN pip install -r requirements_prod.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]