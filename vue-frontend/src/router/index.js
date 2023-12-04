import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/home', // 将根路由重定向到/login
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/UserLogin.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/UserRegister.vue')
    },
    // {
    //   path: '/setting',
    //   name: 'Setting',
    //   component:()=>import('../views/UserSetting.vue')
    // },
    // {
    //   path: '/debug',
    //   name: 'Debug',
    //   component:()=>console.log("Hi")
    // },
    // {
    //   path:  '/apps/hadoken',
    //   component: {render: (e) => e("router-view") },
    //   children: [
    //     {
    //       path: 'index',
    //       component: ()=>import('../apps/hadoken/views/Index')
    //     },
    //     {
    //       path: 'cart',
    //       component: ()=>import('../apps/hadoken/views/Cart')
    //     }
    //       ]
    // }

//导航栏组件复用
    {
        path: '',
        component: () => import("@/components/NavigationTop.vue"),
        children: [
            {
                path: '/home',
                component: () => import("@/views/UserHome.vue")
            },
            {
                path: '/setting',
                component: () => import("@/views/UserSetting.vue")
            },
            {
                path: '/configureNavigation',
                component: () => import("../components/ConfigureNavigation.vue"),
                children: [
                    {
                        path: '/keyConfig',
                        component: () => import("@/views/ApiKeyConfig.vue")
                    },
                     {
                        path: '/dataSetConfig',
                        component: () => import("@/views/DadaSetConfig.vue")
                    }
                ]
            },
        ]
    }
]

const router = new VueRouter({
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return {x: 0, y: 0}
        }
    },
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
