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

RUN --mount=type=secret,id=ACCESS_TOKEN \
  --mount=type=secret,id=MYSQL_HOST \
  --mount=type=secret,id=MYSQL_USER \
  --mount=type=secret,id=MYSQL_PASS \
  --mount=type=secret,id=MYSQL_DTBS \
  export ACCESS_TOKEN=$(cat /run/secrets/ACCESS_TOKEN) && \
  export MYSQL_HOST=$(cat /run/secrets/MYSQL_HOST) && \
  export MYSQL_USER=$(cat /run/secrets/MYSQL_USER) && \
  export MYSQL_PASS=$(cat /run/secrets/MYSQL_PASS) && \
  export MYSQL_DTBS=$(cat /run/secrets/MYSQL_DTBS) && \
  python chatbot.py

EXPOSE 80
CMD ["/bin/bash"]
