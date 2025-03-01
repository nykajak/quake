import axios from 'axios'

export let api = axios.create({
    withCredentials: true,
    baseURL: "http://localhost:5000/",
 });

 api.defaults.headers.common = {
    'X-CSRF-TOKEN': document.cookie.split("=")[1]
  };