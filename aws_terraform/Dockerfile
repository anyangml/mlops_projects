# Deployment with EC2
# FROM python:3.9-slim

# COPY ["aws_terraform/inference_ec2_version.py", "aws_terraform/model.pkl", "./"]

# WORKDIR .

# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir flask joblib numpy scikit-learn

# EXPOSE 8000
# CMD ["python", "inference_ec2_version.py"]


# Depliyment with lambda
FROM public.ecr.aws/lambda/python:3.9

COPY ["aws_terraform/inference_lambda_version.py", "aws_terraform/model.pkl", "./"]

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir joblib numpy scikit-learn

CMD ["inference_lambda_version.predict_handler"]