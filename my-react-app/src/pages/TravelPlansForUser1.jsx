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

const AllTravelPlansForuser = () => {
  const [travelPlans, setTravelPlans] = useState([]);

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

  const handleBookClick = async (planId) => {
    try {
      const response = await axiosInstance.post(`/user/booking/${planId}`);
      if (response.status === 201) {
        alert('Booking successful!');
      }
    } catch (error) {
      console.error('Failed to book travel plan:', error);
      alert('Booking failed!');
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
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {travelPlans.map((plan) => (
              <TableRow key={plan.id}>
                <TableCell>{plan.destination}</TableCell>
                <TableCell>{plan.description}</TableCell>
                <TableCell>{plan.cost}</TableCell>
                <TableCell>
                  <Button variant="contained" color="primary" onClick={() => handleBookClick(plan.id)}>
                    Book Plan
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default AllTravelPlansForuser;
