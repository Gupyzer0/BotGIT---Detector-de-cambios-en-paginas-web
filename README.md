# BotGit

BotGIT es un programa que diseñado para el escaneo del estado de los portales de la administración pública nacional en búsqueda de modificaciones que pudieran estar relacionadas con una desfiguración de portal web o servidores con respuestas erroneas.

## Instalación

BotGIT está programado en Python3 y hace uso de Qt4 y los bindings de Qt4 para Python3 , PyQT4 y utiliza MariaDB como manejador de base de datos.
```
apt-get install mariadb-server python3 python3-pip qt4-* libqt4-sql-mysql python3-sip python3-pyqt4 python-qt4-sql

pip3 install requests
pip3 install pyperclip
pip3 install reportlab
pip3 install beautifulSoup4
pip3 install python-telegram-bot
```
crear base de datos con el nombre botgit e importar el esquema
```
mysql -u xxxx -p botgit < esquema.sql
```
Para que las alarmas via telegram funcionen es necesario crear un Bot de Telegram y colocar el ID de la conversación y token de acceso en el archivo bin/telegramBot.py

Para más información sobre la instalación consulte el manual incluido con BotGIT.

## Uso:

Navegar a la carpeta bin y ejecutar el archivo main.py
```
Python3 main.py
```
## Autor
Leonel Becerra :eight_pointed_black_star:

## Créditos
Logo e idea original por Miguel Marquez.

### BotGIT es un proyecto de la Universidad Bolivariana de Venezuela para SUSCERTE / VenCERT.
