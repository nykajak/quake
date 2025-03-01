import axios from 'axios'

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