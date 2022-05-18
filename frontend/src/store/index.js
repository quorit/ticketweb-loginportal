import Vue from 'vue'
import Vuex from 'vuex'
import { fetch_init_data, get_user_data } from '../js_extra/network.js'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    init_data: null,    //this will be an object after beeing loaded
    user_data: null
  },
  mutations: {
    set_init_data(state,init_data){
      state.init_data = init_data;
    },
    set_user_data(state,user_data){
      state.user_data = user_data;
    }
  },
  actions: {
    set_init_data(context){

      return fetch_init_data().then(
        init_data => new Promise((resolve) => {
          context.commit('set_init_data',init_data);
          resolve(true);
        })
      );
    },
    set_user_data(context,app_token){
      console.log(app_token);
      return get_user_data(app_token).then(
        response_json => new Promise ((resolve) => {
          context.commit('set_user_data',response_json);
          resolve(true);
        })
      );
    }

  },
  modules: {
  }
})
