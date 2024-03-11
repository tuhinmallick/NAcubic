FROM python:3.11@sha256:72afb375030b13c8c9cb72ba1d8c410f25307c2dbbd7d59f9c6ccea5cb152ff9
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD bash run.sh