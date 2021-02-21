FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        build-essential \
        gcc \
        g++ 
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader wordnet
# RUN python app.py
#CMD python ./app.py

# Run the image as a non-root user
#RUN adduser -D myuser
#USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn --bind 0.0.0.0:$PORT wsgi 
#CMD gunicorn --bind 0.0.0.0:80 wsgi 


#https://github.com/microsoft/LightGBM/blob/master/docker/dockerfile-python
#https://github.com/heroku/alpinehelloworld
#https://devcenter.heroku.com/articles/container-registry-and-runtime

#Creating app... done, ⬢ sheltered-reef-65520
#https://sheltered-reef-65520.herokuapp.com/ | https://git.heroku.com/sheltered-reef-65520.git