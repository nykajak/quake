<script setup>
    import { ref } from 'vue';
    import { api } from '@/api';

    import SubjectCard from '../subject/components/SubjectCard.vue';
    const props = defineProps(['uid','sid'])
    const subject = ref(null);

    async function fetchSubject(){
        try{
            let res = await api.get(`/admin/subjects/${props.sid}`);
            subject.value = res.data.payload;
        }

        catch(err){
            console.log(err);
            return -1
        }
    }
    
    fetchSubject();
</script>

<template>
    <template v-if="subject">
        <SubjectCard :subject="subject" :active="true"/>
        <div class="chapters">
            <div class="d-flex flex-column align-items-start m-2 w-100 border" v-for="chapter in subject.chapters">
                <h3>
                    {{chapter.name}}
                </h3>
            </div>
        </div>
    
    </template>
</template>

<style scoped>
.chapters{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1em;
    flex-grow: 1;
    border-top: 1px solid light-dark(var(--dark-color),var(--light-color));
}
</style>