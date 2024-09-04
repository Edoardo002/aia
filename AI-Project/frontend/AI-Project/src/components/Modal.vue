<script setup>
defineProps({
  buttonMessage: String,
})
</script>
<template>
	<button class="pm ms-3" onclick="window.dialog.showModal();"> {{ buttonMessage }} </button>
      <dialog id="dialog">
      <slot> </slot>
	        <button onclick="window.dialog.close();" aria-label="close" class="x">❌</button>
      </dialog>
</template>
<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap");
:root {
	--vs-primary: 128 200 0;
}

dialog {
    margin: auto;
	padding: 1rem 3rem;
	background: hsl(216, 50%, 16%);
	max-width: 800px;
	padding-top: 2rem;
	border-radius: 20px;
	border: 0;
	box-shadow: 0 5px 30px 0 rgb(128, 200, 0, 0.2);
	animation: fadeIn 1s ease both;
	&::backdrop {
		animation: fadeIn 1s ease both;
		background: hsl(215, 32%, 27%, 0.5);
		z-index: 2;
		backdrop-filter: blur(20px);
	}
	.x {
		filter: grayscale(1);
		border: none;
		background: none;
		position: absolute;
		top: 15px;
		right: 10px;
		transition: ease filter, transform 0.3s;
		cursor: pointer;
		transform-origin: center;
		&:hover {
			filter: grayscale(0);
			transform: scale(1.1);
		}
	}
}

/*General Styles*/
button.pm {
	display: inline-block;
	font-size: 0.8rem;
	color: #fff !important;
	background: rgb(var(--vs-primary) / 100%);
	padding: 13px 25px;
	border-radius: 17px;
	transition: background-color 0.1s ease;
	box-sizing: border-box;
	transition: all 0.25s ease;
	border: 0;
	cursor: pointer;
	box-shadow: 0 10px 20px -10px rgb(var(--vs-primary) / 50%);
	&:hover {
		box-shadow: 0 20px 20px -10px rgb(var(--vs-primary) / 50%);
		transform: translateY(-5px);
	}
}

@keyframes fadeIn {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}

</style>
