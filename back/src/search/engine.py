from elasticsearch import Elasticsearch


class SearchEngine():
    
    term_index_name = "term_index2"

    def __init__(self, host: str, port: int):
        self.client = Elasticsearch(f"http://{host}:{port}")
        self.client._verified_elasticsearch = True

        if not self.client.indices.exists(index=self.term_index_name):
            self.__create_term_index()

    def __create_term_index(self):
        """
        Create a term index into the ElasticSearch.
        """
        self.client.indices.create(
            index=self.term_index_name, 
            body={
                "mappings": {
                    "properties": {
                        "term": {
                            "type": "completion"
                        }
                    }
                }
            }
        )

    def insert_term(self, term: str):
        """
        Insert a new term into the search engine.
        """
        self.client.index(
            index=self.term_index_name,
            document={"term": term}
        )

    def search(self, text: str, max_results: int = 20):
        """
        Search for a term.
        """
        response = self.client.search(
            index=self.term_index_name, 
            body={
                "suggest": {
                    "term_suggest" : {
                        "prefix" : text,
                        "completion" : {
                            "field" : "term",
                            "size": max_results
                        }
                    }
                }
            }
        )
        suggestions = response["suggest"]["term_suggest"][0]["options"]
        
        return [suggestion["text"] for suggestion in suggestions]