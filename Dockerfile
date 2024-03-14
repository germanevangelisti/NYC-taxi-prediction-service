# 
FROM python:3.9

# 
WORKDIR /code

ENV HOST 0.0.0.0

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

EXPOSE 80

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]