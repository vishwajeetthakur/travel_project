import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Button,
  Box
} from '@mui/material';
import axiosInstance from '../utils/AxiosInstance';

const AllTravelPlansForUser = () => {
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
      <Grid container spacing={4}>
        {travelPlans.map((plan) => (
          <Grid item key={plan.id} xs={12} sm={6} md={4}>
            <Card>
              <CardMedia
                component="img"
                height="140"
                width="300"
                image={plan.imageUrl || 'default-image-url.jpg'}
                alt={plan.destination}
              />
              <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                  {plan.destination}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {plan.description}
                </Typography>
                <Box mt={2}>
                  <Typography variant="h6" color="text.primary">
                    Cost: ${plan.cost}
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button 
                  variant="contained" 
                  color="primary" 
                  onClick={() => handleBookClick(plan.id)}
                >
                  Book Plan
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default AllTravelPlansForUser;
