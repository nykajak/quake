<script setup>
    import { useRouter, useRoute } from 'vue-router';
    const props = defineProps(['length','beforeSubmit','current','url'])
    const router = useRouter();
    const route = useRoute();
</script>

<template>
    <div class="d-flex flex-row flex-wrap justify-content-center align-items-center">
        <div class="d-flex flex-column p-2" v-for="n in length">
            <div>
                <button :class="props.current == n ? 'current-button': 'nav-button'" @click="
                    beforeSubmit();
                    router.push(
                        {
                            'path': `${props.url}/${n}`
                        }
                    )
                ">
                    {{ n }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.nav-button{
    width: 2.5em;
    background-color: var(--secondary-color);
    color: var(--light-color);
    border: none;
    border-radius: 5px;
}

.current-button{
    width: 2.5em;
    color: var(--light-color);
    border: none;
    border-radius: 5px;
    background-color: var(--primary-color);
}
</style>