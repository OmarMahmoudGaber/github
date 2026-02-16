FROM python:3.9-slim 
WORKDIR /build
COPY pythonscript.py .
ENTRYPOINT ["python", "pythonscript.py"]   
