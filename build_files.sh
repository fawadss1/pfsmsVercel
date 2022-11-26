echo " BUILD START"
python3.9  -m venv venv
python3.9  venv\scripts\activate
python3.9  -m pip install -r requirements.txt
python3.9 manage.py collectstatic  --noinput --clear
echo " BUILD END"