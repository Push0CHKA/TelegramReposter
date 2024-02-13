FROM python:alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /aplhagroup_reposter
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt
COPY ./ ./
CMD ["python3", "main.py"]