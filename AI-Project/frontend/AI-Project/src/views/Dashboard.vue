<script setup>

import '@/assets/style/styles.scss';
import '@/assets/css/base.css';
import '@/assets/css/chat.css';
import '@/assets/css/pricing.css';
import * as Logic from '@/assets/js/triggerLogic';
import { slideToggle, slideUp, slideDown } from '@/assets/js/libs/slide';
import { ANIMATION_DURATION } from '@/assets/js/libs/constants';
import Poppers from '@/assets/js/libs/poppers';
import { onMounted, ref } from 'vue';
import { start, checkAuth, getId} from '@/assets/js/foundamentals';
import { useRoute } from 'vue-router';
import ModelCardElement from '@/components/ModelCardElement.vue'
import ContextCardElement from '@/components/ContextCardElement.vue'
import MaterialButton from "@/components/MaterialButton.vue";
import MaterialInput from '@/components/MaterialInput.vue';
import Modal from '@/components/Modal.vue'

const route = useRoute();
const user_sqid = route.params.id;
const user_id = getId(user_sqid);
const contexts_array = ref([]);
const models_array = ref([]);

const chat_messages = ref([]);

checkAuth(user_id).then((auth) => {
  if (!auth) start();
});

const PoppersInstance = new Poppers();
/**
 * wait for the current animation to finish and update poppers position
 */
const updatePoppersTimeout = () => {
  setTimeout(() => {
    PoppersInstance.updatePoppers();
  }, ANIMATION_DURATION);
};

/**
 * sidebar collapse handler
 */
function sidebarColl() {
  document.getElementById('sidebar').classList.toggle('collapsed');
  PoppersInstance.closePoppers();
  if (document.getElementById('sidebar').classList.contains('collapsed')) {
    document.querySelectorAll(
      '.menu > ul > .menu-item.sub-menu > a'
    ).forEach((element) => {
      element.parentElement.classList.remove('open');
    });
    document.querySelectorAll('.menu-item').forEach((el) => {
      el.childNodes.forEach((child) =>{
        child.lastElementChild.style.display = 'none';
      })
    });
  }
  else {
    document.querySelectorAll('.menu-item').forEach((el) => {
      el.childNodes.forEach((child) =>{
        child.lastElementChild.style.display = 'block';
      })
    });
  }
  updatePoppersTimeout();
};

/**
 * sidebar toggle handler (on break point )
 */
function sidebarHandler() {
  document.getElementById('sidebar').classList.toggle('toggled');
  
  updatePoppersTimeout();
};

/**
 * toggle sidebar on overlay click
 */
function overlay() {
  document.getElementById('sidebar').classList.toggle('toggled');
};

onMounted(() => {

  const fsmb = document.querySelectorAll(
  '.menu > ul > .menu-item.sub-menu > a'
);

  const ismb = document.querySelectorAll(
  '.menu > ul > .menu-item.sub-menu .menu-item.sub-menu > a'
);

  const defaultOpenMenus = document.querySelectorAll('.menu-item.sub-menu.open');
  
  defaultOpenMenus.forEach((element) => {
  element.lastElementChild.style.display = 'block';
});
/**
 * handle top level submenu click
 */
fsmb.forEach((element) => {
  element.addEventListener('click', () => {
    if (document.getElementById('sidebar').classList.contains('collapsed'))
      PoppersInstance.togglePopper(element.nextElementSibling);
    else {
      /**
       * if menu has "open-current-only" class then only one submenu opens at a time
       */
      const parentMenu = element.closest('.menu.open-current-submenu');
      if (parentMenu)
        parentMenu
          .querySelectorAll(':scope > ul > .menu-item.sub-menu > a')
          .forEach(
            (el) =>
              window.getComputedStyle(el.nextElementSibling).display !==
                'none' && slideUp(el.nextElementSibling)
          );
      slideToggle(element.nextElementSibling);
    }
  });
});

/**
 * handle inner submenu click
 */
ismb.forEach((element) => {
  element.addEventListener('click', () => {
    slideToggle(element.nextElementSibling);
  });
});

})

Logic.getContexts(user_id).then((data) => {
  contexts_array.value = data;
});

Logic.getModels(user_id).then((data) => {
  var res = data.substring(2, data.length-2);
  let array = res.split(': ');
  var temp = []; var i = 0;
  array.forEach((item) => {
    if (!i%2==0) temp.push(array[i].split('.')[0].substring(1));
    i++;
  });
  models_array.value = temp; // temp
});

