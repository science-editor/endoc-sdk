SAMPLE_DOC_SEARCH_JSON = {
    "status": "success",
    "message": "Request completed successfully.",
    "response": {
        "search_stats": {
            "DurationTotalSearch": 2217.0,
            "nMatchingDocuments": "14318924"
        },
        "paper_list": [
            {
                "collection": "S2AG",
                "id_field": "id_int",
                "id_type": "int",
                "id_value": "221802394"
            }
        ],
        "reranking_scores": [0.5, 0.4],
        "prefetching_scores": [0.6, 0.3]
    }
}

class DummyAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def execute_query(self, query, variable_values=None):
        _ = query
        _ = variable_values
        return {"documentSearch": SAMPLE_DOC_SEARCH_JSON}