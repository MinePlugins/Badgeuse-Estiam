# Badgeuse-Estiam  :credit_card: 	

Réalisation complète du code de la badgeuse (API Désactivé et Token retiré)

# Dépendences  :package:

- Python 3
  - Flask
  - Flask_SocketIO
  - graphqlclient
  - PySerial
- Lecteur RFID Arduino (Le code à upload est dans Arduino)

# Matériels  :package:

- Ecran 7" HDMI
- Un Raspberry Pi
- Un Arduino
- Un RFID Reader RC522
- Des badges RFID (Mifare classic)

# Montage du Lecteur  :wrench:

```text
RC522   | Arduino Pin
  VCC   |  +5V
  RST   |   9
  GND   |   GND
  MISO  |   12
  MOSI  |   11
  SCK   |   13
  NSS   |   10
  IRC   |   /
  ```

![Montage](https://github.com/MinePlugins/Badgeuse-Estiam/raw/master/Fritzing/Badgeuse%20ESTIAM_bb.png)


# Configuration du Raspberry Pi:strawberry: :pencil2:
Tous d'abord il faut téléchargé le projet et l'installer sur le Raspberry Pi :
```bash
sudo apt-get install git python3-pip -y
sudo git clone https://github.com/MinePlugins/Badgeuse-Estiam
pip install -r requirements.txt
```
Puis il faut faire démarrer le script python, chromium en mode kiosk et de désactiver la souris à chaque démarrage
pour ce faire il faut édité le fichier `/home/pi/.config/lxsession/LXDE-pi○/autostart`.
Remplacer les lignes par celle-ci :

```bash
@python3 /home/pi/app.py
@sleep 10
@chromium-browser --incognito --kiosk http://127.0.0.1:8000
@unclutter -idle 0
```

Puis pour préserver la planète :earth_americas: nous allons faire une tâche cron qui éteint l'écran tous les soir à 19h du lundi au vendredi et une autre tâche qui allume tous les jour du lundi au vendredi à 8h

```bash
crontab -e

0 8 * * 1-5 vcgencmd display_power 1 >/dev/null 2>&1
0 19 * * 1-5 vcgencmd display_power 0 >/dev/null 2>&1

```

Enfin redémmarer les Raspberry Pi normalement tous s'allume correctement (si il est connecté à internet)
```bash
sudo reboot
```
# UI

[Lien .pdf du design](https://github.com/MinePlugins/Badgeuse-Estiam/raw/master/Design/Design%20Badgeuse.pdf)

## Présentation

Voilà le résultat final :

![Final](https://github.com/MinePlugins/Badgeuse-Estiam/raw/master/Github%20data/global.jpg)

En cas d'erreur :

![Error](https://github.com/MinePlugins/Badgeuse-Estiam/raw/master/Github%20data/error.jpg)

En en fonctionnement normal :

![Normal](https://github.com/MinePlugins/Badgeuse-Estiam/raw/master/Github%20data/normal.jpg)

En cas de dysfonctionnement :

![Dys](https://github.com/MinePlugins/Badgeuse-Estiam/raw/master/Github%20data/probleme.jpg)