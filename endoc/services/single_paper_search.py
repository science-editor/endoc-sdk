from ..client import APIClient
from ..queries import SINGLE_PAPER_QUERY
from ..models.single_paper import SinglePaperData

class SinglePaperSearchService:
    def __init__(self, api_key):
        self.client = APIClient(api_key)

    def get_single_paper(self, id_value):
        variable_values = {
            "paper_id": {
                "collection": "S2AG",
                "id_field": "id_int",
                "id_type": "int",
                "id_value": id_value
            }
        }
        raw_result = self.client.execute_query(SINGLE_PAPER_QUERY, variable_values)
        data = raw_result.get("singlePaper")
        if not data:
            raise ValueError("No 'singlePaper' key found in response.")
        return SinglePaperData(**data)