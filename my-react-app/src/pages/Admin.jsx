import React, { useState, useContext } from 'react';
import { Container, Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import AddUser from './Adduser';
import AddTravelPlan from './AddTravelPlan';
import ResetPassword from './ResetPassword';

const Admin = () => {
  const navigate = useNavigate();
  const { logoutUser } = useContext(AuthContext);
  const [openAddUser, setOpenAddUser] = useState(false);
  const [openAddTravelPlan, setOpenAddTravelPlan] = useState(false);
  const [openResetPassword, setOpenResetPassword] = useState(false);

  console.log("--> ",localStorage)
  return (
    <Container>
      <Typography variant="h4" gutterBottom>Admin Dashboard</Typography>
      <Button variant="contained" color="primary" onClick={() => navigate('/admin/users')}>
        See All Users
      </Button>
      <Button variant="contained" color="primary" onClick={() => setOpenAddUser(true)}>
        Add New User
      </Button>
      <Button variant="contained" color="primary" onClick={() => navigate('/admin/travel-plans')}>
        See All Travel Plans
      </Button>
      <Button variant="contained" color="primary" onClick={() => setOpenAddTravelPlan(true)}>
        Add New Travel Plan
      </Button>
      <Button variant="contained" color="secondary" onClick={() => setOpenResetPassword(true)}>
        Reset Password
      </Button>
      <Button variant="contained" color="secondary" onClick={logoutUser}>
        Logout
      </Button>
      <AddUser open={openAddUser} handleClose={() => setOpenAddUser(false)} />
      <AddTravelPlan open={openAddTravelPlan} handleClose={() => setOpenAddTravelPlan(false)} />
      <ResetPassword open={openResetPassword} handleClose={() => setOpenResetPassword(false)} />

    </Container>
  );
};

export default Admin;
