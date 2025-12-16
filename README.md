# Travail Pratique #3: Stéganographie

## Auteurs
- LACU01010000, Ulrich Lacmago Mbonwo
- CAMM06609200, Mariama Cire Camara

## Compatibilité
Python - 3.8+

## Utilisation

### Prérequis
1. Installer Python 3.8 ou supérieur: https://www.python.org/downloads/
2. Installer les dépendances:
```bash
pip install -r requirements.txt
```

### Cacher un message dans une image
```bash
python stegano.py hide -i <chemin_image_source.png> -o <chemin_image_sortie.png> -s "votre message secret"
```

Exemple:
```bash
python stegano.py hide -i input/image.png -o output/image_secret.png -s "Bonjour le monde!"
```

### Révéler un message caché dans une image
```bash
python stegano.py reveal <chemin_image.png>
```

Exemple:
```bash
python stegano.py reveal output/image_secret.png
```

## Structure du projet
```
stegano/
├── src/
│   ├── __init__.py     # Module Python
│   ├── cli.py          # Interface en ligne de commande
│   ├── encoder.py      # Encodage du message dans l'image
│   ├── decoder.py      # Décodage du message depuis l'image
│   ├── utils.py        # Fonctions utilitaires
│   └── bonus/          # Fonctionnalités bonus
│       ├── __init__.py
│       ├── file_encoder.py  # Cacher des fichiers dans une image
│       └── file_decoder.py  # Extraire des fichiers d'une image
├── input/              # Images originales
├── output/             # Images avec messages/fichiers cachés
├── requirements.txt    # Dépendances Python
├── stegano.py          # Point d'entrée principal
└── README.md           # Ce fichier
```

## Méthode utilisée
Ce programme utilise la méthode de substitution des bits de poids faible (LSB - Least Significant Bit). Chaque pixel d'une image PNG contient 3 composantes de couleur (Rouge, Vert, Bleu), chacune codée sur 8 bits. En modifiant uniquement le dernier bit de chaque composante, on peut cacher des informations de manière imperceptible à l'œil humain.

## Notes
- Seul le format PNG est supporté (format sans perte de données)
- La capacité de stockage dépend de la taille de l'image: (largeur × hauteur × 3) / 8 caractères maximum

---

## BONUS: Cacher des fichiers dans une image

En plus de cacher du texte, ce programme permet de cacher **n'importe quel type de fichier** (PDF, ZIP, TXT, images, etc.) à l'intérieur d'une image PNG.

### Cacher un fichier dans une image
```bash
python stegano.py hidefile -i <image_source.png> -o <image_sortie.png> -f <fichier_a_cacher>
```

Exemple:
```bash
python stegano.py hidefile -i input/image.png -o output/image_avec_fichier.png -f input/document_secret.pdf
```

### Extraire un fichier caché d'une image
```bash
python stegano.py extract <image.png> -o <chemin_sortie_optionnel>
```

Exemple:
```bash
python stegano.py extract output/image_avec_fichier.png -o output/document_extrait.pdf
```

Si le paramètre `-o` n'est pas spécifié, le fichier sera extrait avec son nom original dans le répertoire courant.

### Capacité de stockage pour les fichiers
La capacité maximale de fichier dépend de la taille de l'image:
- Image 100x100 pixels: ~3.7 Ko
- Image 1920x1080 pixels (Full HD): ~760 Ko
- Image 4000x3000 pixels: ~4.5 Mo

### Format des données cachées
Le fichier est stocké avec les métadonnées suivantes:
1. Longueur du nom de fichier (4 octets)
2. Nom du fichier original (jusqu'à 256 octets)
3. Taille du fichier (4 octets)
4. Données du fichier
