python3 -m venv my-env


source my-env/bin/activate


pip install -r requirements.txt


docker run --name meu-redis -d -p 6379:6379 redis


python app.py


