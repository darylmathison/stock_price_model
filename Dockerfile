FROM amazon/aws-lambda-python:latest
LABEL authors="darylmathison"

COPY requirements.txt .
RUN mkdir -p ${LAMBDA_TASK_ROOT} && pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY data/stock_model.pickle ${LAMBDA_TASK_ROOT}
COPY src/main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.handle" ]