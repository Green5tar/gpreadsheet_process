#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a Python script that performs data receiving from csv file.

Author: Roman Boba
Date: 2023-07-10
"""

import sys
import json
import argparse
import pandas as pd
from typing import Dict, List
from datatypes import FieldValidationCheckNamedTuple


class GoogleCloudFileReader:
    def __init__(self, fields: List[str], file_link: str):
        self.fields = fields
        self.file_link = file_link

    def _retrieve_file(self):
        """
        The function retrieves a file from a given file link and returns it as a pandas DataFrame.
        """
        try:
            data_frame = pd.read_csv(self.file_link)
            return data_frame
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Unable to read file via provided link- {self.file_link}"
            )

    @staticmethod
    def _validate_fields(
        user_fields: List[str], cloud_columns: List[str]
    ) -> FieldValidationCheckNamedTuple:
        """
        The `_validate_fields` function takes in two lists of strings, `user_fields` and `cloud_columns`,
        and checks if each field in `user_fields` is present in `cloud_columns`, returning a named tuple
        indicating the validity of the fields.
        """
        valid_fields = list(set(user_fields) & set(cloud_columns))
        invalid_fields = list(set(user_fields) - set(cloud_columns))
        return FieldValidationCheckNamedTuple(
            is_valid=not invalid_fields,
            invalid_fields=invalid_fields,
            valid_fields=valid_fields,
        )

    @staticmethod
    def _construct_response(
        data_frame: List[Dict[str, str]], selected_fields: List[str]
    ):
        """
        The function `_construct_response` takes a data frame and a list of selected fields, and returns a
        list of dictionaries representing the selected fields from the data frame.
        """
        data_records = data_frame[selected_fields].to_dict(orient="records")
        return json.dumps({"data": data_records}, indent=4)

    def process_document(self) -> Dict[str, object]:
        """
        The `process_document` function retrieves data from a file, validates user-specified fields, and
        constructs a response with the selected fields.
        """
        data_frame = self._retrieve_file()
        cloud_columns = data_frame.columns.to_list()
        if not self.fields:
            # If user not specified any field to retrieve, program will grab all data
            # Validation is not needed
            selected_fields = cloud_columns
        else:
            fields_validation = self._validate_fields(
                user_fields=self.fields, cloud_columns=cloud_columns
            )
            if not fields_validation.is_valid:
                raise ValueError(
                    f"We detected invalid fields - {fields_validation.invalid_fields}"
                )
            selected_fields = fields_validation.valid_fields
        response_data = self._construct_response(
            data_frame=data_frame, selected_fields=selected_fields
        )

        return response_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument(
        "-f", "--fields", type=str, required=True, help="Comma separated string"
    )
    args = parser.parse_args()

    parser.add_argument(
        "-fl",
        "--file_link",
        type=str,
        required=False,
        help="URL to CSV file",
        default="https://drive.google.com/uc?id=1zLdEcpzCp357s3Rse112Lch9EMUWzMLE&export",
    )
    # Parse the command-line arguments
    args = parser.parse_args()

    constructed_data = GoogleCloudFileReader(
        fields=args.fields.split(","), file_link=args.file_link
    ).process_document()

    sys.stdout.write(constructed_data)
