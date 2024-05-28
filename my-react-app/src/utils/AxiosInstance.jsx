import axios from 'axios';

let refresh = false;

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api',  // Ensure this matches your backend URL
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,  // Apply withCredentials to all requests
});

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response.status === 401 && !refresh) {
      refresh = true;
      const authTokens = JSON.parse(localStorage.getItem('authTokens'));
      const refreshToken = authTokens?.refresh;

      try {
        const response = await axiosInstance.post('/token/refresh/', { refresh: refreshToken });

        if (response.status === 200) {
          const newTokens = {
            access: response.data.token.access,
            refresh: response.data.token.refresh
          };
          localStorage.setItem('authTokens', JSON.stringify(newTokens));
          axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${newTokens.access}`;
          error.config.headers['Authorization'] = `Bearer ${newTokens.access}`;
          refresh = false;
          return axiosInstance(error.config);
        }
      } catch (refreshError) {
        console.error('Error refreshing token:', refreshError);
        localStorage.removeItem('authTokens');
        window.location.href = '/login';
      }
    }

    refresh = false;
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.request.use(
  (config) => {
    const authTokens = JSON.parse(localStorage.getItem('authTokens'));
    if (authTokens) {
      config.headers.Authorization = `Bearer ${authTokens.access}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default axiosInstance;
