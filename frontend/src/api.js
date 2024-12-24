import axios from 'axios'

export let api = axios.create({
    withCredentials: true,
    baseURL: "http://localhost:5000/"
 });