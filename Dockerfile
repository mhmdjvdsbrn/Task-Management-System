FROM python:3.10

ADD requirements/ requirements/
RUN pip install -r requirements/production.txt

WORKDIR /app
ADD . .

EXPOSE 8000

CMD [ "./scripts/start.sh" ]
