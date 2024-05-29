import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import Login from './pages/Login';
import Admin from './pages/Admin';
import User from './pages/User';
import AllUsers from './pages/AllUsers';
import AllTravelPlans from './pages/AllTravelPlans';
import TravelPlansForUser from './pages/TravelPlansForUser';
import UserBookings from './pages/UserBookings';
import Register from './pages/Register';
import HelloWorld from './pages/HelloWorld';
import './index.css';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<HelloWorld />} />
          <Route path="/register" element={<Register />} />
          <Route element={<PrivateRoute />}>
            <Route path="/admin" element={<Admin />} />
            <Route path="/user" element={<User />} />
            <Route path="/admin/users" element={<AllUsers />} />
            <Route path="/admin/travel-plans" element={<AllTravelPlans />} />
            <Route path="/user/travel-plans" element={<TravelPlansForUser />} />
            <Route path="/user/bookings" element={<UserBookings />} />
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
