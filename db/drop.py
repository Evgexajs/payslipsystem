import subprocess

# указываем путь до исполняемого файла mysql
mysql_executable = r'"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"'

# указываем данные для подключения к базе данных
user = "root"
password = "root"
host = "localhost"
database = "paySystem"

# формируем команду для удаления базы данных
command = f"{mysql_executable} -u {user} -p{password} -h {host} -e \"DROP DATABASE {database}\""

# запускаем команду
subprocess.run(command, shell=True)
