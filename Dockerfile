FROM python:3.6
  
ADD t-reqs /t-reqs
RUN pip install configargparse
