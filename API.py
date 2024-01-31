from enum import Enum
from dataclasses import dataclass
import json
import argparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from json import JSONDecodeError


class ApiError(Exception):
    pass


class ParsingError(ApiError):
    pass


class ActionType(Enum):
    NAVIGATE = 'navigate'
    CLICK = 'click'
    EXECUTE_SCRIPT = 'execute_script'
    SCREENSHOT = 'screenshot'
    INSTALL_PLUGIN = 'install_plugin'


@dataclass
class Action:
    type: ActionType
    url: str = None
    selector: str = None
    script: str = None
    filename: str = None
    plugin_name: str = None


class API:
    """
    Cette classe représente l'interface pour interagir avec le navigateur via
    Selenium.
    """
    def __init__(self, instructions_file):
        self.instructions_file = instructions_file
        self.instructions = self._read_instructions()
        self.driver = self._initialize_driver()

    def _read_instructions(self):
        """
        Lit les instructions à partir du fichier JSON spécifié.

        :return: Dictionnaire contenant les instructions.
        :raises ParsingError: En cas d'erreur de lecture ou d'analyse du
        fichier JSON.
        """
        try:
            with open(self.instructions_file, 'r') as file:
                return json.load(file)
        except JSONDecodeError as e:
            # Handle JSON decoding error
            raise ParsingError(f"JSON decoding error: {e}")

    def _initialize_driver(self):
        """
        Initialise le WebDriver de Selenium avec les options configurées.

        :return: Instance du WebDriver configuré.
        """
        chrome_options = Options()
        # Configuration des options Chrome, y compris les plugins
        for action in self.instructions['actions']:
            if action['type'] == 'install_plugin':
                plugin_path = action['plugin_name']
                chrome_options.add_extension(plugin_path)

        return webdriver.Chrome(options=chrome_options)

    def navigate(self, action):
        """
        Navigue vers une URL spécifiée.

        :param action: L'objet Action contenant les détails de l'action.
        """
        try:
            if action.url:
                self.driver.get(action.url)
        except Exception as e:
            raise ApiError(f"Error navigating to URL: {e}")

    def click(self, action):
        """
        Effectue un clic sur l'élément spécifié par le sélecteur CSS.

        :param action: L'objet Action contenant les détails de l'action.
        :raises ApiError: En cas d'erreur lors du clic.
        """
        try:
            if action.selector:
                clickable = EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, action.selector)
                )
                element = WebDriverWait(self.driver, 10).until(clickable)
                element.click()
                WebDriverWait(self.driver, 10).until(
                    EC.staleness_of(WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.TAG_NAME, 'body'))
                    ))
                )
        except (TimeoutException, NoSuchElementException) as e:
            raise ApiError(f"Error performing click action: {e}")

    def execute_script(self, action):
        """
        Exécute un script JavaScript spécifié.

        :param action: L'objet Action contenant les détails de l'action.
        """
        try:
            if action.script:
                element = self.driver.execute_script(action.script)
                print('Script result ====> ', element)
        except Exception as e:
            raise ApiError(f"Error executing script: {e}")

    def screenshot(self, action):
        """
        Prend un screenshot du navigateur.

        :param action: L'objet Action contenant les détails de l'action.
        """
        try:
            if action.filename:
                self.driver.save_screenshot(action.filename)
        except Exception as e:
            raise ApiError(f"Error taking screenshot: {e}")

    def install_plugin(self, action):
        """
        Install un plugin au navigateur.

        :param action: Chemin vers le fichier du plugin (.crx).
        """
        try:
            if action.plugin_name:
                self.driver_options = Options()
                self.driver_options.add_extension(action.plugin_name)
                self.driver = webdriver.Chrome(options=self.driver_options)
        except Exception as e:
            raise ApiError(f"Error installing plugin: {e}")

    def close(self):
        """
        Ferme le navigateur.
        """
        self.driver.quit()

    def execute_instructions(self):
        """
        Exécute les instructions contenues dans le fichier d'instructions JSON.

        :raises ParsingError: En cas d'erreur lors de la lecture du fichier
        JSON.
        :raises ApiError: En cas d'erreur lors de l'exécution des instructions.
        """
        # Dictionnaire des actions avec les méthodes correspondantes
        actions_dispatcher = {
            ActionType.NAVIGATE: self.navigate,
            ActionType.CLICK: self.click,
            ActionType.EXECUTE_SCRIPT: self.execute_script,
            ActionType.SCREENSHOT: self.screenshot,
        }
        # Lecture du fichier d'instructions au format JSON
        try:
            # Parcours des actions dans les instructions
            for action_data in self.instructions['actions']:
                action_type = ActionType[action_data['type'].upper()]
                action_function = actions_dispatcher.get(action_type)
                if action_function:
                    action_data['type'] = action_type
                    action = Action(**action_data)
                    action_function(action)
        except JSONDecodeError as e:
            # Gestion des erreurs de lecture ou d'analyse du fichier JSON
            raise ParsingError(f"JSON decoding error: {e}")

        except Exception as e:
            # GGestion des autres erreurs inattendues
            raise ApiError(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Création du parseur d'arguments
    parser = argparse.ArgumentParser(description="Selenium Automation API")
    parser.add_argument(
        '-f', '--file',
        dest='instructions_file',
        type=str,
        default='instructions.json',
        help=('Chemin vers le fichier JSON contenant les instructions '
              '(optionnel)')
    )
    # Récupération des arguments
    args = parser.parse_args()
    try:
        # Initialisation de l'API avec le driver et le fichier d'instructions
        print("Initialisation de l'API...")
        api = API(instructions_file=args.instructions_file)
        # Exécution des instructions
        api.execute_instructions()
        # Fermeture du driver
        api.close()
        print("Fin d'execution de l'API.")
    except ApiError as e:
        # Gestion des erreurs de l'API
        print(f"API error: {e}")
    except Exception as e:
        # Gestion des autres erreurs inattendues
        print(f"Unexpected error: {e}")
