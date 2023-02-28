import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginForm from '../views/Login.vue'

Vue.use(VueRouter)



const routes = [
    {
        path: '/:app_key?',
        component: LoginForm,
        name: "login"
    },

];



function scrollBehavior (to, from, savedPosition){
    if (savedPosition){
        return savedPosition;
    }else{
        return {x:0, y:0};
    }
}

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior
});




export default router
