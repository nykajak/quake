<script setup>

import { defineProps,ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const props = defineProps(['type','pages'])

const router = useRouter();
const route = useRoute();

let startPage = 1;
if (route.query.page){
    let page = Number(route.query.page)
    if (page - 2 >= 1 && page + 2 <= props.pages){
        startPage = page - 2;
    }
    else if (page - 2 < 1){
        startPage = 1;
    }
    else{
        startPage = props.pages - 4;
    }
}

</script>

<template>
    <div class="d-flex flex-row">
        <div class="d-flex align-items-center" v-if="startPage > 1">
            ---
        </div>
            <div class="p-2" v-for="n in 5">
                <template v-if="startPage + n - 1 <= props.pages && 1 <= startPage + n - 1">
                    <button @click="() => {
                        router.push({path: `/admin/${type}`, query : {
                        ...route.query,
                        'page': startPage + n - 1
                    }})
                    }" :class="{current:startPage + n - 1 == (route.query.page ?? 1)}">
                        {{ startPage + n - 1 }}
                    </button>
                </template>
            </div>
        <div class="d-flex align-items-center" v-if="startPage < props.pages - 4">
            ---
        </div>
    </div>  
</template>

<style scoped>
.current {
    color: var(--light-color);
    background-color: var(--secondary-color);
}
</style>