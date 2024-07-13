import * as React from 'react';

import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

const suggestions = [];
let lastInputValueLength = 0;


export default function SearchBox() {
  const [value,] = React.useState(null);

  return (
    <Autocomplete id="autocomplete" sx={{ width: 550 }} value={value}
      options={[]}

      filterOptions={(options, params) => {
        const filtered = [];

        const { inputValue } = params;

        if (inputValue.length < 4) {
          return filtered;
        }

        if (inputValue.length < lastInputValueLength) {
          suggestions.pop();
          return suggestions[sessionStorage.suggestions.length - 1];
        }
        else {
          const newSuggestions = [inputValue + " alguma coisa alem", inputValue + " alguma coisa"];
          suggestions.push(newSuggestions);

          return newSuggestions;
        }
      }}

      renderInput={(params) => (
        <TextField {...params} />
      )}
    />
  );
}
