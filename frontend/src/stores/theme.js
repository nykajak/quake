import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  let theme = ref(localStorage.getItem("theme") || "dark")

  function toggle() {
    if (theme.value == "dark"){
      theme.value = "light"
      localStorage.setItem("theme","light")
    }
    else{
      theme.value = "dark"
      localStorage.setItem("theme","dark")
    }
  }

  return { theme, toggle }
})
