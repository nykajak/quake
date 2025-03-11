import axios from 'axios'
import router from './router';

export let api = axios.create({
    withCredentials: true,
    baseURL: "http://localhost:5000/",
 });

 api.interceptors.request.use(
   config => {
      config.headers['X-CSRF-TOKEN'] = document.cookie.split("=")[1]
      return config
   }
 )

 api.interceptors.response.use(response => {
   return response;
},(error) => {
  if ((error.response && error.response.status === 401) || error.status == 401) {
      router.push({
         'path': '/login'
      })
  }
//   return error;
});