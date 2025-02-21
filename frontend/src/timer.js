import { ref } from "vue"

export function useTimer(initialTime){
    let time = ref(initialTime);

    let id = setInterval(() => {
        if (time.value > 0){
            time.value = time.value - 1;
        }
        else{
            clearInterval(id);
        }
    },1000)
    return {time}
}