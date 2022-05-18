import Vue from 'vue'
import VueRouter from 'vue-router'
import TicketInfo from '../views/TicketInfo.vue'
import ReportingForm from '../views/Reporting.vue'
import RptSupport from '../views/RptSupport.vue'
import ErrorPage from '../views/ErrorPage.vue'
import LoginForm from '../views/Login.vue'
import store from '../store'
import {SessionAuthenticationError, get_app_token, HTTPResponseError} from '../js_extra/network.js'
import {WebProjectError} from '../js_extra/web_project_error.js'


Vue.use(VueRouter)


//function sessionCookieExists() {
//    var cookieArr = document.cookie.split(";");
//    var cookieName;
//    var cookiePair;
//    console.log(document.cookie);
//    console.log(cookieArr);
//    for(var i = 0; i < cookieArr.length; i++) {
//        cookiePair = cookieArr[i].split("=");
//        cookieName = cookiePair[0].trim();
//        if (cookieName == "reporting"){
//            return true;
//        }
//    }
//    return false;
// }






const routes = [
	{
        path: '/ticket_info/:id',
        component: TicketInfo,
        name: 'ticket_info',
        props: (route) => { 
            return {
                id: route.params.id
            }; 
        }    
	},
    {
        path: '/forms/:type(admissions|student)',
        component: ReportingForm,
        name: "reporting_request_forms"
    },
    {
        path: '/login/:type(admissions|student|rptsupport)',
        component: LoginForm,
        name: "login"
    },
    {
        path: '/forms/:type(rptsupport)',
        component: RptSupport,
        name: "reporting_support_form"
    },
    {
        path: '/error/:error_type/:status_code?',
        component: ErrorPage,
        name: 'error_page',
        // eslint-disable-next-line no-unused-vars
        props: true
    }

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



function get_error_params(e){
    var return_val={};
    if (e instanceof WebProjectError){
        return_val.error_type = e.name;
        if (e instanceof HTTPResponseError){
            return_val.status_code=e.status_code.toString();
        }
    }else{
        return_val.error_type = "Uncategorized";
    }
    return return_val;
}


router.get_error_params=get_error_params;

router.beforeEach(async (to,from,next) => {
    function next_login(){
        //here 'to' is assumed to be either reporting_support_form or
        //reporting_request forms
        var type;
        if (to.name == 'reporting_support_form'){
            type = 'rptsupport';
        }else{
            type = to.params.type
        }
        next({
            name: "login",
            params: {
                type: type
            }
        });
    }

    


    if((to.name == 'reporting_request_forms' || to.name == 'reporting_support_form')){
        if(!store.state.init_data){
            var x;
            try { 
                x=await store.dispatch('set_init_data');
                console.log(x);
            } catch(e) {
                next({
                    name: "error_page",
                    params: get_error_params(e)
                });
                return;            
            }
        }
      

        var app_token;
        try{
            app_token = await get_app_token();

        } catch (e) {
            if (e instanceof SessionAuthenticationError){
                //this should cover...missing session cookie, expired session
                //anyhitng that would result in an "401 Unauthorized". Don't forget that
                //the language of 'Unauthorized' in HTTP codes is wrong
                //and really refers to authentication problems.
                next_login();
                return;
            }else{

                const error_params=get_error_params(e);

                next( {                    
                    name: "error_page",
                    params: error_params
                });
                return;
            }

        }
        if (!store.state.user_data){
            try{
                await store.dispatch('set_user_data',app_token);
            } catch (e) {
                //note that a 401 here does not mean we go to the login page.
                //since we are using a jwt token that we just got and it should work.
                next( {                    
                    name: "error_page",
                    params: get_error_params(e)
                });
                return;
            }
        }
    }
    next();
 });


export default router
