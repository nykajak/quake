import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref("dark")
  function toggle() {
    if (theme.value == "dark"){
      theme.value = "light"
    }
    else{
      theme.value = "dark"
    }
  }

  return { theme, toggle }
})
