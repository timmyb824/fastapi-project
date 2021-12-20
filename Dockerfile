FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

# running this first will cache the packages so it does not have to run each time we change our code
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# any time there is a space in the command, we need to use the double quotes
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]