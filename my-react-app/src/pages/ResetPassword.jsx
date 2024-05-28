import React, { useState, useEffect } from 'react';
import { TextField, Button, Alert, Container, Typography, Box, Dialog } from '@mui/material';
import axiosInstance from '../utils/AxiosInstance';

const ResetPassword = ({ open, handleClose }) => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    if (!open) {
      setOldPassword('');
      setNewPassword('');
      setConfirmNewPassword('');
      setError('');
      setSuccess('');
    }
  }, [open]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (newPassword !== confirmNewPassword) {
      setError('New password and confirm new password do not match.');
      return;
    }

    try {
      const response = await axiosInstance.post('/change-password/', {
        old_password: oldPassword,
        new_password: newPassword,
        confirm_new_password: confirmNewPassword
      });

      setSuccess('Password changed successfully!');
      handleClose();
    } catch (error) {
      if (error.response && error.response.data) {
        setError(error.response.data.errors || 'An error occurred.');
      } else {
        setError('An error occurred.');
      }
    }
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <Container maxWidth="sm">
        <Box mt={5}>
          <Typography variant="h4" component="h1" gutterBottom>
            Reset Password
          </Typography>
          {error && <Alert severity="error">{error}</Alert>}
          {success && <Alert severity="success">{success}</Alert>}
          <form onSubmit={handleSubmit}>
            <TextField
              label="Old Password"
              type="password"
              fullWidth
              margin="normal"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              required
            />
            <TextField
              label="New Password"
              type="password"
              fullWidth
              margin="normal"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
            <TextField
              label="Confirm New Password"
              type="password"
              fullWidth
              margin="normal"
              value={confirmNewPassword}
              onChange={(e) => setConfirmNewPassword(e.target.value)}
              required
            />
            <Box mt={2} mb={5}>
              <Button type="submit" variant="contained" color="primary" fullWidth>
                Change Password
              </Button>
            </Box>
          </form>
        </Box>
      </Container>
    </Dialog>
  );
};

export default ResetPassword;
