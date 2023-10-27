"""
Author: Quintin Dunn
Date: 10/22/23
"""

from datetime import datetime, timedelta

import logging
logger = logging.getLogger("lapsepy.journal.factory.py")


class BaseGQL:
    """
    Base class for GraphQL queries.
    """
    def __init__(self, operation_name: str, query: str):
        self.variables = None
        self.operation_name = operation_name
        self.query = query

    def to_dict(self):
        """
        :return: The GraphQL query as a dictionary, this is what is uploaded to the API.
        """
        return {
            "operationName": self.operation_name,
            "query": self.query,
            "variables": self.variables
        }
