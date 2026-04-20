from python:3.11-slim
WORKDIR app
COPY requirment.txt .

RUN pip install -r requirment.txt
COPY . .
EXPOSE 5001
CMD ["python","app.py"]