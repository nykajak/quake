<script setup>
  import axios from 'axios'

  async function sendReq(){
    try{
      let f = new FormData()
      f.set("username", "Nykaj")
      f.set("password", "123456")
      let res = await axios.post("http://localhost:5000/login",f,{ withCredentials: true });

      // let res = await axios.post("http://localhost:5000/logout",new FormData(),{ withCredentials: true });
      return res.data.msg
    }
    catch{
      return 0
    }
  }

  async function access(){
    try{
      let res = await axios.get("http://localhost:5000/all",{ withCredentials: true });
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
