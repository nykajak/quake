<script setup>
    import { api } from '@/api';
    import { ref } from 'vue';
    import { useRoute } from 'vue-router';

    const route = useRoute();
    const users = ref([]);

    async function fetchUsers(){
        let page = route.query["page"] ?? 1;
        let per_page = route.query["per_page"] ?? 5 ;
        let res = await api.get(`/admin/users/?page=${page}&per_page=${per_page}`);
        return res.data.payload
    }

    fetchUsers().then(data => {
        console.log(data);
        users.value = data;
    })

</script>

<template>
    <div v-for="u in users">
        {{ u.name }}
    </div>
</template>

<style scoped>
</style>