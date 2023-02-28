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
            Student Information Systems Login Portal {{ mode_text }}
      </span>
      <v-spacer/>
    </v-app-bar>

    <v-main> 
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>



const config_data = JSON.parse(process.env.VUE_APP_CONFIG_DATA);

export default {
  name: 'App',


  data: () =>  
  {
    var banner_color;
    var mode_text;
    mode_text = config_data.banner.mode_text;
    banner_color = config_data.banner.color;
    
    return {
      banner_color: banner_color,
      mode_text: mode_text
      //
    };
  },
  methods: {


  },
  mounted: async function(){
  }
};
</script>
