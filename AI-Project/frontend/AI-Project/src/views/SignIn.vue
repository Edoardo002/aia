<script setup>
import MaterialInput from "@/components/MaterialInput.vue";
import MaterialSwitch from "@/components/MaterialSwitch.vue";
import MaterialButton from "@/components/MaterialButton.vue";
import { dashboard } from '@/assets/js/foundamentals'

async function loginSubmit() {
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;
  const response = await fetch('http://127.0.0.1:8000/chatbot/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email:email, password:password })
  });
  if (response.ok) {
    const data = await response.json();
    console.log(data);
    dashboard(data);
  } else {
    const error = await response.json();
    console.error(error);
    alert('Invalid e-mail or password');
  }
}
</script>
<template>
    <div
      class="page-header align-items-start min-vh-100 bg">
      <span class="mask bg-gradient-dark opacity-6"></span>
      <div class="container my-auto">
        <div class="row">
          <div class="col-lg-4 col-md-8 col-12 mx-auto">
            <div class="card z-index-0 fadeIn3 fadeInBottom">
              <div
                class="card-header p-0 position-relative mt-n4 mx-3 z-index-2"
              >
                <div
                  class="defcolor shadow-success border-radius-lg py-3 pe-1"
                >
                  <h4
                    class="text-white font-weight-bolder text-center mt-2 mb-0"
                  >
                    Log in
                  </h4>
                  <div class="row mt-3">
                    <div class="col-2 text-center ms-auto">
                      <a class="btn btn-link px-3" href="javascript:;">
                        <i class="fa fa-facebook text-white text-lg"></i>
                      </a>
                    </div>
                    <div class="col-2 text-center px-1">
                      <a class="btn btn-link px-3" href="javascript:;">
                        <i class="fa fa-github text-white text-lg"></i>
                      </a>
                    </div>
                    <div class="col-2 text-center me-auto">
                      <a class="btn btn-link px-3" href="javascript:;">
                        <i class="fa fa-google text-white text-lg"></i>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card-body">
                <div role="form" class="text-start">
                  <MaterialInput
                    id="email"
                    class="input-group-outline my-3"
                    placeholder="email"
                    type="email"
                  />
                  <MaterialInput
                    id="password"
                    class="input-group-outline mb-3"
                    placeholder="password"
                    type="password"
                  />
                  <MaterialSwitch
                    class="d-flex align-items-center mb-3"
                    id="rememberMe"
                    labelClass="mb-0 ms-3"
                    checked
                    >Remember me</MaterialSwitch
                  >

                  <div class="text-center">
                    <MaterialButton
                      class="my-4 mb-2"
                      color="defcolor" @click="loginSubmit"
                      fullWidth
                      >Log in</MaterialButton
                    >
                  </div>
                  <p class="mt-4 text-sm text-center">
                    Don't have an account?
                    <a
                      href="/signup"
                      class="text-dark text-gradient font-weight-bold"
                      >Sign up</a
                    >
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <footer class="footer position-absolute bottom-2 py-2 w-100">
      </footer>
    </div>
</template>

<style>
.bg {
  background-image: url(../assets/img/black.jpg);
}
.defcolor {
  background-color:rgb(128, 200, 0);
}
</style>