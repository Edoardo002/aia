k<script setup>
import MaterialInput from "@/components/MaterialInput.vue";
import MaterialSwitch from "@/components/MaterialSwitch.vue";
import MaterialButton from "@/components/MaterialButton.vue";
import { dashboard, sign, eLoginSubmit } from '@/assets/js/foundamentals';
import { signOut } from '@/assets/js/Gauth';
import * as mAuth from '@/assets/js/Mauth';
import { onMounted } from "vue";

window.handleCredentialResponse = (response) => {
    const responsePayload = parseJwt(response.credential);
    console.log("ID: " + responsePayload.sub);
    console.log('Full Name: ' + responsePayload.name);
    console.log('Given Name: ' + responsePayload.given_name);
    console.log('Family Name: ' + responsePayload.family_name);
    console.log("Image URL: " + responsePayload.picture);
    console.log("Email: " + responsePayload.email);

    eLoginSubmit(responsePayload.given_name, responsePayload.family_name, responsePayload.email);
}

function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

async function loginSubmit() {
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;
  if (email==null || password==null) {
    alert('Field email or password cannot be empty');
    return;
  }
  const response = await fetch('http://127.0.0.1:8000/chatbot/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email:email, password:password })
  });
  if (response.ok) {
    const data = await response.json();
    const now = new Date()
    const token = {
        value: data.token,
        expiry: now.getTime() + 3600*1000*4,
    }
    localStorage.setItem('token', JSON.stringify(token));
    dashboard(data.user);
  } else {
    const error = await response.json();
    console.error(error);
    alert('Invalid e-mail or password');
  }
}

onMounted(() => {
  let gClientScript = document.createElement('script');
  gClientScript.setAttribute('src', "https://accounts.google.com/gsi/client");
  document.head.appendChild(gClientScript);
})

</script>
<template>
    <div
      class="page-header align-items-start min-vh-100 back">
      <span class="mask bg-dark opacity-6"></span>
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
                      color="dark" @click="loginSubmit"
                      fullWidth
                      >Log in</MaterialButton
                    >
                  </div>
                  <p class="mt-4 text-sm text-center">
                    Don't have an account?
                    <a
                      class="text-dark text-gradient font-weight-bold"
                      @click="sign"
                      >Sign up</a
                    >
                  </p>
                </div>
                <div id="g_id_onload"
                  data-client_id="616333172733-j0pkj677420lqm9dvljud9d8n2tsok2f.apps.googleusercontent.com"
                  data-context="signin"
                  data-ux_mode="popup"
                  data-callback="handleCredentialResponse"
                  data-auto_select="false">
                </div>

                <div class="g_id_signin"
                  data-type="standard"
                  data-shape="pill"
                  data-theme="filled_black"
                  data-text="signin_with"
                  data-size="large"
                  data-logo_alignment="left">
                </div>
                <div class="text-center">
                    <MaterialButton
                      class="my-4 mb-2"
                      color="info" @click="mAuth.signIn"
                      fullWidth
                      >Accedi con Microsoft</MaterialButton
                    >
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
.back {
  background-image: url(../assets/img/black.jpg);
}
.defcolor {
  background-color:rgb(128, 200, 0);
}
</style>