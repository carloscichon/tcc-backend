FROM python:3.11

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get -y install libgl1
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR code/
EXPOSE 8000

ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]