

<template>
   

   <v-container>
      <v-row>
         <v-col cols="12">
            <h1>OUR/UAR web-forms login</h1>
         </v-col>
      </v-row>
      <v-form
         ref="form"
         v-model="form_valid"
         lazy-evaluation
      >
     <v-row>
         <v-col cols="12">
            <v-text-field
                maxlength="50"
                  v-model="net_id"
                  v-bind:counter="50"
                  v-bind:rules="[v => !!v || 'Net ID is required']"
                  label="Queen's Net ID"
                  />
                   <v-text-field
                  :append-icon="pass_show ? 'mdi-eye' : 'mdi-eye-off'"
                  maxlength="50"
                  :type="pass_show ? 'text' : 'password'"
                  v-model="password"
                  v-bind:counter="50"
                  v-bind:rules="[v => !!v || 'Password is required']"
                  label="Password"
                  @click:append="pass_show = !pass_show"
                  @keyup.enter="login()"
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
  
const authsystem_network = require ("authsystem_network");


import {FormValidationError} from "../js_extra/web_project_error.js"
import ErrorDiv from '../components/ErrorDiv.vue'

const config_data = JSON.parse(process.env.VUE_APP_CONFIG_DATA);

const authsystem_path = config_data.vue_app_path_roots.authsystem;



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
         password: "",
         pass_show: false,
         login_error: null
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
         try {
            await authsystem_network.login_session(this.net_id,this.password,authsystem_path,"reporting");
         } catch (e) {
            this.login_error = e;
            this.processing_request=false;
            this.login_fail=true;
            return;
         }
         this.processing_request=false;
         var route_name;
         const form_type = this.$route.params.type;
         if (form_type == 'rptsupport'){
            route_name = 'reporting_support_form';
         } else{
            route_name = 'reporting_request_forms'
         }
         var route_obj = {name: route_name};
         if (form_type != 'rptsupport'){
            route_obj.params = 
               { 
                  type: form_type
               };
         }
         await this.$router.push(route_obj);
      }    
      
   },
   watch:{
   }
}
</script>





