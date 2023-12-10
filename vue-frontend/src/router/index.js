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
                component: () => import("@/views/me/UserSetting.vue")
            },
            {
                path: '/userFriendsList',
                component: () => import("@/views/me/UserFriendsList.vue")
            },
            {
                path: '/experimentList/:id/:name',
                component: () => import("@/views/Experiment/ExperimentList.vue")
            },
            {
                path: '/configureNavigation',
                component: () => import("../components/ConfigureNavigation.vue"),
                children: [
                    {
                        path: '/keyConfig',
                        component: () => import("@/views/Config/ApiKeyConfig.vue")
                    },
                    {
                        path: '/dataSetConfig',
                        component: () => import("@/views/Config/DadaSetConfig.vue")
                    }
                ]
            },
            {
                path: '/collaborateNavigation',
                component: () => import("../components/CollaborateNavigation.vue"),
                children: [
                    {
                        path: '/myCollaborate',
                        component: () => import("@/views/Collaborate/MyCollaborate.vue")
                    },
                    {
                        path: '/userList',
                        component: () => import("@/views/Collaborate/UserList.vue")
                    }
                ]
            },
            {
                path: '/projectNavigation',
                component: () => import("../components/ProjectNavigation.vue"),
                children: [
                    {
                        path: '/addProject',
                        component: () => import("@/views/Project/AddProject.vue")
                    },
                    {
                        path: '/projectsList',
                        component: () => import("@/views/Project/ProjectsList.vue")
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
            return { x: 0, y: 0 }
        }
    },
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
