FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8501

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "home.py"]