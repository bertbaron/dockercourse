FROM alpine:3.5
RUN apk add --no-cache python py-pip
RUN pip install cherrypy simplejson

WORKDIR "/greeting"
ADD https://code.jquery.com/jquery-3.2.1.min.js \
    static/jquery-3.2.1.min.js
ADD app .
CMD ["python", "service.py"]
EXPOSE 8000
