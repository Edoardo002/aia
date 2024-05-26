<script setup>

defineProps({
  modelName: String,
  modelDescription: String,
  modelType: String,
  modelId: String
})

</script>

<template>

<div class="card-container">
      <a class="hero-image-container">
        <img class="hero-image" src="https://appmaster.io/api/_files/oeHrNPjB9CSUTM4HTfypjP/download/" alt="Spinning glass cube"/>
      </a>
      <main class="main-content">
        <h1>{{ modelName }}</h1>
        <p>Description of the chatbot</p>
        <div class="flex-row">
          <div class="coin-base">
            <img src="https://cdn-icons-png.freepik.com/256/10321/10321703.png" alt="Ethereum" class="small-image"/>
            <h2>OpenAI</h2>
          </div>
          <div class="time-left">
            <img src="https://i.postimg.cc/prpyV4mH/clock-selection-no-bg.png" alt="clock" class="small-image"/>
            <p>2 hours ago</p>
          </div>
        </div>
      </main>
</div>

</template>

<style>
/* 
s
Eye view

https://i.postimg.cc/9MtT4GZY/view.png' border='0' alt='view */

/*
=========================
Font Styling
=========================
*/

h1 {
    font: var(--var-heading);
    color: var(--var-lightest);
    padding-bottom: 0.2em;
    padding-top: 0.5rem;
}

h2 {
    font: var(--var-small-heading);
    color: var(--var-lightest);
    padding-top: 0.2rem;
    /* padding on .coin-base */
}

p {
    font: var(--var-para);
    color: var(--var-soft-blue);
    padding-top: 0.2rem;
}

span {
    color: white;
}
/* 
=====================
Classes
=====================
*/

/* LAYOUT */

.card-container {
    width: 100%;
    max-width: 400px;
    margin: 2em auto;
    background-color: var(--var-card-dark);
    border-radius: 15px;
    margin-bottom: 1rem;
    padding: 1.5rem;
	background-image: linear-gradient(
		135deg,
		#586164,
		#4a5b73 0.5%,
		#3a4555 2%,
		hsl(216, 50%, 16%) 100%
	);
}

div.flex-row {
    display: flex;
    justify-content: space-between;
    align-items: start;
}

div.coin-base, .time-left, .card-attribute {
    display: flex;
    align-items:start;
    padding: 0.2rem
}

a.hero-image-container {
    position: relative;
    display: block;
}



/* Details */

img.eye {
    position: absolute;
    width: 100%;
    max-width: 2em;
    top: 44%;
    left: 43%;
}

@media (min-width:400px) {
  img.eye {
    max-width: 3em;
}
}

.hero-image-container::after {
    content: '';
    background-image: url("https://i.postimg.cc/9MtT4GZY/view.png");
    background-position: center;
    background-repeat: no-repeat;
    background-size: 5rem;
    background-color: hsla(178, 100%, 50%, 0.3);
    width: 100%;
    height: 100%;
    border-radius: 1rem;
    position: absolute;
    top: 0;
    left: 0;
    display: block;
    z-index: 2;
    opacity: 0;
    transition: opacity 0.3s ease-out;
}

.hero-image-container:hover::after {
  opacity: 1;
}

.small-image {
    width: 1.2em;
    margin-right: 0.5em;
}

.small-avatar {
    width: 2em;
    border-radius: 200px;
    outline: 2px solid white;
    margin-right: .4em;
}

@media (min-width:600px) {
    body {
        font-size: 10;
    }
}
</style>