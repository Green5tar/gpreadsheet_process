import unittest
from unittest.mock import patch
import pandas as pd
import json
from run import GoogleCloudFileReader


class TestGoogleCloudFileReader(unittest.TestCase):
    def setUp(self):
        self.fields = ["date", "campaign", "clicks"]
        self.file_link = (
            "https://drive.google.com/uc?id=1zLdEcpzCp357s3Rse112Lch9EMUWzMLE&export"
        )
        self.reader = GoogleCloudFileReader(self.fields, self.file_link)

    def test_process_document(self):
        data_frame = self.reader._retrieve_file()

        response_dict = json.loads(self.reader.process_document())
        self.assertIn("data", response_dict)
        self.assertEqual(len(data_frame), len(response_dict["data"]))


if __name__ == "__main__":
    unittest.main()
