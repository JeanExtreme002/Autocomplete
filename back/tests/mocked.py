from typing import List


__all__ = ["get_mocked_search_engine",]


class MockedSearchEngine:
    """
    Mock for SearchEngine class. 
    """
    def __init__(self):
        self.__terms = list()
        self.base_url = "mocked_url"
        self.term_index_name = "mocked_index"

    def insert_term(self, term: str) -> None:
        self.__terms.append(term)
    
    def get_all_terms(self, page: int = 0) -> List[str]:
        return self.__terms[100 * page: 100 * page + 100]

    def search(self, text: str, max_results: int = 20) -> List[str]:
        results = []

        for term in self.__terms:
            if term.lower().startswith(text.lower()):
                results.append(term)
                
        return results[:max_results]
    

mocked_search_engine = MockedSearchEngine()

def get_mocked_search_engine():
    """
    Return an instance of a mocked search engine.
    """
    return mocked_search_engine