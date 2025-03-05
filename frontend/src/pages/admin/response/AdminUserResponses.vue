<script setup>
    import { api} from '@/api';
    import { ref } from 'vue';
    
    import StaticResponse from '@/components/StaticResponse.vue';

    const props = defineProps(['uid'])
    const responses = ref(null);

    async function fetchResponses(){
        let res = await api.get(`/admin/responses/?user_id=${props.uid}`);
        responses.value = res.data.payload;
    }

    fetchResponses()
</script>

<template>
    <div v-if="responses">
        <div v-for="r in responses">
            <StaticResponse :response="r"/>
        </div>
    </div>
</template>

<style scoped>

</style>