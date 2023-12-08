FROM python3

WORKDIR /sites/aptech-s4

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./index.py"]

