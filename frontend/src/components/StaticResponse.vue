<script setup>
    import { RouterLink,useRouter } from 'vue-router';

    import StaticQuestion from './StaticQuestion.vue';
    import StaticOptions from './StaticOptions.vue';

    const props = defineProps(['response'])
    const router = useRouter();
</script>

<template>
    <div class="mt-4 mb-4">
        <div class="metadata">
            <div v-if="props.response.user">
                <button class="nav-button" @click="router.push({
                    'path': `/admin/users/${props.response.user.id}`
                })">
                    {{ props.response.user.name }}
                </button>
            </div>

            <div v-if="props.response.quiz">
                <button class="nav-button" @click="router.push({
                    'path': `/admin/subjects/${props.response.quiz.chapter.subject.id}/chapters/${props.response.quiz.chapter.id}/quizes/${props.response.quiz.id}`
                })">
                    Quiz #{{ props.response.quiz.id }}
                </button>
            </div>

            <div>
                {{ props.response.dated.day }}/{{ props.response.dated.month }}/{{ props.response.dated.year }}
                at
                {{ props.response.dated.hour }}:{{ props.response.dated.minute }}
            </div>
        </div>
        <StaticQuestion :description="props.response.question.description"/>
        <StaticOptions :question="props.response.question" :marked="props.response.marked"/>
    </div>
</template>

<style scoped>
.nav-button{
    display: flex;
    background-color: var(--primary-color);
    border:none;
    color: var(--light-color);
}

.metadata{
    display: flex;
    justify-content: space-between;
    background-color: var(--primary-color);
    color: var(--light-color);
    padding-left: 1em;
    padding-right: 1em;
}
</style>
