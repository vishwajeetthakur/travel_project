import axios from "axios";

let refresh = false;

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response.status === 401 && !refresh) {
      refresh = true;
      const refreshToken = localStorage.getItem("refresh");
      
      try {
        const response = await axios.post(
          "http://localhost:8000/api/token/refresh/",
          {
            refresh: refreshToken,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
            withCredentials: true,
          }
        );
        
        
        if (response.status === 200) {
          axios.defaults.headers.common["Authorization"] = `Bearer ${response.data["token"]["access"]}`;
          localStorage.setItem("access", response.data.token.access);
          localStorage.setItem("refresh", response.data.token.refresh);
          refresh = false;
          return axios(error.config);
        }
      } catch (refreshError) {
        console.error("Error refreshing token:", refreshError);
        // Handle token refresh error
      }
    }

    refresh = false;
    return Promise.reject(error);
  }
);

export default axios;
