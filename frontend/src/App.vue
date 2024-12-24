<script setup>
  import axios from 'axios'

  async function sendReq(){
    try{
      let res = await axios.get("http://localhost:5000");
      return res.data.msg
    }
    catch{
      return 1
    }
  }

  sendReq().then((data) => {
    console.log(data);
  })
</script>

<template>
  <button class="btn btn-danger">Click!</button>
</template>

<style scoped>
</style>
