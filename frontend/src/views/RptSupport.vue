<template>
   <FormShell
   :clear-func="clear_func"
    heading="Data and Data support request"
    :submission-data="submission_data"
    :init-data="init_data"
    submit_button_label="SUBMIT YOUR SUPPORT REQUEST"
    form-type="rptsupport">
         <v-row>
            <v-col cols="6">


               <v-text-field
                  maxlength="50"
                  v-model="requestor_name"
                  disabled
                  label="Requestor name"
                  />
                   <v-text-field
                  maxlength="50"
                  v-model = "requestor_email"
                  disabled
                  label = "Requestor email"
                  required
               />
               <br/>
               <ReportChoice 
                :data_support_choices="init_data.data_support_choices"
                v-model="source_choice"
               />
            </v-col>
            <v-col cols="6">
               <v-text-field
                  maxlength="50"
                  v-model="requestor_dept"
                  v-bind:counter="50"
                  v-bind:rules="requestorDeptRules"
                  label="Requestor dept"/>
               <v-text-field
                  v-model="requestor_position"
                  v-bind:counter="100"
                  maxlength='100'
                  v-bind:rules="requestorPositionRules"
                  label="Position"
                  required/>
               <DateMenu 
                :rules="dueDateRules"
                v-model="due_date"
               />
            </v-col>
         </v-row>


         <v-row>
            <v-col cols="12">
               <p> 
                    Please indicate how we can support you with the above-mentioned report?
                    <br/>
                    <span class='text-caption'>(e.g. I don't know what X means; should X plus Y equal Z)</span>
               </p>
            </v-col>
         </v-row>
         <v-row>
 
            <v-col cols="1">
            </v-col>
            <v-col cols="11" rows="3">
                  <v-textarea
                  outlined
                  v-model="support_request_descr"
                  maxlength="500"
                  :counter="500"
                  :rules="[v => !!v || 'Problem description is required.']"
                  required/>
            </v-col>
         </v-row>
         <v-row>
             <v-col cols="12">
                  <p>Enter any needed attachments
                  <br/>
                  <span class='text-caption'>(Drag and drop is not available)</span>
                  </p>
                 <RptFileInput
                  v-model="files"/>

             </v-col>

         </v-row>

  
  </FormShell>


</template>



<script>
  


import DateMenu from '../components/DateMenu.vue'
import FormShell from '../components/FormShell.vue'
import ReportChoice from '../components/ReportChoice.vue'
import RptFileInput from '../components/FileInput.vue'
import {n_busdays_hence} from '../js_extra/utils.js';


export default {
   name: 'RptSupport',
   components: {
    FormShell,
    DateMenu,
    ReportChoice,
    RptFileInput
},
   data: function() {
      
      return {
         requestor_name: this.$store.state.user_data.display_name,
         requestor_dept: '',
         requestor_email: this.$store.state.user_data.mail,
         requestor_position: '',
         due_date: '',
         requestorEmailRules: [
            v => !!v || 'E-mail is required',
            v => /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || 'E-mail must be valid'
         ],
         requestorNameRules: [
         ],
         requestorDeptRules: [
         ],
         dueDateRules: [
            v => {
               const holidays = this.$store.state.init_data.holidays
               if (!v){
                  return 'Due date is required.'
               } else {
                  const five_busdays_hence = n_busdays_hence(5,holidays);
                  const input_date = new Date(v);
                  // input_date is 12:00 AM on date v UTC time...
                  const input_date_t = input_date.getTime()
                  const time_diff = (input_date_t - five_busdays_hence);


                  if (time_diff < 0){
                     return 'Due date must be at least five business days in the future';
                  }else{
                     return true;
                  }

               }
            }
         ],
         
         



         requestorPositionRules: [
         ],
         support_request_descr: '',
         source_choice: null,
         files: []
      };
   },
   methods: {
      clear_func(){

         this.requestor_dept="";
         this.requestor_position="";
         this.support_request_descr="";
         this.due_date="";
         this.source_choice=null;
         this.files=[];
      },
      


      requested_before: function(){
         return this.requested_before_selection==0;
      },
      close_date_dialog: function(){
         this.show_date_alert = false;
      }

   },
   computed:{
      submission_display: function() {
         return this.submission_data();
      },
      submission_data: function(){
         //var content_data = {
         //   request_type: "rptsupport",
         //   due_date: this.due_date,
         //};
         var content_data = {
            json: {},
         };
         content_data.json.due_date = this.due_date
         //if (this.requestor_name){
         //   content_data.requestor_name = this.requestor_name;
         //}
         if (this.requestor_dept){
            content_data.json.requestor_dept = this.requestor_dept;
         }
         if (this.requestor_position){
            content_data.json.requestor_position = this.requestor_position;
         }
         if (this.support_request_descr){
            content_data.json.support_request_descr = this.support_request_descr;
         }
         if(this.source_choice){
            content_data.json.source_choice = this.source_choice;
         }
         content_data.attachments=this.files;
         return content_data;
      },

      init_data: function(){
         return this.$store.state.init_data;
      }

      
   },
   watch:{


   }
}
</script>



