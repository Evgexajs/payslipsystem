import os
import subprocess

# указываем путь до исполняемого файла mysql
mysql_executable = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"'

# указываем данные для подключения к базе данных
user = "root"
password = "root"
host = "localhost"

# получаем полный путь до файла mydatabase.sql
current_dir = os.path.dirname(os.path.abspath(__file__))
sql_file = os.path.join(current_dir, "database.sql")

# формируем команду для выполнения скрипта из файла
command = f"{mysql_executable} -u {user} -p{password} -h {host} < {sql_file}"

# запускаем команду
subprocess.run(command, shell=True)
