<script setup>
  import { api } from './api';
  import { RouterView } from 'vue-router';

  async function sendReq(){
    try{
      let f = new FormData()
      f.set("username", "Nykaj")
      f.set("password", "123456")
      let res = await api.post("/login",f);

      // let res = await api.post("/logout");
      return res
    }
    catch{
      return 0
    }
  }

  async function access(){
    try{
      let res = await api.get("/all");
      return res.data
    }
    catch{
      return 0
    }
  }
</script>

<template>
  <RouterView/>
</template>

<style scoped>
</style>
