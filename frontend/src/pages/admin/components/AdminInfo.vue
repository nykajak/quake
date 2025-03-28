<script setup>
    import NavButton from '@/components/NavButton.vue';
</script>

<template>
    <div class="d-flex flex-column w-100 mt-2 align-items-center">
        <h3 id="greeting-text">
            Welcome Jakyn!
        </h3>
        <p id="secondary-text">
            What would you like to do today?
        </p>

        <div class="d-flex">
            <NavButton text="Monitor Users" color="primary" url="/admin/users"/>
            <NavButton text="Manage Subjects" color="secondary" url="/admin/subjects"/>
            <NavButton text="View applications" color="tertiary" url="/admin/requests"/>
        </div>

    </div>
</template>

<style scoped>
#greeting-text{
    font-size: 2.3em;
}

#secondary-text{
    color: var(--contrast-color)
}
</style>