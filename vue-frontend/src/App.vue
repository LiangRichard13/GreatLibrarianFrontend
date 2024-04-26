<template>
    <router-view/>
</template>

<script>
export default {
  provide() {
    return {
      isUpdate:false
    }
  }
}
//解决error：ResizeObserver loop completed with undelivered notifications
const debounce = (fn, delay) => {
    let timer
     return (...args) => {
       if (timer) {
         clearTimeout(timer)
       }
       timer = setTimeout(() => {
         fn(...args)
       }, delay)
     }
  }
    
  const _ResizeObserver = window.ResizeObserver;
  window.ResizeObserver = class ResizeObserver extends _ResizeObserver{
     constructor(callback) {
       callback = debounce(callback, 200);
       super(callback);
     }
  }
</script>

<style>
    body {
        background: white;
        width: 100%;
        min-width: 1500px;
        height: 100%;
        margin: 0;
    }

    a{
        text-decoration: none;
    }
</style>
