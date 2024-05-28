import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button
} from '@mui/material';
import axiosInstance from '../utils/AxiosInstance';
import EditTravelPlan from './EditTravelPlan'; // Import the new component

const AllTravelPlans = () => {
  const [travelPlans, setTravelPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [editModalOpen, setEditModalOpen] = useState(false);

  useEffect(() => {
    const fetchTravelPlans = async () => {
      try {
        const response = await axiosInstance.get('/get_travel_plan/');
        setTravelPlans(response.data);
      } catch (error) {
        console.error('Failed to fetch travel plans:', error);
      }
    };

    fetchTravelPlans();
  }, []);

  const handleEditClick = (plan) => {
    setSelectedPlan(plan);
    setEditModalOpen(true);
  };

  const handleEditModalClose = () => {
    setEditModalOpen(false);
    setSelectedPlan(null);
  };

  const handlePlanUpdated = (updatedPlan) => {
    setTravelPlans((prevPlans) =>
      prevPlans.map((plan) => (plan.id === updatedPlan.id ? updatedPlan : plan))
    );
    handleEditModalClose();
  };

  const handleDeleteClick = async (planId) => {
    try {
      await axiosInstance.delete(`/travel_plan_delete/${planId}/`);
      setTravelPlans((prevPlans) => prevPlans.filter((plan) => plan.id !== planId));
    } catch (error) {
      console.error('Failed to delete travel plan:', error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>All Travel Plans</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Destination</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Cost</TableCell>
              <TableCell>Edit</TableCell>
              <TableCell>Delete</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {travelPlans.map((plan) => (
              <TableRow key={plan.id}>
                <TableCell>{plan.destination}</TableCell>
                <TableCell>{plan.description}</TableCell>
                <TableCell>{plan.cost}</TableCell>
                <TableCell>
                  <Button variant="contained" color="primary" onClick={() => handleEditClick(plan)}>
                    Edit
                  </Button>
                </TableCell>
                <TableCell>
                  <Button variant="contained" color="secondary" onClick={() => handleDeleteClick(plan.id)}>
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      {selectedPlan && (
        <EditTravelPlan
          open={editModalOpen}
          handleClose={handleEditModalClose}
          plan={selectedPlan}
          onPlanUpdated={handlePlanUpdated}
        />
      )}
    </Container>
  );
};

export default AllTravelPlans;
