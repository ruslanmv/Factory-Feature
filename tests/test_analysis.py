import unittest
from src.analysis.project_parser import parse_project

class TestAnalysis(unittest.TestCase):
    def test_parse_project(self):
        project_data = parse_project("./sample_project")
        self.assertGreater(len(project_data), 0)
