<script setup>

</script>

<template>

<div class="card-container">
      <a href="/" class="hero-image-container">
        <img class="hero-image" src="https://i.postimg.cc/NfR2yhNs/image-equilibrium.jpg" alt="Spinning glass cube"/>
      </a>
      <main class="main-content">
        <h1><a href="#">Equilibrium #3429</a></h1>
        <p>Our Equilibrium collection promotes balance and calm.</p>
        <div class="flex-row">
          <div class="coin-base">
            <img src="https://i.postimg.cc/T1F1K0bW/Ethereum.png" alt="Ethereum" class="small-image"/>
            <h2>0.041 ETH</h2>
          </div>
          <div class="time-left">
            <img src="https://i.postimg.cc/prpyV4mH/clock-selection-no-bg.png" alt="clock" class="small-image"/>
            <p>3 days left</p>
          </div>
        </div>
      </main>
      <div class="card-attribute">
        <img src="https://i.postimg.cc/SQBzNQf1/image-avatar.png" alt="avatar" class="small-avatar"/>
        <p>Creation of <span><a href="#">Jules Wyvern</a></span></p>
      </div>
</div>
<div class="attribution">
    Challenge by <a href="https://www.frontendmentor.io?ref=challenge" target="_blank">Frontend Mentor</a>. 
    Coded by <a href="#">Lauro235</a>.
</div>

</template>

<style>
/* 

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
    padding: 1.2em 0;
}

h2 {
    font: var(--var-small-heading);
    color: var(--var-lightest);
    /* padding on .coin-base */
}

p {
    font: var(--var-para);
    color: var(--var-soft-blue);
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
    width: 30%;
    max-width: 400px;
    margin: 2em auto;
    background-color: var(--var-card-dark);
    border-radius: 15px;
    margin-bottom: 1rem;
    padding: 2rem;
	background-image: linear-gradient(
		135deg,
		#752e7c 1%,
		#734a58 10%,
		#1b2028 30%,
		hsl(216, 50%, 16%) 100%
	);
}

div.flex-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

div.coin-base, .time-left, .card-attribute {
    display: flex;
    align-items:center;
    padding: 1em 0;
}

.card-attribute {
    padding-bottom: 1.5em;
    border-top: 2px solid var(--var-line-dark);
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
    margin-right: .5em;
}

.small-avatar {
    width: 2em;
    border-radius: 200px;
    outline: 2px solid white;
    margin-right: 1.4em;
}

div.attribution {
    margin: 0 auto;
    width: 100%;
    font: var(--var-para);
    text-align: center;
    padding: 1.5em 0 4em 0;
    color: var(--var-line-dark);
}
.attribution a {
    color: var(--var-soft-blue);
}

@media (min-width:600px) {
    body {
        font-size: 18px;
    }
}
</style>