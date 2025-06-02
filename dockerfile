FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

<<<<<<< HEAD

CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port", "8501", \
     "--server.address", "0.0.0.0", \
     "--server.baseUrlPath", "/", \
     "--server.enableCORS", "true", \
     "--server.enableXsrfProtection", "false"]
=======
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
>>>>>>> 04786e0... change1: change .streamlit config to work with nginx
