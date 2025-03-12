import axios from 'axios'
import { useRouter } from 'vue-router';

const router = useRouter();
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

 axios.interceptors.response.use(response => {
   return response;
}, error => {
  if (error.response.status === 401) {
      router.push({
         'path': '/login'
      })
  }
  return error;
});