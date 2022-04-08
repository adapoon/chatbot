FROM python
COPY chatbot.py /chatbot.py
COPY requirements.txt /requirements.txt
RUN pip install pip update
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=5229910365:AAFBPO2l2Z-FmdtoEuVRh4C09ySVqF42xXE
EXPOSE 80
ENTRYPOINT ["python", "/chatbot.py"]
