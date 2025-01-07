<script>

</script>

<template>

    <div class=" d-flex justify-content-center">
        <div class="slideshow">
            
        </div>
    </div>

    <div class="slideshow-control-div">
        <button class="slideshow-control" @click="page=(page+2)%3">&lt;</button>
    </div>
    
    <div v-if="page==0" class="slideshow-item">
        <div class="slideshow-header">
            <div class="slideshow-symbol">
                <h3>?</h3>
            </div>
            <div class="slideshow-question">
                <h3>Our mission</h3>
            </div>
        </div>
        <div class="slideshow-answer">
            <p>
                Revolutionise exam preparation by making 
            </p>
        </div>
    </div>
    
    <div v-else-if="page==1" class="slideshow-item">
        <div class="slideshow-header">
            <div class="slideshow-symbol">
                <h3>?</h3>
            </div>
            <div class="slideshow-question">
                <h3>Why choose us?</h3>
            </div>
        </div>
        <div class="slideshow-answer">
            <p>
                Answer to question 2 given here!
            </p>
        </div>
    </div>
    
    <div v-else-if="page==2" class="slideshow-item">
        <div class="slideshow-header">
            <div class="slideshow-symbol">
                <h3>?</h3>
            </div>
            <div class="slideshow-question">
                <h3>Question 3</h3>
            </div>
        </div>
        <div class="slideshow-answer">
            <p>
                Answer to question 3 given here!
            </p>
        </div>
    </div>
    
    <div class="slideshow-control-div">
        <button class="slideshow-control" @click="page=(page+1)%3">&gt;</button>
    </div>
</template>

<style scoped>

.slideshow{
    width: 40%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: stretch;
}

.slideshow-control{
    display: flex;
    height: 100%;
    align-items: center;
}

.slideshow-item{
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    width: 100%;
    justify-content: center;
    align-items: center;
}

.slideshow-header{
    display: flex;
    flex-direction: row;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    text-align: center;
}

.slideshow-symbol{
    flex-grow: 1;
}

.slideshow-question{
    flex-grow: 5;
    background-color: light-dark(var(--light-color),var(--secondary-color));
}

.slideshow-answer{
    display: flex;
    flex-direction: column;
    padding: 1em;
}

</style>