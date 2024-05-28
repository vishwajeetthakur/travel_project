import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';
import Login from './pages/Login';
import Admin from './pages/Admin';
import User from './pages/User';
import AllUsers from './pages/AllUsers';
import AllTravelPlans from './pages/AllTravelPlans';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route 
            path="/admin" 
            element={
              <PrivateRoute>
                <Admin />
              </PrivateRoute>
            }
          />
          <Route 
            path="/user" 
            element={
              <PrivateRoute>
                <User />
              </PrivateRoute>
            }
          />
          <Route 
            path="/admin/users" 
            element={
              <PrivateRoute>
                <AllUsers />
              </PrivateRoute>
            }
          />
          <Route 
            path="/admin/travel-plans" 
            element={
              <PrivateRoute>
                <AllTravelPlans />
              </PrivateRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
