import unittest
from src.generation.project_generator import generate_project

class TestGeneration(unittest.TestCase):
    def test_generate_project(self):
        generate_project("./project_old", "./project_new", [{"file": "main.py", "content": "# Feature added"}])
        self.assertTrue(os.path.exists("./project_new/main.py"))
