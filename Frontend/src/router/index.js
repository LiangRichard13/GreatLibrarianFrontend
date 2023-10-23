import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component:()=>import('../views/Home')
  },
  {
    path: '/usr',
    name: 'Login',
    component:()=>import('../views/Login')
  },
  {
    path: '/register',
    name: 'Register',
    component:()=>import('../views/Register')
  },
  {
    path: '/debug',
    name: 'Debug',
    component:()=>console.log("Hi")
  },
  {
    path:  '/apps/hadoken',
    component: {render: (e) => e("router-view") },
    children: [
      {
        path: 'index',
        component: ()=>import('../apps/hadoken/views/Index')
      },
      {
        path: 'cart',
        component: ()=>import('../apps/hadoken/views/Cart')
      }
        ]
  }

]

const router = new VueRouter({
  scrollBehavior(to, from, savedPosition){ 
    if (savedPosition) { 
      return savedPosition
    }else{
      return {x:0, y:0}
    }
  },
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
