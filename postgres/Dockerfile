FROM postgres:17.7-alpine
RUN apk update \
  && apk add py-pip make gcc musl-dev \
  && pip install pgxnclient
#RUN apk add postgresql-server-dev-all
#RUN apk add postgresql-common
#RUN pgxn install quantile