FROM python:3.9

WORKDIR /app
COPY dashboard/data .
EXPOSE 8080

RUN apt-get update
RUN pip install streamlit pandas matplotlib plotly-express psycopg2-binary SQLAlchemy
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
