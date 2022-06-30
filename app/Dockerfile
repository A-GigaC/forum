FROM python:3.10.4-alpine
WORKDIR /app
RUN pip3 install aiohttp pyjwt jsonschema python-dotenv gino
EXPOSE 8080
COPY . .
CMD ["python3", "main.py"]