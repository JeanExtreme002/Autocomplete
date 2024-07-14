import * as React from 'react';

import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

async function getSuggestions(text) {
  const baseURL = process.env.REACT_APP_API_URL;

  const body = {
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
  };

  const response = await fetch(baseURL + `?query={searchTerms(text:"${text}")}`, body);
  
  if (response.status === 200) {
    return (await response.json())["data"]["searchTerms"].map((term) => {
      return {term: term, match: term.slice(0, text.length)};
    });
  }
}

export default function SearchBox() {
  const [options, setOptions] = React.useState([]);
  
  const getData = (inputValue) => {
    getSuggestions(inputValue).then((results) => setOptions(results));
  };
  
  const onInputChange = (event, value, reason) => {
    value ? getData(value) : setOptions([]);
  };

  return (
    <Autocomplete id="autocomplete" options={options}
      sx={{ width: "60vw", backgroundColor: "white" }} 

      autoHighlight 
      noOptionsText=""
      onInputChange={onInputChange}

      getOptionLabel={(option) => option.term}

      renderOption={(props, option) => {
        const term = option.term.replace(option.match, "<b>" + option.match + "</b>").replaceAll(" ", "&nbsp;");
        return (<li {...props} dangerouslySetInnerHTML={{ __html: term }}></li>)
      }}

      renderInput={(params) => (
        <TextField {...params} InputProps={{...params.InputProps, style: {height: "7vh", fontSize: "1.4vmax"}}}/>
      )}

      ListboxProps={{
        style: {
          maxHeight: "min(20vmax, 300px)",
          border: "1px solid",
          whiteSpace: "nowrap",
          fontSize: "min(1vmax, 12px)"
        }
      }}
    />
  );
}
