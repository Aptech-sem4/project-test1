FROM python:3.11

WORKDIR /sites/aptech-s4

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod -R 777 /sites/aptech-s4/sources/app/static/uploads

CMD ["python", "sources/run.py"]

