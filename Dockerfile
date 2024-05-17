FROM python:3.12
EXPOSE 5000
ENV PIP_ROOT_USER_ACTION=ignore
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN flask db upgrade
CMD ["flask", "run", "--host", "0.0.0.0"]
