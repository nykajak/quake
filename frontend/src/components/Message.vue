<script setup>
    import { ref } from 'vue';
    const props = defineProps(['text','hideFunction','level'])
    let time = ref(5);

    let id = setInterval(()=>{
        if (time.value > 0){
            time.value -= 1
        }
        else{
            props.hideFunction()
            clearInterval(id);
        }
    },1000)
</script>

<template>
    <div class="d-flex justify-content-center">
        <div :class="['outerMessage',props.level]">
            <div class="innerMessage">
                <slot></slot>
            </div>
            <div class="closeButtonDiv">
                <button class="closeButton" @click="props.hideFunction">
                    x   
                </button>
            </div>
        </div>
    </div>
</template>

<style>
.outerMessage{
    display: flex;
    width: fit-content;
    padding: 0.3em;
    padding-left: 0.7em;
    padding-right: 0.7em;
    margin: 0.2em;
    border-radius: 10px;
    gap: 1em;
    z-index: 2;
}

.info{
    background-color: var(--secondary-color);
}

.warning{
    background-color: var(--primary-color);
}

.danger{
    background-color: var(--error-color);
}

.innerMessage{
    display: flex;
    flex-direction: row;
    flex-grow: 1;
    justify-content: center;
    color: var(--light-color);
}

.closeButtonDiv{
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--light-color);
}


.closeButton{
    display: flex;
    border:none;
    height: 1.2em;
    align-items: center;
    color: var(--light-color);
}

.info .closeButton{
    background-color: var(--secondary-color);
}

.warning .closeButton{
    background-color: var(--primary-color);
}

.danger .closeButton{
    background-color: var(--error-color);
}

</style>