FROM python:3.11

WORKDIR /sites/aptech-s4

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "flask --app index run --host=0.0.0.0 --port=80"]

