import React, { useState } from 'react';
import { Container, Typography, TextField, Button, Modal, Box, Alert } from '@mui/material';
import axiosInstance from '../utils/AxiosInstance';

const AddUser = ({ open, handleClose }) => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [alert, setAlert] = useState({ show: false, message: '', severity: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post('/register/', { email, name, password, password2 });
      if (response.data.msg === 'Registration Successful') {
        setAlert({ show: false, message: '', severity: '' });
        handleClose();
      }
    } catch (error) {
      setAlert({ show: true, message: `Adding user failed! ${error.response?.data?.message || ''}`, severity: 'error' });
    }
  };

  return (
    <Modal open={open} onClose={handleClose}>
      <Box sx={modalStyle}>
        <Container>
          <Typography variant="h4" gutterBottom>Add New User</Typography>
          {alert.show && (
            <Alert severity={alert.severity} onClose={() => setAlert({ show: false, message: '', severity: '' })}>
              {alert.message}
            </Alert>
          )}
          <form onSubmit={handleSubmit}>
            <TextField
              label="Name"
              fullWidth
              margin="normal"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <TextField
              label="Email"
              type="email"
              fullWidth
              margin="normal"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <TextField
              label="Password"
              type="password"
              fullWidth
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <TextField
              label="Confirm Password"
              type="password"
              fullWidth
              margin="normal"
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
            />
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Add User
            </Button>
          </form>
        </Container>
      </Box>
    </Modal>
  );
};

const modalStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

export default AddUser;
