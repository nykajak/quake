import axios from 'axios'
import router from './router';

// Backend API instantiation
export let api = axios.create({
   withCredentials: true,
   baseURL: "http://localhost:5000/",
});

// Attaching CSRF token before sending to backend (required for POST)
api.interceptors.request.use(
   config => {
      config.headers['X-CSRF-TOKEN'] = document.cookie.split("=")[1]
      return config
   }
)

// Handling unauthorised action
api.interceptors.response.use(response => {
   return response;
},(error) => {
   if ((error.response && error.response.status === 401) || error.status == 401) {
      console.log(error)
      router.push({
         'path': '/login'
      })
   }
   return Promise.reject(error);
});