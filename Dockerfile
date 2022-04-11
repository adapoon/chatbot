FROM python
COPY chatbot.py /chatbot.py
COPY search.py /search.py
COPY browse.py /browse.py
COPY vote.py /vote.py
COPY location.py /location.py
COPY view.py /view.py
COPY help.py /help.py
COPY requirements.txt /requirements.txt
RUN pip install pip update
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=
ENV MYSQL_HOST=comp7940-mysql.mysql.database.azure.com
ENV MYSQL_USER=comp7940group2
ENV MYSQL_PASS=hkbuMySQL7940
ENV MYSQL_DTBS=chatbot
EXPOSE 80
ENTRYPOINT ["python", "/chatbot.py"]
