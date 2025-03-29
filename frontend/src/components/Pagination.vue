<!-- Renders a window of divs which ensures user can navigate to any page! -->
<script setup>

import { defineProps,ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const props = defineProps(['url','pages'])

const router = useRouter();
const route = useRoute();

let startPage = 1; // Default start page is 1

// If page no given detect start and end of window.
// Strategy: Keep current page in the middle
if (route.query.page){
    let page = Number(route.query.page)
    
    // If lower and upper bound are valid
    if (page - 2 >= 1 && page + 2 <= props.pages){
        startPage = page - 2;
    }

    // If lower bound is invalid
    else if (page - 2 < 1){
        startPage = 1;
    }

    // If upper bound is invalid
    else{
        startPage = Math.max(props.pages - 4,0);
    }
}

</script>

<template>
    <div class="d-flex flex-row flex-grow-1 justify-content-center">
        <div class="p-2 d-flex align-items-center" v-if="startPage > 1">
            ---
        </div>
            <template v-for="n in 5">
                <template v-if="startPage + n - 1 <= props.pages && 1 <= startPage + n - 1">
                    <div class="p-2">
                        <button @click="() => {
                            router.push({path: `${url}`, query : {
                            ...route.query,
                            'page': startPage + n - 1
                        }})
                        }" :class="{current:startPage + n - 1 == (route.query.page ?? 1)}">
                            {{ startPage + n - 1 }}
                        </button>
                    </div>
                </template>
            </template>
        <div class="p-2 d-flex align-items-center" v-if="startPage < props.pages - 4">
            ---
        </div>
    </div>  
</template>

<style scoped>
.current {
    color: var(--light-color);
    background-color: var(--secondary-color);
}

button {
    border-radius: 5px;
    padding-left: 0.7em;
    padding-right: 0.7em;
}
</style>