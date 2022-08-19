FROM python:3.10-slim

WORKDIR /opt

RUN apt update && apt install git build-essential cmake -y --no-install-suggests --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* /usr/share/man/* /root/.cache/*

RUN git clone https://github.com/Husseinfo/tracker.git --depth=1 && rm -rf tracker/.git

# Install Dlib
ENV CFLAGS=-static
RUN pip3 install --upgrade pip && \
    git clone -b 'v19.21' --single-branch https://github.com/davisking/dlib.git --depth=1 && \
    cd dlib/ && python3 setup.py install --set BUILD_SHARED_LIBS=OFF && cd /opt && rm -rf dlib/

WORKDIR /opt/tracker
ENV DJANGO_SUPERUSER_EMAIL admin@admin.local
ENV DJANGO_SUPERUSER_USERNAME admin
ENV DJANGO_SUPERUSER_PASSWORD admin
RUN pip install -r requirements.txt && python manage.py migrate && python manage.py createsuperuser --noinput && python manage.py test

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
