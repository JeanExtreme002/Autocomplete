import * as React from 'react';

import Button from '@mui/material/Button';

export default function SearchButton() {
    return (
        <div id='SearchButton'>
            <Button style={{fontSize: '1vmax', marginTop: '2vh'}} variant='contained'>
                Buscar
            </Button>
        </div>
    );
}
