FROM python:3.10
EXPOSE 5000
WORKDIR /app
RUN pip install flask
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