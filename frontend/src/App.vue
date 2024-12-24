<script setup>
  import { api } from './api';

  async function sendReq(){
    try{
      let f = new FormData()
      f.set("username", "Nykaj")
      f.set("password", "123456")
      let res = await api.post("/login",f);

      // let res = await api.post("/logout");
      return res.data.msg
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

  // sendReq().then((data) => {
  //   console.log(data);
  //   access().then((x)=>{
  //     console.log(x)
  //   })
  // })
  sendReq().then((data) =>{
    console.log(data)
  })
  access().then((x)=>{
      console.log(x)
    })
</script>

<template>
  <button class="btn btn-danger" @click="access">Click!</button>
</template>

<style scoped>
</style>
