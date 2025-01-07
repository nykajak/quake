<script setup>
    import Header from '@/components/Header.vue';
    import Branding from '@/components/Branding.vue';
</script>

<template>
    <Header></Header>
    <div class="content">
        <div class="jumbotron jumbotron-fluid">
            <div class="container-fluid marketing text-center">
                <h1 class="display-1">Quake</h1>
                <p class="lead">
                    Your one stop solution for all your quizzing needs!
                </p>
            </div>
        </div>
        <Branding/>
    </div>
</template>

<style scoped>
.content{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    color: var(--light-color);
}

.marketing {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 1em;
    background-image: linear-gradient(to bottom right,  light-dark( var(--primary-color),var(--dark-color)),  light-dark( var(--secondary-color),var(--contrast-color)));
}
</style>