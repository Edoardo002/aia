<script setup>

import '@/assets/style/styles.scss';
import '@/assets/css/base.css'
import { slideToggle, slideUp, slideDown } from '@/assets/js/libs/slide';
import { ANIMATION_DURATION } from '@/assets/js/libs/constants';
import Poppers from '@/assets/js/libs/poppers';
import { onMounted } from 'vue';
import { start, checkAuth} from '@/assets/js/foundamentals';
import { useRoute } from 'vue-router';
import CardElement from '@/components/CardElement.vue'

const route = useRoute();
const user_id = route.params.id;

if (checkAuth(user_id)) {}
else start();

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
                        <a href="#">
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
                              <a href="#">
                                <span class="menu-title">RAGGed</span>
                              </a>
                            </li>
                            <li class="menu-item">
                              <a href="#">
                                <span class="menu-title">Base Models</span>
                              </a>
                            </li>
                            <li class="menu-item sub-menu">
                              <a href="#">
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
                        <a href="#">
                          <span class="menu-title">Utilization</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a href="#">
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
                        <a href="#">
                          <span class="menu-title">Profile</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Payment method</span>
                        </a>
                      </li>
                    </ul>
                  </div>
                </li>
                <li class="menu-item">
                  <a href="#">
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
            <h1 style="margin-bottom: 0">Models</h1>
            <span style="display: inline-block; margin-bottom: 10px">
              Here your context-aware models. If you have not created one yet, start the process by clicking on Create
            </span>

            <CardElement></CardElement>

          </div>
        </main>
        <div class="overlay"></div>
      </div>
    </div>

</template>