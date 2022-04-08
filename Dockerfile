FROM python
COPY chatbot.py /chatbot.py
COPY search.py /search.py
COPY browse.py /browse.py
COPY vote.py /vote.py
COPY requirements.txt /requirements.txt
RUN pip install pip update
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=
EXPOSE 80
ENTRYPOINT ["python", "/chatbot.py"]
