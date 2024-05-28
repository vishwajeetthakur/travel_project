import React, { useState } from 'react';
import { Container, Typography, TextField, Button, Modal, Box, Alert } from '@mui/material';
import axiosInstance from '../utils/AxiosInstance';

const AddTravelPlan = ({ open, handleClose }) => {
  const [destination, setDestination] = useState('');
  const [description, setDescription] = useState('');
  const [cost, setCost] = useState('');
  const [alert, setAlert] = useState({ show: false, message: '', severity: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post('/travel_plan/', { destination, description, cost });
      if (response.status === 201) {
        setAlert({ show: true, message: 'Travel plan added successfully!', severity: 'success' });
        setTimeout(() => {
          setAlert({ show: false, message: '', severity: '' });
          handleClose();
        }, 2000);
      }
    } catch (error) {
      setAlert({ show: true, message: `Adding travel plan failed! ${error.response?.data?.message || ''}`, severity: 'error' });
      setTimeout(() => setAlert({ show: false, message: '', severity: '' }), 3000);
    }
  };

  return (
    <Modal open={open} onClose={handleClose}>
      <Box sx={modalStyle}>
        <Container>
          <Typography variant="h4" gutterBottom>Add New Travel Plan</Typography>
          {alert.show && (
            <Alert severity={alert.severity} onClose={() => setAlert({ show: false, message: '', severity: '' })}>
              {alert.message}
            </Alert>
          )}
          <form onSubmit={handleSubmit}>
            <TextField
              label="Destination"
              fullWidth
              margin="normal"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
            />
            <TextField
              label="Description"
              fullWidth
              margin="normal"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
            <TextField
              label="Cost"
              type="number"
              fullWidth
              margin="normal"
              value={cost}
              onChange={(e) => setCost(e.target.value)}
            />
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Add Travel Plan
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

export default AddTravelPlan;
