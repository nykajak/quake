<script setup>
</script>

<template>
    <div class="d-flex w-100 flex-column align-self-center m-1 p-1">
        <div class="question-container">
            <div class="question-no-div">
                <div>
                    Q9
                </div>
            </div>
            <div class="question-statement-div">
                It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
            </div>
        </div>
        
        <div class="option-container">
            <div class="d-flex flex-row justify-content-center flex-wrap w-100">
                <button class="option-button">
                    <div class="rounded-div">
                        A
                    </div>
                    <div class="option-text">
                        Option A
                    </div>
                </button>
    
                <button class="option-button">
                    <div class="rounded-div">
                        B
                    </div>
                    <div class="option-text">
                        Option B
                    </div>
                </button>
    
                <button class="option-button">
                    <div class="rounded-div">
                        C
                    </div>
                    <div class="option-text">
                        Option C
                    </div>
                </button>
    
                <button class="option-button">
                    <div class="rounded-div">
                        D
                    </div>
                    <div class="option-text">
                        Option D
                    </div>
                </button>
            </div>
        </div>
    </div>

</template>

<style scoped>

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

.option-button:hover{
    background-color: var(--primary-color);
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