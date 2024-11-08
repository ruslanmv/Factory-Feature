import unittest
from src.main import main

class TestMain(unittest.TestCase):
    def test_main_flow(self):
        prompt = "Add user authentication feature"
        main(prompt)
        self.assertTrue(os.path.exists("./project_new"))
