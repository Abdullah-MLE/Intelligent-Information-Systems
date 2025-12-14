python -m venv .venv

.venv\Scripts\activate

python -m pip install -r requirements.txt

python main.py

python -m pip freeze > requirements.txt
