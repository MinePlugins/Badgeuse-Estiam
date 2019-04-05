# Badgeuse-Estiam
Code de la Badgeuse ESTIAM

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

# Montage du Lecteur

```
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

## Présentation

Voilà le résultat final :

![Final](https://github.com/MinePlugins/Badgeuse-Estiam/raw/master/Github%20data/global.jpg)

En cas d'erreur :

![Error](https://github.com/MinePlugins/Badgeuse-Estiam/raw/master/Github%20data/error.jpg)

En en fonctionnement normal :

![Error](https://github.com/MinePlugins/Badgeuse-Estiam/raw/master/Github%20data/normal.jpg)