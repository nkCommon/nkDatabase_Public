from unittest import TestCase
from NKDatabase.InitialValues.InitialValues import Configuration



class TestCustomFileLocation(TestCase):
    def setUp(self) -> None:
        self.valid_app_name = "nk-edoc-geocoding"
        self.invalid_app_name = "mit-mega-seje-program"
        self.too_short = "kort"
        self.invalid_debug = "False"
        self.valid_debug = False
        self.config: Configuration

    def test_valid_app(self):
        """
        Testing if it passes correctly specified app
        """
        self.config = Configuration(
            self.valid_app_name, self.valid_debug, ini_file="PATH_TO_INI_FILE"
        )
        self.assertIsInstance(self.config.configs, dict)