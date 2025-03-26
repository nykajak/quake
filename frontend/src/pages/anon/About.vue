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
                <h1 class="question-text">What does Quake have to offer?</h1>
                <p>
                    &nbsp;&nbsp;&nbsp;&nbsp;Quake is a novel solution for applicants to give mock quizes for a plethora of subjects to assess their readiness and point out areas requiring improvement for competitive examinations. Multiple choice question based quizes at regular intervals ensure that concepts remain fresh in memory. 
                </p>
                <p>
                    &nbsp;&nbsp;&nbsp;&nbsp;Quake boasts a carefully curated list of questions as well as instant feedback and reviews for user performance on a quiz by quiz basis. A world of learning awaits you!
                </p>
            </div>
            <div class="options">
                <div class="option">
                    <div class="option-letter">A</div>
                    <div class="option-text">
                        Timed quizes and mock tests
                    </div>
                </div>
                <div class="option">
                    <div class="option-letter">B</div>
                    <div class="option-text">
                        Support for a wide range of exams
                    </div>
                </div>
                <div class="option">
                    <div class="option-letter">C</div>
                    <div class="option-text">
                        Feedback and course management help
                    </div>
                </div>
                <div class="option" id="correct-option">
                    <div class="option-letter" id="correct-letter">D</div>
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
    background-color: green;
}

#correct-text{
    color: var(--light-color);
}

#correct-letter{
    background-color: green;
}

.question-text{
    font-size: 2.7em;
    color: var(--secondary-color);
}

p{
    font-size: 1.2em;
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
    background-color: var(--secondary-color);
    border-radius: 5px;
    margin: 1em 0 0;
}

.option-letter {
    display: flex;
    font-weight: bold;
    text-align: center;
    justify-content: center;
    align-items: center;
    border-radius: 100%;
    width: 2em;
    height: 2em;
    background-color: var(--secondary-color);
    color: var(--light-color);
    border: 1px solid var(--light-color);
}

.option-text{
    font-weight: bold;
    display: flex;
    align-items: center;
    padding-left: 1em;
    flex-grow: 1;
    text-align: start;
    color: var(--light-color);
}

</style>