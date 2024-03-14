FROM python:3.11@sha256:893d6e5056aac0e6465ca48b46184bad966fec3e74d7d56ee684bceb3822aa78
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD bash run.sh