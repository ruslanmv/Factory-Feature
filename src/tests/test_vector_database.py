import unittest
from src.vector_database.db_builder import build_vector_database
from src.vector_database.db_query import query_vector_database

class TestVectorDatabase(unittest.TestCase):
    def setUp(self):
        self.mock_data = [
            {"path": "file1.py", "content": "print('Hello, World!')"},
            {"path": "file2.py", "content": "def add(a, b): return a + b"}
        ]
        self.vector_db = build_vector_database(self.mock_data)

    def test_query_vector_database(self):
        query = "Hello"
        results = query_vector_database(self.vector_db, query)
        self.assertGreater(len(results), 0)
