FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

RUN sudo apt-get install binutils libproj-dev gdal-bin

WORKDIR /app
RUN pip install pipenv
COPY ./ ./
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
