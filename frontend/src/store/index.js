import Vue from 'vue'
import Vuex from 'vuex'

const rt_network = require("rt_network");

Vue.use(Vuex)

const config_data = JSON.parse(process.env.VUE_APP_CONFIG_DATA);
const shared_data_path = config_data.vue_app_path_roots.shared_data;

const app_server_path = config_data.vue_app_path_roots.app_server;

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

      return rt_network.fetch_init_data(shared_data_path).then(
        init_data => new Promise((resolve) => {
          context.commit('set_init_data',init_data);
          resolve(true);
        })
      );
    },
    set_user_data(context,app_token){
      return rt_network.get_user_data(app_token,app_server_path).then(
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