<script setup>
    const props = {
        "response": {
            "user": {
                "id": 1,
                "name": "Username",
            },
            "quiz": {
                "id": 1,
                "description": "Quiz description",
            },
            "question": {
                "description" : "What is 1 + 1?",
                "marks": 1,
                "options": [
                    "1",
                    "2",
                    "3",
                    "4"
                ],
                "correct": 1 
            },
            "marked": 1,
            "answered_at": {
                "day": "31",
                "month": "10",
                "year": "2004",
                "hour": "15",
                "minute": "26",
            }
        }
    }
</script>

<template>
    <div class="d-flex flex-column mt-3 align-items-center">
        <!-- Header and metadata -->
        <div class="w-100 border">
            <div class="d-flex justify-content-between">
                <div class="d-flex p-2 m-1">
                    {{ props.response.user.name }}
                </div>
                <div class="d-flex p-2 m-1">
                    Timestamp:
                    {{ props.response.answered_at.hour }}:{{ props.response.answered_at.minute }}
                    on
                    {{ props.response.answered_at.day }}/{{ props.response.answered_at.month }}/{{ props.response.answered_at.year }}
                </div>
            </div>
            
            <div class="d-flex align-items-center flex-column">
                <div>
                    Quiz ID: {{ props.response.quiz.id }}
                </div>
                <div>
                    {{ props.response.quiz.description }}
                </div>
            </div>
        </div>

        <div class="d-flex w-100 flex-column align-self-center m-1 p-1">

            <!-- Question body -->
            <div class="question-container">
                    <div class="question-no-div">
                        <div>
                            Q{{ props.response.question.id }}
                        </div>
                    </div>
                    <div class="question-statement-div">
                        {{ props.response.question.description }}
                    </div>
                    </div>
                    
                    <div class="option-container">
                        <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                            <div class="option-button">
                                <div :class="{'rounded-div':true, 'selected-option':props.response.question.correct == 0}">
                                    A
                                </div>
                                <div class="option-text">
                                    {{ props.response.question.options[0] }}
                                </div>
                            </div>
                
                            <div class="option-button">
                                <div :class="{'rounded-div':true, 'selected-option':props.response.question.correct == 1}">
                                    B
                                </div>
                                <div class="option-text">
                                    {{ props.response.question.options[1] }}
                                </div>
                            </div>
                
                            <div class="option-button">
                                <div :class="{'rounded-div':true, 'selected-option':props.response.question.correct == 2}">
                                    C
                                </div>
                                <div class="option-text">
                                    {{ props.response.question.options[2] }}
                                </div>
                            </div>
                
                            <div class="option-button">
                                <div :class="{'rounded-div':true, 'selected-option':props.response.question.correct == 3}">
                                    D
                                </div>
                                <div class="option-text">
                                    {{ props.response.question.options[3] }}
                                </div>
                            </div>
                        </div>
                </div>
        </div>

        <!-- Answer -->
    </div>
</template>

<style scoped>

#edit-button{
    border: 1px solid var(--light-color);
    color: var(--light-color);
    background-color: var(--tertiary-color);
    padding: 0.5em;
    border-radius: 10px;
}

.option-button:has(.selected-option){
    input{
        background-color: green !important;
        border-color: green !important;    
        transition: none;
    }
    background-color: green !important;
}

.selected-option{
    background-color: green !important;
}

.question-container{
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 1px solid var(--light-color);
    padding: 0.33em;
    color: var(--light-color);
    background-color: var(--secondary-color);
}

.question-no-div{
    display: flex;
    flex-direction: row;
    height: 100%;
    margin: 0.33em;
    padding: 0.33em;
}

.question-no-div div{
    display: flex;
    border: 1px solid var(--light-color);
    width: 2em;
    height: 2em;
    justify-content: center;
    align-items: center;
    border-radius: 100%;
}

.question-statement-div{
    display: flex;
    justify-content: center;
    flex-grow: 1;
    text-align: center;
}

.option-container{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    margin-top: 2em;
}

.option-text{
    justify-content: center;
    display: flex;
    flex-grow: 1;
}

.option-button{
    max-width: 25%;
    display: flex;
    flex-grow: 1;
    justify-content: center;
    align-items: center;
    padding: 0.5em;
    margin: 0.5em;
    color: var(--light-color);
    border: 1px solid var(--light-color);
    background-color: var(--secondary-color);
    border-radius: 1em;
}

.rounded-div{
    border: 1px solid var(--light-color);
    border-radius: 100%;
    width: 1.5em;
    height: 1.5em;
    display: flex;
    flex-shrink: 0;
    justify-content: center;
    align-items: center;
    margin: 0.33em;
}
</style>