export FLASK_APP=server.py
export FLASK_ENV=development
flask db upgrade -d 'models/migrations'
flask run --host=0.0.0.0 --port=50000
