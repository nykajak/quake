<script setup>
    import StaticQuestion from '@/components/StaticQuestion.vue';
    import StaticOption from '@/components/StaticOption.vue';
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
        <div class="metadata border">
            <div class="d-flex justify-content-between">
                <div class="d-flex p-1 m-1">
                    {{ props.response.user.name }}
                </div>
                <div class="d-flex p-1 m-1">
                    Timestamp:
                    {{ props.response.answered_at.hour }}:{{ props.response.answered_at.minute }}
                    on
                    {{ props.response.answered_at.day }}/{{ props.response.answered_at.month }}/{{ props.response.answered_at.year }}
                </div>
            </div>
            
            <div class="d-flex justify-content-between">
                <div class="d-flex p-1 m-1">    
                    Quiz ID: {{ props.response.quiz.id }}
                </div>
                <div class="d-flex p-1 m-1">    
                    {{ props.response.quiz.description }}
                </div>
            </div>
        </div>

        <div class="d-flex w-100 flex-column align-self-center m-1 p-1">
            <StaticQuestion :index="props.response.question.id" :description="props.response.question.description"/>
            <!-- Question body -->
            <!-- <div class="question-container">
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
                </div> -->
        </div>

        <!-- Answer -->
    </div>
</template>

<style scoped>

.metadata{
    width: 100%;
    background-color: var(--secondary-color);
    color: var(--light-color);
}
</style>