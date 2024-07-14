import { Config } from '../config';

export async function getSuggestions(text, signal = null) {
    const baseURL = Config.API_URL;
  
    const body = {
      signal,
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    };
  
    let response = null;

    try {
      response = await fetch(baseURL + `?query={searchTerms(text:"${text}")}`, body);
    } 
    catch(error) {
      console.error("Oops, something is wrong with the server... Please try again.\n\n" + error);
      return [];
    }
    
    if (response.status === 200) {
      return (await response.json())["data"]["searchTerms"].map((term) => {
        return {term: term, match: term.slice(0, text.length)};
      });
    }
  }