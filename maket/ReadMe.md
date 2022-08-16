- create db maket
- utf8mb4_unicode_ci
- /makety create config.cfg
[LOG_PAS]
user = 
pass = 
sec_key = 
admin = False
- from /makety python manage.py makemigrations
- from /makety python manage.py migrate
- manage.py runserver 8800


apt-get update
apt-cache search maria (смотреть что есть за пакеты)
apt-get install mariadb-server
mysql
  create user maketuser identified by password '{password}';
  set collation_server = 'utf8mb4_unicode_ci';
  create database maket;
  grant all privileges on maket.* to 'maketuser';
apt-get install git python
### mkdir p_proj
cd p_proj
git clone https://github.com/tsibul/Makety.git
cd makety
pip install -r requirements.txt (он вначале ругался и сказал вначале сделать apt install python3-pip)
##  apt-get install mariadb-client - зря не то надо было
apt-cache search mariadb
apt-get install libmariadbd-dev - вот этот исправил
pip install -r requirements.txt
cd makety
touch config.cfg
python3 -c 'import secrets; print(secrets.token_hex(100))'
vim config.cfg - текстовый редактор (можешь писать nano config.cfg а то vim очень неинтуитивный)