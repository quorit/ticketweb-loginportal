

<template>
   

   <v-container>
      <v-row>
         <v-col cols="12">
        <v-img
          style="margin-left:auto;margin-right:auto;"
          alt="Vuetify Name"
          sclass="shrink mt-1 hidden-sm-and-down"
          contain
          max-width="50%"
          :src="img_url"
          width="50%"
        />

         </v-col>
      </v-row>
      <v-form
         ref="form"
         v-model="form_valid"
         lazy-evaluation
         @submit.prevent="login()"
      >
     <v-row>
         <v-col cols="12">
            <v-text-field
                maxlength="50"
                  v-model="net_id"
                  v-bind:counter="50"
                  v-bind:rules="[v => !!v || 'Net ID is required']"
                  label="Queen's Net ID"

               
                  required
                  />
                 
        </v-col>
    </v-row>
    




         <v-row>
            <v-col cols="12">
               <v-btn
                  class="ma-2"
                  @click="login()"
                  :disabled="processing_request">
                  Log in
               </v-btn>

            </v-col>
         </v-row>

            </v-form>
      
      <v-row>
         <v-col cols="12">
            <v-alert type="error" v-if="login_fail" v-model="login_fail" dismissible  close-text="Close Alert">
               <ErrorDiv
                 :error_obj="login_error">

               </ErrorDiv>
            </v-alert>
         </v-col>
      </v-row>

  </v-container>


</template>



<script>
  


import {FormValidationError} from "../js_extra/web_project_error.js"
import {login} from "../js_extra/login_network.js"
import ErrorDiv from '../components/ErrorDiv.vue'

const config_data = JSON.parse(process.env.VUE_APP_CONFIG_DATA);

const server_path = config_data.vue_app_path_roots.server;



export default {
   name: 'LoginForm',
   components: { 
      ErrorDiv
   },
   props: {
   },
   data: function() {

      return {  
         form_valid: true,
         processing_request: false,
         login_fail: false,
         net_id: "",
         login_error: null,
         img_url: process.env.BASE_URL + "stargate.svg"
      };
   },

   methods: {

      login: async function () {

         const validation_result = this.$refs.form.validate();
         if (!validation_result){
            this.login_fail=true;
            this.login_error = new FormValidationError();
            return
         }
         this.processing_request=true;
         this.login_fail=false;
         var id_token;
         try {
            id_token=await login(this.net_id,server_path);
         } catch (e) {
            this.login_error = e;
            this.processing_request=false;
            this.login_fail=true;
            return;
         }
         this.processing_request=false;
         console.log(id_token)
         const queryString = window.location.search;
         const urlParams = new URLSearchParams(queryString);
         const redirect_uri = urlParams.get('redirect_uri');
         const destination_params = new URLSearchParams({
            id_token: id_token
         });
         const new_url=`${redirect_uri}?${destination_params.toString()}`;
         console.log(new_url);
         window.location.replace(new_url);
      }    
      
   },
   watch:{
   }
}
</script>





