<script setup>
  import { RouterView } from 'vue-router';
</script>

<template>
  <div class="container-div">
    <RouterView/>
  </div>
</template>

<style scoped>

.container-div {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  height: 100vh;
}
</style>
