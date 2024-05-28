import React, { useState } from 'react';
import { Container, Typography, TextField, Button, Modal, Box } from '@mui/material';
import axiosInstance from '../utils/AxiosInstance';

const EditTravelPlan = ({ open, handleClose, plan, onPlanUpdated }) => {
  const [destination, setDestination] = useState(plan.destination);
  const [description, setDescription] = useState(plan.description);
  const [cost, setCost] = useState(plan.cost);
  const [alert, setAlert] = useState({ show: false, message: '', severity: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.put(`/travel_plan_edit/${plan.id}/`, { destination, description, cost });
      onPlanUpdated(response.data);
      setAlert({ show: false, message: '', severity: '' });
    } catch (error) {
      setAlert({ show: true, message: `Updating plan failed! ${error.response?.data?.message || ''}`, severity: 'error' });
    }
  };

  return (
    <Modal open={open} onClose={handleClose}>
      <Box sx={modalStyle}>
        <Container>
          <Typography variant="h4" gutterBottom>Edit Travel Plan</Typography>
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
              Save Changes
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

export default EditTravelPlan;
