<script setup>
    import { ref } from 'vue';

    const props = defineProps(['type','values','setVal'])
    const hidden = ref(true);
    const selectedText = ref("");

</script>

<template>
    <div class="d-flex flex-column">
        <div class="dropdown" @click="hidden=!hidden">
            <input id="dropdown-input" type="text" readonly :value="selectedText">
        </div>
        <div class="dropdown-options" v-show="hidden == false && values && values.length > 0">
            <div class="d-flex flex-column">
                <template v-if="props.type == 'question'">
                    <template v-for="val in props.values">
                        <button class="dropdown-button" @click="()=>{
                            props.setVal(val.id);
                            selectedText = val.description
                        }">{{val.description}}</button>
                    </template>
                </template>

                <template v-if="props.type == 'user'">
                    <template v-for="val in props.values">
                        <button class="dropdown-button" @click="()=>{
                            props.setVal(val.id);
                            selectedText = val.name
                        }">{{val.name}}</button>
                    </template>
                </template>
            </div>
        </div>
    </div>
</template>

<style scoped>
#dropdown-input{
    display: flex;
    width: 30em;
}

.dropdown{
    display: flex;
    flex-direction: row;
    gap: 1em;
    anchor-name: --dropdown;
}

.dropdown-options{
    position: absolute;
    position-anchor: --dropdown;
    position-area: bottom center;
    overflow-y: auto;
    height: 5em;
    width: 100%;
    border: 1px solid light-dark(var(--dark-color), var(--light-color));
}

.dropdown-button{
    background-color: light-dark(var(--light-color),var(--dark-color));
    border: none;
}

.dropdown-button:hover{
    background-color: var(--secondary-color);
}
</style>