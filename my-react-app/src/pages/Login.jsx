import React, { useState, useContext } from 'react';
import { Container, TextField, Button, Typography, Paper, Link, Alert } from '@mui/material';
import AuthContext from '../context/AuthContext';
import { Link as RouterLink } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { loginUser } = useContext(AuthContext);

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Clear any previous error messages
    setError('');

    // Validate email format
    if (!validateEmail(email)) {
      setError('Invalid email format.');
      return;
    }

    try {
      await loginUser(email, password);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.errors && err.response.data.errors.non_field_errors) {
        setError(err.response.data.errors.non_field_errors[0]);
      } else {
        setError('Login failed. Please check your email and password.');
      }
    }
  };

  return (
    <Container maxWidth="xs" style={{ marginTop: '2rem' }}>
      <Paper elevation={3} style={{ padding: '2rem', backgroundColor: 'white' }}>
        <Typography variant="h4" align="center" gutterBottom>Login</Typography>
        {error && <Alert severity="error">{error}</Alert>}
        <form onSubmit={handleSubmit}>
          <TextField
            label="Email"
            type="email"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <TextField
            label="Password"
            type="password"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Login
          </Button>
        </form>
        <Typography align="center" style={{ marginTop: '1rem' }}>
          <Link component={RouterLink} to="/register">Don't have an account? Register</Link>
        </Typography>
      </Paper>
    </Container>
  );
};

export default Login;
