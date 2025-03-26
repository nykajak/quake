<!-- Renders a div which displays some important and transient message! -->
<script setup>
    import { ref } from 'vue';

    // hideFunction used to clear logic that renders Message
    const props = defineProps(['hideFunction','level'])

    let time = ref(5); // Time taken for message to vanish

    // Interval to decrement time
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
    <div class="containerMessage">
        <div :class="['outerMessage',props.level]">
            <div class="innerMessage">
                <!-- Content to be displayed! -->
                <slot></slot> 
            </div>
            <div class="closeButtonDiv">
                <button class="closeButton" @click="()=>{
                    time = 5;
                    props.hideFunction()
                }">
                    x   
                </button>
            </div>
        </div>
    </div>
</template>

<style>
.containerMessage{
    position: absolute;
    top:5px;
    left: 50%;
    transform: translate(-50%,0%);
    justify-content: center;
}

.outerMessage{
    display: flex;
    width: fit-content;
    padding: 0.3em;
    padding-left: 0.7em;
    padding-right: 0.7em;
    margin: 0.2em;
    border-radius: 10px;
    gap: 1em;
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
    z-index: 2;
}

.closeButtonDiv{
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--light-color);
    z-index: 2;
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