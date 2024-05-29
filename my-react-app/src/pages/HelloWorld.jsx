import React from 'react';
import Typography from '@mui/material/Typography';

const styles = {
  root: {
    textAlign: 'center',
    marginTop: 50,
  },
};

const HelloWorld = () => {
  return (
    <div style={styles.root}>
      <Typography variant="h3" component="h1">
        Hello, World!
      </Typography>
    </div>
  );
};

export default HelloWorld;
