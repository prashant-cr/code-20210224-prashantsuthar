FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN nosetests unittests/ -sv --with-xunit --xunit-file=nosetests.xml --with-coverage
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]