const showRAGged = ref(true);
const showContext = ref(false);
const showBase = ref(false);
const showCreateNew = ref(false);
const showUtilization = ref(false);
const showBills = ref(false);
const showProfile= ref(false);
const showPaymentMethod = ref(false);
const showPlan = ref(false);

const chat = ref(false);
const chat_model = ref();

const urlNotUploaded = ref(true);
const filesNotUploaded = ref(true);

function clear(){
  showRAGged.value = false;
  showContext.value = false;
  showBase.value = false;
  showCreateNew.value = false;
  showUtilization.value= false;
  showBills.value = false;
  showProfile.value = false;
  showPaymentMethod.value = false;
  showPlan.value = false;
}

function changeFrame(frame) {
  clear();
  if (frame==0) showContext.value=true;
  else if (frame==1) showRAGged.value=true;
  else if (frame==2) showBase.value=true;
  else if (frame==3) showCreateNew.value=true;
  else if (frame==4) showUtilization.value=true;
  else if (frame==5) showBills.value=true;
  else if (frame==6) showProfile.value=true;
  else if (frame==7) showPaymentMethod.value=true;
  else showPlan.value=true;
}

function onFileUpload() {
  filesNotUploaded.value=false;
}

function onUrlUpload() {
  urlNotUploaded.value=false;
}

function startRagUI(model) {
  clear();
  chat.value = true;
  chat_model.value = model;
}

