<script setup>
    import AnonHeader from './components/AnonHeader.vue';
</script>

<template>
    <AnonHeader></AnonHeader>
    <div class="content">
        <div class="jumbotron jumbotron-fluid">
            <div class="container-fluid marketing text-center">
                <h1 class="display-1">Quake</h1>
                <p class="lead">
                    Your one stop solution for all your quizzing needs!
                </p>
            </div>
        </div>
        
        <div class="content2">
            <div class="question">
                <h1 class="question-text">Q. What does Quake have to offer?</h1>
                <p>
                    It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
                </p>
            </div>
            <div class="options">
                <div class="option">
                    <button class="option-letter">A</button>
                    <div class="option-text">
                        Timed quizes and mock tests
                    </div>
                </div>
                <div class="option">
                    <button class="option-letter">B</button>
                    <div class="option-text">
                        Support for a wide range of exams
                    </div>
                </div>
                <div class="option">
                    <button class="option-letter">C</button>
                    <div class="option-text">
                        Feedback and course management help
                    </div>
                </div>
                <div class="option" id="correct-option">
                    <button class="option-letter" id="correct-letter">D</button>
                    <div class="option-text" id="correct-text">
                        All of the above
                    </div>
                </div>
            </div>
        </div> 
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
    background-image: linear-gradient(to bottom right, var(--primary-color),  var(--secondary-color));
}


#correct-option{
    border: 1px solid green;
}

#correct-text{
    color: green;
}

#correct-letter{
    background-color: green;
}

.question-text{
    font-size: 2.5em;
}

.content2{
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    padding-top: 2em;
}

.question {
    display: flex;
    flex-direction: column;
    padding: 0.5em;
    color: light-dark(var(--dark-color),var(--light-color));
    align-items: center;
    width: 650px;
    justify-content: center;
}

.option{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    padding: 1em;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
    border-radius: 5px;
    margin: 1em 0 0;
}

.option-letter {
    font-weight: bold;
    text-align: center;
    justify-content: center;
    align-items: center;
    border-radius: 100%;
    width: 2em;
    height: 2em;
    border: 1px solid light-dark(var(--dark-color),var(--light-color));
}

.option-text{
    font-weight: bold;
    display: flex;
    align-items: center;
    padding-left: 1em;
    flex-grow: 1;
    text-align: start;
    color : light-dark(var(--dark-color), var(--light-color));
}

</style>