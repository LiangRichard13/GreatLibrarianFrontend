import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI);

new Vue({
    router,
    render: h => h(App)
}).$mount('#app');

//解决error：ResizeObserver loop completed with undelivered notifications
// const debounce = (fn, delay) => {
//   let timer
//    return (...args) => {
//      if (timer) {
//        clearTimeout(timer)
//      }
//      timer = setTimeout(() => {
//        fn(...args)
//      }, delay)
//    }
// }
  
// const _ResizeObserver = window.ResizeObserver;
// window.ResizeObserver = class ResizeObserver extends _ResizeObserver{
//    constructor(callback) {
//      callback = debounce(callback, 200);
//      super(callback);
//    }
// }

// 在 main.js
// Vue.prototype.$navigating = false;
