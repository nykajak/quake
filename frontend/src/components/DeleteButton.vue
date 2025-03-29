<!-- Renders a button that deletes a particular component! -->
<script setup>
    
    import { useRouter } from 'vue-router';
    import { api } from '@/api';
    const props = defineProps(['redirect','url','color'])
    const router = useRouter();

    async function deleteConfirm(){
        let x = confirm("Confirm deletion?")
        if (x){
            let res = await api.delete(props.url);
            router.push({
                'path' : props.redirect
            })
        }
    }
</script>

<template>
    <button :class="['base-button',props.color+'-button'] " @click="deleteConfirm">
        <slot></slot>
    </button>
</template>

<style scoped>
.base-button{
    display: flex;
    border: none;
    padding: 0.5em;
    color: var(--light-color);
}

.primary-button{
    background-color: var(--primary-color);
}

.secondary-button{
    background-color: var(--secondary-color);
}


.error-button{
    background-color: var(--error-color);
}

</style>