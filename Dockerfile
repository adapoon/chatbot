FROM python
COPY chatbot.py /chatbot.py
COPY const.py /const.py
COPY browse.py /browse.py
COPY search.py /search.py
COPY vote.py /vote.py
COPY nearby.py /nearby.py
COPY top10.py /top10.py
COPY view.py /view.py
COPY help.py /help.py
COPY requirements.txt /requirements.txt
RUN pip install pip update
RUN pip install -r requirements.txt
ARG ACCESS_TOKEN=${ACCESS_TOKEN}
ARG MYSQL_HOST=${MYSQL_HOST}
ARG MYSQL_USER=${MYSQL_USER}
ARG MYSQL_PASS=${MYSQL_PASS}
ARG MYSQL_DTBS=${MYSQL_DTBS}
ENV ACCESS_TOKEN=${ACCESS_TOKEN}
ENV MYSQL_HOST=${MYSQL_HOST}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PASS=${MYSQL_PASS}
ENV MYSQL_DTBS=${MYSQL_DTBS}
EXPOSE 80
ENTRYPOINT ["python", "/chatbot.py"]