</script>
<template>

    <div class="layout has-sidebar fixed-sidebar fixed-header">
      <aside id="sidebar" class="sidebar break-point-lg has-bg-image">
        <a id="btn-collapse" class="sidebar-collapser" @click="sidebarColl"><i class="ri-arrow-left-s-line"></i></a>
        <div class="image-wrapper">
          <img src="../assets/img/black.jpg" alt="sidebar background" />
        </div>
        <div class="sidebar-layout">
          <div class="sidebar-header">
            <div class="pro-sidebar-logo">
              <div>C</div>
              <h5>CogiTCH</h5>
            </div>
          </div>
          <div class="sidebar-content">
            <nav class="menu open-current-submenu">
              <ul>
                <li class="menu-header"><span> GENERAL </span></li>
                <li class="menu-item sub-menu">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-codepen-fill"></i>
                    </span>
                    <span class="menu-title">My Bots</span>
                    <span class="menu-suffix">
                      <span class="badge primary">New</span>
                    </span>
                  </a>
                  <div class="sub-menu-list">
                    <ul>
                      <li class="menu-item">
                        <a @click="changeFrame(0)" href="#">
                          <span class="menu-title">Contexts</span>
                        </a>
                      </li>
                      <li class="menu-item sub-menu">
                        <a href="#">
                          <span class="menu-title">Models</span>
                        </a>
                        <div class="sub-menu-list">
                          <ul>
                            <li class="menu-item">
                              <a @click="changeFrame(1)" href="#">
                                <span class="menu-title">RAGged</span>
                              </a>
                            </li>
                            <li class="menu-item">
                              <a @click="changeFrame(2)" href="#">
                                <span class="menu-title">Base Models</span>
                              </a>
                            </li>
                            <li class="menu-item">
                              <a @click="changeFrame(3)" href="#">
                                <span class="menu-title">Create new</span>
                              </a>
                            </li>
                          </ul>
                        </div>
                      </li>
                    </ul>
                  </div>
                </li>
                <li class="menu-item sub-menu">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-bar-chart-2-fill"></i>
                    </span>
                    <span class="menu-title">Stats</span>
                  </a>
                  <div class="sub-menu-list">
                    <ul>
                      <li class="menu-item">
                        <a @click="changeFrame(4)" href="#">
                          <span class="menu-title">Utilization</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a @click="changeFrame(5)" href="#">
                          <span class="menu-title">Bills</span>
                        </a>
                      </li>
                    </ul>
                  </div>
                </li>
                <li class="menu-item sub-menu">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-calendar-fill"></i>
                    </span>
                    <span class="menu-title">Settings</span>
                  </a>
                  <div class="sub-menu-list">
                    <ul>
                      <li class="menu-item">
                        <a @click="changeFrame(6)" href="#">
                          <span class="menu-title">Profile</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a @click="changeFrame(7)" href="#">
                          <span class="menu-title">Payment method</span>
                        </a>
                      </li>
                    </ul>
                  </div>
                </li>
                <li class="menu-item">
                  <a @click="changeFrame(8)" href="#">
                    <span class="menu-icon">
                      <i class="ri-vip-diamond-fill"></i>
                    </span>
                    <span class="menu-title">Plan</span>
                  </a>
                </li>
                <li class="menu-header" style="padding-top: 20px"><span> MORE </span></li>
                <li class="menu-item">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-book-2-fill"></i>
                    </span>
                    <span class="menu-title">Examples</span>
                  </a>
                </li>
                <li class="menu-item">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-global-fill"></i>
                    </span>
                    <span class="menu-title">Integrate</span>
                  </a>
                </li>
                <li class="menu-item">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-service-fill"></i>
                    </span>
                    <span class="menu-title">Contact us</span>
                  </a>
                </li>
              </ul>
            </nav>
          </div>
          <div class="sidebar-footer">
          </div>
        </div>
      </aside>
      <div id="overlay" class="overlay" @click="overlay"></div>
      <div class="layout">
        <main class="content">
          <div>
            <a id="btn-toggle" href="#" class="sidebar-toggler break-point-lg" @click="sidebarHandler">
              <i class="ri-menu-line ri-xl"></i>
            </a>

            <Transition mode="out-in">
              
            <div v-if="showRAGged">
            <h1 style="margin-bottom: 0">Models</h1>
            <span style="display: inline-block; margin-bottom: 10px">
              Here your context-aware models. If you have not created one yet, start the process by clicking on Create
            </span>

            <Modal button-message="+ Create">
              <h2>Create a new Model</h2>
	            <p>Choose a large language model to RAG with your context and query</p>
              <h2>Select a context</h2>
              <fieldset>
              <label v-for="item in contexts_array" class="rad-label">
                <input type="radio" class="rad-input" name="context" v-bind:value="item">
                <div class="rad-design"></div>
                <div class="rad-text">{{ item }}</div>
              </label>
              </fieldset>
              <h2 class="mt-2">Select a Model</h2>
              <fieldset>
              <label class="rad-label">
                <input type="radio" class="rad-input" name="model" value="openai">
                <div class="rad-design"></div>
                <div class="rad-text">OpenAI</div>
              </label>
              <label class="rad-label">
                <input type="radio" class="rad-input" name="model" value="cohere">
                <div class="rad-design"></div>
                <div class="rad-text">Cohere</div>
              </label>
              <label class="rad-label">
                <input type="radio" class="rad-input" name="model" value="anthropic">
                <div class="rad-design"></div>
                <div class="rad-text">Anthropic</div>
              </label>
              </fieldset><br>
              <MaterialButton id="rag" color="secondary" @click="Logic.addNewModel(user_id)">Create Rag</MaterialButton>
            </Modal>
            
            <div class="grid-container">
              <div v-for="item in models_array"
                @click="startRagUI(item)" class="grid-item"><ModelCardElement v-bind:model-name="item">{{ item }}</ModelCardElement>
              </div>
            </div>
            </div>
          
            <div v-else-if="showContext">
            <h1 style="margin-bottom: 0">Contexts</h1>
            <span style="display: inline-block; margin-bottom: 10px">
              Here your uploaded Contexts. If you have not created one yet, start the process by clicking on Add
            </span>

            <Modal button-message="+ Add">
              <h2>Upload your context</h2>
	            <p>Here you can store your documents by selecting files from your device or linking a Sharepoint repository</p>
              <MaterialInput id="contextURL"
                    class="input-group-outline mb-3"
                    placeholder="Sharepoint URL"
                    type="url" v-on:input="onUrlUpload"> </MaterialInput>
              <MaterialInput id="clientId"
                    class="input-group-outline mb-3"
                    placeholder="client id"> </MaterialInput>
              <MaterialInput id="clientSecret"
                    class="input-group-outline mb-3"
                    placeholder="client secret"> </MaterialInput>
              <MaterialInput id="documentLib"
                    class="input-group-outline mb-3"
                    placeholder="document library id"> </MaterialInput>
              <MaterialInput id="path"
                    class="input-group-outline mb-3"
                    placeholder="folder path"> </MaterialInput>
              <h2 class="mt-2">Select an Embedding</h2>
              <fieldset>
              <label class="rad-label">
                <input type="radio" class="rad-input" name="embed" value="openai">
                <div class="rad-design"></div>
                <div class="rad-text">OpenAI</div>
              </label>
              <label class="rad-label">
                <input type="radio" class="rad-input" name="embed" value="cohere">
                <div class="rad-design"></div>
                <div class="rad-text">Cohere</div>
              </label>
              </fieldset><br>
              <MaterialButton id="sharebtn" color="secondary" :disabled="urlNotUploaded" @click="Logic.addSharepointContext(user_id)"
                >use sharepoint</MaterialButton>
              <input id="userFiles" type="file" accept=".txt, .pdf" v-on:change="onFileUpload" multiple="true">
              <MaterialButton id="uploadbtn" color="secondary" :disabled="filesNotUploaded" @click="Logic.addNewContext(user_id)"
                >upload</MaterialButton>
            </Modal>

            <div class="grid-container">
              <div v-for="item in contexts_array"
              class="grid-item"><ContextCardElement v-bind:context-name="item">{{ item }}</ContextCardElement>
            </div>
            </div>
            </div>


            <div v-else-if="chat">
            <h1 id="chatName" style="margin-bottom: 0"> {{ chat_model }} </h1>
            <span style="display: inline-block; margin-bottom: 10px">
              Ask questions to your RAGged model to unlock all Cogitch power.
            </span>

            <div class="wrapper">
              <ul id="chatList">
                <li>Hi, ask me anything!</li>
              </ul>
            </div>

            <MaterialInput id="queryBot"
                    class="input-group-outline mb-3"
                    placeholder="Write message..."
                    type="text">
            </MaterialInput>
            <MaterialButton @click="Logic.queryBot(user_id)" id="sendbtn" color="secondary">SEND</MaterialButton>
            </div>

            <div v-else-if="showPlan">
              <h1 style="margin-bottom: 0">Plan</h1>
              <span style="display: inline-block;">
                Select your subscription plan to CogiTCH
              </span>

              <div class="grid_price">
                  <div class="card_price">
                      <h2 class="card_price_title">Student</h2>
                      <p class="pricing">20$<span class="small">/per month</span></p>
                      <span class="small">Save 6$</span>
                      <hr>
                      <ul class="features">
                          <li>Personal Account</li>
                          <li>Limited Contexts</li>
                          <li>Limited Queries</li>
                      </ul>
                      <a href="#" class="cta_btn">Buy Now</a>
                  </div>
                  <div class="card_price">
                      <h2 class="card_price_title">Personal</h2>
                      <p class="pricing">60$<span class="small">/per month</span></p>
                      <span class="small">Save 15$</span>
                      <hr>
                      <ul class="features">
                          <li>Personal account</li>
                          <li>Limited Contexts</li>
                          <li>Unlimited Queries</li>
                      </ul>
                       <a href="#" class="cta_btn">Buy Now</a>
                  </div>
                  <div class="card_price">
                      <h2 class="card_price_title">Business</h2>
                      <p class="pricing">100$<span class="small">/per month</span></p>
                      <span class="small">Save 25$</span>
                      <hr>
                      <ul class="features">
                          <li>Organizational Accounts</li>
                          <li>Unlimited Contexts</li>
                          <li>Unlimited Queries</li>
                      </ul>
                       <a href="#" class="cta_btn">Buy Now</a>
                  </div>
              </div>
            </div>

          </Transition>
          
          </div>
        </main>
        <div class="overlay"></div>
      </div>
    </div>

</template>

<style>

.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}

h2 {
	font-weight: 600;
	font-size: 1.5rem;
	padding-bottom: 1rem;
}

p {
	font-size: 1rem;
	line-height: 1.3rem;
	padding: 0.5rem 0;
}

input {
  margin-bottom: 1rem;
  color: #fffff4 !important;
}

input::file-selector-button {
  font-weight: bold;
  font-family: sans-serif;
  text-transform: uppercase;
  color: #ffffff;
  background-color: rgb(128, 200, 0);
  padding-left: 1.4rem;
  padding-right: 1.4rem;
  padding-top: 0.6rem;
  padding-bottom: 0.6rem;
  border: thin solid hsl(215, 32%, 27%, 0.5);
  border-radius: 8px;
  font-size: 0.8rem;
}

</style>