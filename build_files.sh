echo " BUILD START"
python3.10.2  -m pip install -r requirements.txt
python3.10.2 manage.py collectstatic  --noinput --clear
echo " BUILD END"