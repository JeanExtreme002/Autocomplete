import * as React from 'react';

import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

import './SearchBox.css';

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

const ListboxComponent = React.forwardRef((props,ref) => {
  const { children, ...other } = props;

  delete other.className;

  return (
    <ul className="Autocomplete-listbox" {...other} ref={ref}>{children}</ul>
  );
});

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

        delete props.className;

        return (<li className="Autocomplete-option" {...props} key={option.term} dangerouslySetInnerHTML={{ __html: term }}></li>)
      }}

      renderInput={(params) => (
        <TextField {...params} InputProps={{...params.InputProps, style: {height: "7vh", fontSize: "1.4vmax"}}}/>
      )}

      ListboxComponent={ListboxComponent}
    />
  );
}
