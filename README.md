# API-Selenium-Python

Ce projet implémente une API en Python pour automatiser les interactions avec les navigateurs web via Selenium. Il permet de lire un ensemble d'instructions à partir d'un fichier JSON et d'exécuter diverses actions telles que naviguer sur des pages web, cliquer sur des éléments, exécuter des scripts JavaScript, prendre des captures d'écran et installer des plugins.

## Table des Matières

- [Prérequis](#prérequis)
- [Installation des Dépendances](#installation-des-dépendances)
- [Execution](#execution)
- [Installation + Execution de l'API](#installation--execution-de-lapi)
- [Format du fichier JSON](#format-du-fichierjson)
- [Description](#descriptions)
- [Norme](#norme)

## Prérequis

```bash
  python >= 3.12.1
  Google Chrome >= 120.0.6099.234
```
    
## Installation des Dépendances


```bash
  Pip3 install -r requirements.txt   
```
## Execution

Execution du programme sans argument(Le programme sera lancé par default avec introduction.json):

```bash
  Python3 API.py
```

Execution du programme avec argument(file.json):

```bash
  Python3 API.py /path/file.json
```

## Installation + Execution de l'API

Vous pouvez installer et executer le projet directement avec le script :


1 - Le script installe un environnement virtual Python

2 - Installe les dépendances

3 - Lance l'API

Sans Argument : (Le programme est lancé avec le json inclue dans le dossier "intructions.json")
```bash
  chmod +x start.sh
  ./start.sh
```

avec Argument : (Le programme est lancé avec le json de votre choix)

```bash
  chmod +x start.sh
  ./start.sh /path/file.json
```


## Format du fichier.json

Voici le Format du Json:

```json
  {
  "actions": [
    {
      "type": "navigate",
      "url": "https://example.com"
    },
    {
      "type": "click",
      "selector": "#buttonId" // css selector could be div.<class_name> -> div.login_link
    },
    {
      "type": "execute_script",
      "script": "return document.title;"
    },
    {
      "type": "screenshot",
      "filename": "screenshot.png"
    },
    {
      "type": "install_plugin",
      "plugin_name": "cookie_popup_blocker" // download in local and install it from selenium
    }
  ]
}
```

## Descriptions

Voici quelques explications sur les fonctions Selenium utilisé dans mon API:

Installation de Plugin

La méthode install_plugin permet d'installer un plugin dans le navigateur.
Information : Les plugin s'installe au demarrage du driver et ne peux etre installé en cours de route.
```python
    driver_options = Options()
    driver_options.add_extension("plugin_name") # un plugin à pour extension .crx
    driver = webdriver.Chrome(options=self.driver_options)
```

La méthode navigate permet de naviguer vers une URL spécifiée.

``` python
    driver.get("http://www.exemple.com")
```

Exécution de Script

La méthode execute_script exécute un script JavaScript.

```python
    driver.execute_script("script JavaScript")
```

Capture d'Écran

La méthode screenshot prend une capture d'écran de la page actuelle.

```python
    driver.save_screenshot("filename")
```

Wait

La méthode wait est cruciale pour gérer les éléments dynamiques sur les pages web. En utilisant cette méthode, le script Selenium attend qu'un certain état soit atteint avant de continuer l'exécution. Cela améliore la stabilité du script en s'assurant que les éléments sont chargés et interactifs.

Il existe deux types de wait dans Selenium :

1 - Explicit Wait : Attend explicitement qu'une certaine condition soit remplie avant de continuer. Par exemple, attendre qu'un élément soit visible ou cliquable.

```python
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID,"monElement"))
    )
```

2 - Implicit Wait : Configure un délai d'attente global pour le WebDriver, qui sera appliqué à toutes les opérations.

```python
    driver.implicitly_wait(10)
```

## Norme

Ce projet respecte la norme PEP 8 Python.