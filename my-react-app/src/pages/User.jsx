import React, { useContext, useState } from 'react';
import { Container, Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import ResetPassword from './ResetPassword';

const User = () => {
  const navigate = useNavigate();
  const { logoutUser } = useContext(AuthContext);
  const [openResetPassword, setOpenResetPassword] = useState(false);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>User Dashboard</Typography>
      <Button variant="contained" color="primary" onClick={() => navigate('/user/travel-plans')}>
        See All Travel Plans
      </Button>
      <Button variant="contained" color="primary" onClick={() => navigate('/user/bookings')}>
        See My Bookings
      </Button>
      <Button variant="contained" color="secondary" onClick={logoutUser}>
        Logout
      </Button>
      <ResetPassword open={openResetPassword} handleClose={() => setOpenResetPassword(false)} />
    </Container>
  );
};

export default User;
