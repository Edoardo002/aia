<script setup>
import { RouterLink } from 'vue-router'
import MaterialButton from "@/components/MaterialButton.vue";
import { start } from "@/assets/js/foundamentals.js";
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark navbar-absolute bg-transparent shadow-none" >
      <div class="container">
        <a class="navbar-brand text-white" href="javascript:;">AI project</a>
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbar-header-2"
          aria-controls="navbar-header-2"
          aria-expanded="false"
          aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbar-header-2">
          <ul class="navbar-nav mx-auto">
            <li class="nav-item"><RouterLink class="nav-link text-white" to="/"> Home </RouterLink></li>
            <li class="nav-item">
              <RouterLink class="nav-link text-white" to="/about">About Us</RouterLink></li>
          </ul>
          <ul class="nav navbar-nav">
            <li class="nav-item">
              <a
                class="nav-link text-white"
                href="https://twitter.com/CreativeTim">
                <i class="fab fa-twitter"></i>
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link text-white mx-2"
                href="https://www.facebook.com/CreativeTim">
                <i class="fab fa-facebook"></i>
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link text-white"
                href="https://www.instagram.com/CreativeTimOfficial">
                <i class="fab fa-instagram"></i>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="page-header min-vh-100 bg">
      <span class="mask bg-gradient-dark opacity-5"></span>
      <div class="container">
        <div class="row">
          <div class="col-lg-6 col-md-7 d-flex justify-content-center flex-column">
            <h1 class="text-white mb-4">Enhance LLMs with your own Data</h1>
            <p class="text-white opacity-8 lead pe-5 me-5">
              Query and manage your context-aware chatbots using custom data to perform Retrieval Augmented Generation on the best LLMs available. 
            </p>
            <div class="buttons">
              <MaterialButton color="white" class="mt-4" @click="start()"
                >Get Started</MaterialButton>
              <MaterialButton color="none" class="text-white shadow-none mt-4"
                >Read more</MaterialButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style>
.bg {
  background-image: url(../assets/img/land.png);
}
</style>