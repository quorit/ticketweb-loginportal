<template>
  <v-app>
    <v-app-bar
      app
      :color = "banner_color"
      dark
    >
      <!-- <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer> -->
      <span class="mr-2">
            OUR/UAR Service Ticket Request Forms {{ mode_text }}
      </span>
      <v-spacer/>
      <v-btn v-if="$route.name != 'login' && $route.name != 'error_page'"
                  class="ma-2"
                  @click ="logout()">
                  LOGOUT
               </v-btn>
    </v-app-bar>

    <v-main> 
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

import {delete_session} from './js_extra/network.js';


export default {
  name: 'App',


  data: () =>  
  {
    var banner_color;
    var mode_text;
    mode_text = process.env.VUE_APP_MODE_TEXT;
    banner_color = process.env.VUE_APP_MODE_BANNER_COLOR;

    return {
      banner_color: banner_color,
      mode_text: mode_text
      //
    };
  },
  methods: {
    logout: async function(){
      try {
         await delete_session();      
      } catch (e) {
          this.$router.push( {                    
                    name: "error_page",
                    params: this.$router.get_error_params(e)
                });
          return;
      }
      this.$router.go() //reloads page which should cause cause a re-route to the login page because the session cookie go mauled
    }

  }
};
</script>
