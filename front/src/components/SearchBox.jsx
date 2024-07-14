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
    return (await response.json())["data"]["searchTerms"];
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
    <Autocomplete id="autocomplete" sx={{ width: "60vw", backgroundColor: "white" }} 
      options={options} 
      freeSolo
      autoHighlight
      onInputChange={onInputChange}
      renderInput={(params) => (
        <TextField {...params} InputProps={{...params.InputProps, style: {height: "7vh", fontSize: "min(6vh, 18px)"}}}/>
      )}
      ListboxProps={{
        style: {
          maxHeight: "min(40vh, 300px)",
          border: "1px solid",
          whiteSpace: "nowrap",
          fontSize: "80%"
        }
      }}
    />
  );
}
