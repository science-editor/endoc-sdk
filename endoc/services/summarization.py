from ..client import APIClient
from ..queries import SUMMARIZE_PAPER_QUERY
from ..models.summarization import SummarizationResponseData

class SummarizationService:
    def __init__(self, api_key):
        self.client = APIClient(api_key)

    def summarize_paper(self, id_value):
        variable_values = {
            "paper_id": {
                "collection": "S2AG",
                "id_field": "id_int",
                "id_type": "int",
                "id_value": id_value
            }
        }
        raw_result = self.client.execute_query(SUMMARIZE_PAPER_QUERY, variable_values)
        data = raw_result.get("summarizePaper")
        if not data:
            raise ValueError("No 'summarizePaper' key found in response.")
        return SummarizationResponseData(**data)