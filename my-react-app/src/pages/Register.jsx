import React, { useState } from 'react';
import { Container, TextField, Button, Typography, Paper, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/AxiosInstance';

const Register = () => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [alert, setAlert] = useState({ show: false, message: '', severity: '' });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setAlert({ show: true, message: 'Passwords do not match!', severity: 'error' });
      return;
    }
    try {
      const response = await axiosInstance.post('/register/', { email, name, password, password2: confirmPassword });
      setAlert({ show: true, message: 'Registration successful!', severity: 'success' });
      setTimeout(() => {
        setAlert({ show: false, message: '', severity: '' });
        navigate('/login');
      }, 2000);
    } catch (error) {
      setAlert({ show: true, message: `Registration failed! ${error.response?.data?.message || ''}`, severity: 'error' });
    }
  };

  return (
    <Container maxWidth="xs" style={{ marginTop: '2rem' }}>
      <Paper elevation={3} style={{ padding: '2rem', backgroundColor: 'white' }}>
        <Typography variant="h4" align="center" gutterBottom>Register</Typography>
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
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Register
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export default Register;
