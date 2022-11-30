FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# Install the docker desktop on your machine n login
# This is the command will help to run this python app on the docker container
# docker build -t rest-apis-flask-python .


# running docker conatiner from command line
# docker run -p 5005:5000 rest-apis-flask-python

# to run docker container in te background
# -d is deamon
# docker run -d -p 5005:5000 rest-apis-flask-python

# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - Current deployment
# docker build -t flask-smorest-api .
# docker run -dp 5000:5000 flask-smorest-api

# every time we change the code in editor, we need to build the docker container
# in order to overcame it, we can configure the volume as below
# docker run -d -p 5000:5000 -w /app -v $PWD:/app flask-amorest-api

# - - - - - - execute these three in order, in windows machine only
# docker build -t flask-smorest-api .

# docker run -dp 5000:5000 flask-smorest-api

# or

# docker run -d -p 5000:5000 -w /app -v "${PWD}:/app" flask-smorest-api