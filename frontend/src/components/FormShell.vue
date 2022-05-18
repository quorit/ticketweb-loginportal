<template>
   <v-container v-if="ticket_id">
       <div class="text-center">
        <v-icon
             x-large
             color="green"

            >
                mdi-check-bold
            </v-icon>
        </div>
        <v-row>
        <v-col cols="12">
                Ticket #{{ ticket_id }} has been created. An accompanying email should be sent to the email address you supplied.
             </v-col>
        </v-row>

   </v-container>
   <v-container v-else>
      <v-row>
         <v-col cols="12">
            <h1>{{ heading }}</h1>
         </v-col>
      </v-row>
      <v-form
         ref="form"
         v-model="form_valid"
         lazy-evaluation
      >
         <slot/>
         <v-row>
            <v-col cols="12">
               <v-btn
                  class="ma-2"
                  @click="submit_ticket"
                  :disabled="processing_request">
                  {{ submit_button_label }}
               </v-btn>
               <v-btn
                  class="ma-2"
                  @click="reset_all()"
                  :disabled="processing_request">
                  Reset this form
               </v-btn>

            </v-col>
         </v-row>

            </v-form>
      
      <v-row>
         <v-col cols="12">
            <v-alert type="error" v-if="submit_fail" v-model="submit_fail" dismissible  close-text="Close Alert">
               <ErrorDiv
                 :error_obj="submit_error">

               </ErrorDiv>
            </v-alert>
         </v-col>
      </v-row>

      <div v-if="devel_mode">
            {{ submission_display }}
       </div>
  </v-container>


</template>



<script>
  

import {create_html} from '../js_extra/ticket_content.js';
import {submit_json,get_app_token,SessionAuthenticationError} from '../js_extra/network.js';
import {FormValidationError} from '../js_extra/web_project_error.js'
import ErrorDiv from './ErrorDiv.vue'

export default {
   name: 'FormShell',
   components: {
      ErrorDiv
   },
   props: {
        clearFunc: Function,
        submissionData: Object,
        heading: String,
        initData: Object,
        submit_button_label: String,
        formType: String
   },
   data: function() {


      return {
         response_text: '',         
         form_valid: true,
         processing_request: false,
         submit_fail: false,
         submit_error: null,
         devel_mode: process.env.NODE_ENV === 'development',
         ticket_id: null
      };
   },
   methods: {
      

      validate_form: function (app_token){
         return (new Promise((resolve,reject)=>{
            const validation_result = this.$refs.form.validate();
            if (validation_result){
               resolve(app_token)  //just passes the app token down the chain.
                                   //Not used by this function which is not really async
            }else{
               const err= new FormValidationError();
               reject(err)
            }
         }));
      },


      submit_ticket: async function () {
         this.processing_request=true;
         this.submit_fail=false;
         var response_json=null;
         try {
            response_json = await get_app_token()
                                 .then(this.validate_form)
                                 .then(app_token => submit_json(this.submission_data(),this.formType,app_token))
         } catch(e){
            if (e instanceof SessionAuthenticationError){
               //this should cover...missing session cookie, expired session
               //anyhitng that would result in an "401 Unauthorized". Don't forget that
               //the language of 'Unauthorized' in HTTP codes is wrong
               //and really refers to authentication problems.
               this.$router.go();
            } else {
               this.submit_error=e;
               this.processing_request=false;
               this.submit_fail=true;
            }
            return;
         }
         this.ticket_id = response_json.id
         this.processing_request=false;
      },
      submission_data: function(){
         var returnObj = {
            content_data: create_html(this.initData,this.formType,this.submissionData),
         };
         if (this.formType != "rptsupport"){
            returnObj.subject = this.submissionData.subject
         }


         if ('dueDate' in this.submissionData){
            returnObj.due_date=this.submissionData.dueDate;
          
         }
         return returnObj;
      },

      reset_all: async function(){
        try {
           await get_app_token(); //don't care what the app_token is
        } catch (e){
           if (e instanceof SessionAuthenticationError){
               //this should cover...missing session cookie, expired session
               //anyhitng that would result in an "401 Unauthorized". Don't forget that
               //the language of 'Unauthorized' in HTTP codes is wrong
               //and really refers to authentication problems.
               this.$router.go();
           }
           //we don't care about other errors that may result. not relevant
        }
        this.clearFunc();
        this.submit_fail=false;
        this.$refs.form.resetValidation();
      }

   },
   computed:{
      submission_display: function() {
         return this.submission_data();
      }      
      
   },
   watch:{
   }
}
</script>





