<script setup>

import '@/assets/style/styles.scss';
import { slideToggle, slideUp, slideDown } from '@/assets/js/libs/slide';
import { ANIMATION_DURATION } from '@/assets/js/libs/constants';
import Poppers from '@/assets/js/libs/poppers';
import { onMounted } from 'vue';

const PoppersInstance = new Poppers();
/**
 * wait for the current animation to finish and update poppers position
 */
const updatePoppersTimeout = () => {
  setTimeout(() => {
    PoppersInstance.updatePoppers();
  }, ANIMATION_DURATION);
};

const fsmb = document.querySelectorAll(
  '.menu > ul > .menu-item.sub-menu > a'
);

const ismb = document.querySelectorAll(
  '.menu > ul > .menu-item.sub-menu .menu-item.sub-menu > a'
);

/**
 * sidebar collapse handler
 */
function sidebarColl() {
  document.getElementById('sidebar').classList.toggle('collapsed');
  PoppersInstance.closePoppers();
  if (document.getElementById('sidebar').classList.contains('collapsed'))
    fsmb.forEach((element) => {
      element.parentElement.classList.remove('open');
    });

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
              <div>P</div>
              <h5>Pro Sidebar</h5>
            </div>
          </div>
          <div class="sidebar-content">
            <nav class="menu open-current-submenu">
              <ul>
                <li class="menu-header"><span> GENERAL </span></li>
                <li class="menu-item sub-menu">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-vip-diamond-fill"></i>
                    </span>
                    <span class="menu-title">Components</span>
                    <span class="menu-suffix">
                      <span class="badge primary">Hot</span>
                    </span>
                  </a>
                  <div class="sub-menu-list">
                    <ul>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Grid</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Layout</span>
                        </a>
                      </li>
                      <li class="menu-item sub-menu">
                        <a href="#">
                          <span class="menu-title">Forms</span>
                        </a>
                        <div class="sub-menu-list">
                          <ul>
                            <li class="menu-item">
                              <a href="#">
                                <span class="menu-title">Input</span>
                              </a>
                            </li>
                            <li class="menu-item">
                              <a href="#">
                                <span class="menu-title">Select</span>
                              </a>
                            </li>
                            <li class="menu-item sub-menu">
                              <a href="#">
                                <span class="menu-title">More</span>
                              </a>
                              <div class="sub-menu-list">
                                <ul>
                                  <li class="menu-item">
                                    <a href="#">
                                      <span class="menu-title">CheckBox</span>
                                    </a>
                                  </li>
                                  <li class="menu-item">
                                    <a href="#">
                                      <span class="menu-title">Radio</span>
                                    </a>
                                  </li>
                                  <li class="menu-item sub-menu">
                                    <a href="#">
                                      <span class="menu-title">Want more ?</span>
                                      <span class="menu-suffix">&#x1F914;</span>
                                    </a>
                                    <div class="sub-menu-list">
                                      <ul>
                                        <li class="menu-item">
                                          <a href="#">
                                            <span class="menu-prefix">&#127881;</span>
                                            <span class="menu-title">You made it </span>
                                          </a>
                                        </li>
                                      </ul>
                                    </div>
                                  </li>
                                </ul>
                              </div>
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
                    <span class="menu-title">Charts</span>
                  </a>
                  <div class="sub-menu-list">
                    <ul>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Pie chart</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Line chart</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Bar chart</span>
                        </a>
                      </li>
                    </ul>
                  </div>
                </li>
                <li class="menu-item sub-menu">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-shopping-cart-fill"></i>
                    </span>
                    <span class="menu-title">E-commerce</span>
                  </a>
                  <div class="sub-menu-list">
                    <ul>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Products</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Orders</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">credit card</span>
                        </a>
                      </li>
                    </ul>
                  </div>
                </li>
                <li class="menu-item sub-menu">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-global-fill"></i>
                    </span>
                    <span class="menu-title">Maps</span>
                  </a>
                  <div class="sub-menu-list">
                    <ul>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Google maps</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Open street map</span>
                        </a>
                      </li>
                    </ul>
                  </div>
                </li>
                <li class="menu-item sub-menu">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-ink-bottle-fill"></i>
                    </span>
                    <span class="menu-title">Theme</span>
                  </a>
                  <div class="sub-menu-list">
                    <ul>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Dark</span>
                        </a>
                      </li>
                      <li class="menu-item">
                        <a href="#">
                          <span class="menu-title">Light</span>
                        </a>
                      </li>
                    </ul>
                  </div>
                </li>
                <li class="menu-header" style="padding-top: 20px"><span> EXTRA </span></li>
                <li class="menu-item">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-book-2-fill"></i>
                    </span>
                    <span class="menu-title">Documentation</span>
                    <span class="menu-suffix">
                      <span class="badge secondary">Beta</span>
                    </span>
                  </a>
                </li>
                <li class="menu-item">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-calendar-fill"></i>
                    </span>
                    <span class="menu-title">Calendar</span>
                  </a>
                </li>
                <li class="menu-item">
                  <a href="#">
                    <span class="menu-icon">
                      <i class="ri-service-fill"></i>
                    </span>
                    <span class="menu-title">Examples</span>
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
            <h1 style="margin-bottom: 0">Pro Sidebar</h1>
            <span style="display: inline-block; margin-bottom: 10px">
              Responsive layout with advanced sidebar menu built with SCSS and vanilla Javascript
            </span>
          </div>
          <div>
            <h2>Features</h2>
          </div>
        </main>
        <div class="overlay"></div>
      </div>
    </div>

</template>../assets/libs/slide../assets/libs/constants../assets/libs/poppers