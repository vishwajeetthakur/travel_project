import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import jwtDecode from 'jwt-decode';
import axiosInstance from '../utils/AxiosInstance';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
  );
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const initAuth = async () => {
      if (authTokens) {
        try {
          setUser(jwtDecode(authTokens.access));
          axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${authTokens.access}`;
        } catch (error) {
          console.log("Token decode failed, possibly due to expiration or tampering: ", error);
          logoutUser();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const loginUser = async (email, password) => {
    try {
      const response = await axiosInstance.post('/login/', { email, password });
      const data = response.data;
      setAuthTokens(data.token);  // Store the token object that includes both access and refresh tokens
      setUser(jwtDecode(data.token.access));
      localStorage.setItem('authTokens', JSON.stringify(data.token));  // Ensure the entire token object is stored
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${data.token.access}`;
      navigate(data.msg.includes('Admin') ? '/admin' : '/user');
    } catch (error) {
      console.error('Login failed:', error);
      throw error;  // Re-throw the error to be handled in the calling function
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    axiosInstance.defaults.headers.common['Authorization'] = null;  // Clear default Authorization header
    navigate('/login');
  };

  if (loading) {
    return <div>Loading...</div>;  // Show a loading message or a spinner
  }

  const contextData = {
    user,
    authTokens,
    loginUser,
    logoutUser,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
