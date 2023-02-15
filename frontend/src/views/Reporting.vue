<template>
   <FormShell
    :clear-func="clear_func"
    :heading="$route.params.type.charAt(0).toUpperCase() + $route.params.type.slice(1) + ' data request'"
    :submission-data="submission_data"
    submit_button_label="SUBMIT YOUR REQUEST"
    :init-data="init_data"
    :form-type="route_type"
    :designated-approver = "da_confirm || !requested_fields.includes('Applicant Email')">

    <div class="text-center" v-if="$route.params.type=='admissions'">
    <v-dialog
      v-model="da_dialog"
      width="500"
    >


      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Notice to users of this form
        </v-card-title>

        <v-card-text>
         Reports requiring applicant email addresses must be submitted by a UAR Designated Approver.
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="da_dialog = false"
          >
            I understand
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>



         <v-row>
            


            <v-col cols="6">
               <v-text-field
                  maxlength="50"
                  v-model="requestor_name"
                  label="Requestor name"
                  disabled
                  />
            </v-col>
            <v-col cols="6">
               <v-text-field
                  maxlength="50"
                  v-model="requestor_dept"
                  v-bind:counter="50"
                  v-bind:rules="requestorDeptRules"
                  label="Requestor dept"/>
            </v-col>
         </v-row>
         <v-row>
            <v-col cols="6">
               <v-text-field
                  maxlength="50"
                  v-model = "requestor_email"
                  label = "Requestor email"
                  disabled
               />
            </v-col>
            <v-col cols="6">
               <DateMenu 
                :rules = "dueDateRules"
                v-model = "due_date"
               />
            </v-col>
         </v-row>

         <v-row>
            <v-col cols="6">
               <v-text-field
                  v-model="requestor_position"
                  v-bind:counter="100"
                  maxlength='100'
                  v-bind:rules="requestorPositionRules"
                  label="Position"
                  required/>
            </v-col>

            <v-col cols="6">
               <v-text-field
                  v-model="subject"
                  v-bind:counter="100"
                  maxlength='100'
                  v-bind:rules="subjectRules"
                  label="Report title"
                  required/>
            </v-col>
         </v-row>
         <v-row>
            <v-col cols="12">
               <p>
                    Have you asked for this report before?
                    <v-btn-toggle v-model="requested_before_selection" mandatory>
                       <v-btn>
                          Yes
                       </v-btn>
                       <v-btn>
                          No
                       </v-btn>
                    </v-btn-toggle>
               </p>
            </v-col>
            <v-col cols="12">
               <p v-bind:class="requested_before()?'text--primary':'text--disabled'"> 
                    If so, provide information that would help us identify the previous report.
               </p>
            </v-col>
         </v-row>
         <v-row v-if="requested_before()">
            <v-col cols="1">
            </v-col>
            <v-col cols="11">
               <v-textarea
                  outlined
                  v-model = "prev_report_info"
                  maxlength="500"
                  v-bind:counter = "500"
                  :rules = "requested_before_rules" />
            </v-col>
         </v-row>
         <v-row>
            <v-col cols="12">
               <p> 
                    What is the purpose of this report?
                    <br/>
                    <span class='text-caption'>(i.e. communication, stats for planning/research, determine eligibility for a select service)</span>
               </p>
            </v-col>
         </v-row>
         <v-row>
            <v-col cols="1">
            </v-col>
            <v-col cols="11">
                  <v-textarea
                  outlined
                  v-model="report_purpose"
                  maxlength="500"
                  :counter="500"
                  :rules="reportPurposeRules"
                  required/>
            </v-col>
         </v-row>
         <v-row>
            <v-col cols="12">
               <TermSelect
                  v-model="terms_selected"
                  :term_bounds="term_bounds"
                  :input_required="term_required"
                  :label="term_label_extended"
               >
               </TermSelect>
            </v-col>
         </v-row>
         <v-row v-if="$route.params.type=='admissions'">
            <v-col v-for="key in Object.keys(list_choices)" cols="6" :key="key">
                  <MandatoryList
                     v-model="list_choices[key]"
                     :list_data="init_data.data_lists[key]"
                  > 
                  </MandatoryList>
            </v-col>
         </v-row>
         <v-row v-else>
            <v-col cols="12">
                  <SelectList
                    hdr_extra
                    v-model="list_choices.careers_student"
                    :list_data="init_data.data_lists.careers_student">
                  </SelectList>
            </v-col>
            <v-col cols="12">
               <MultiSelectStudent
                v-model="progs_selected"
                :faculties="init_data.faculties_student"
                heading="Programs"
               />

             </v-col>

            <v-col cols="6">
                  <SelectList
                    v-model="list_choices.term_statuses"
                    :list_data="init_data.data_lists.term_statuses"
                    hdr_extra>
                  </SelectList>
            </v-col>
            <v-col cols="6">
                  <SelectList
                    v-model="list_choices.acad_loads_student"
                    :list_data="init_data.data_lists.acad_loads_student"
                    hdr_extra>
                  </SelectList>
<v-alert type =  "info" v-model = "acad_loads_show" dismissible  close-text = "Close Alert">
               Because you are requesting information on a future dated term, depending on the purpose of your request, we may suggest including
               <i>No Load</i> among your choices for this form input.
            </v-alert>

            </v-col>
            <v-col cols="6">
                  <SelectList
                    v-model="list_choices.student_statuses"
                    :list_data="init_data.data_lists.student_statuses"
                    hdr_extra>
                  </SelectList>
                  
            </v-col>
             <v-col cols="6">
                  <SelectList
                    v-model="list_choices['campuses']"
                    :list_data="init_data.data_lists.campuses"
                    hdr_extra>
                  </SelectList>
                  
            </v-col>
         </v-row>

         <v-row v-if="$route.params.type=='admissions'"> 
            <v-col cols="12">     
                     <MultiSelect
                        v-model="progs_selected"
                        v-bind:faculties="init_data.faculties"
                        heading = "Programs"
  
                     />
            </v-col>

         </v-row>
         <v-row>
            <v-col cols="12">
               <p> 
                    Additional data requirements
                    <br/>
                    <span class='text-caption'>Use this text area to provide us with any other specifics.</span>
               </p>
            </v-col>
         </v-row>
         <v-row>
            <v-col cols="1">
            </v-col>
            <v-col cols="11">
                  <v-textarea
                  outlined
                  v-model="extra_details"
                  maxlength="500"
                  v-bind:counter="500"
                  v-bind:rules= "extraDetailsRules" />
            </v-col>
         </v-row>
                   
         <v-row>
            <v-col rows="12">
               <v-combobox
                 v-model="requested_fields"
                 :items ="field_list"
                 multiple
                 chips
                 deletable-chips
                 :rules="requestedFieldsRules"
                 :value_comparator="compare_list_items"


               >
                  <template v-slot:label>
                   <b>Requested Fields.</b> (Fields not available in the drop-down can be added manually.)
                  </template>

               </v-combobox>
<!--
               <SelectFields
                 v-model="requested_fields"
                 :items="field_dict"
               />
-->
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
         <v-row v-if="requested_fields.includes('Applicant Email')">
            <v-col cols="12">
         <v-alert type =  "info" v-model = "da_confirm_alert" dismissible  close-text = "Close Alert">
               Because <i>Applicant Email</i> is included among your selection of requested fields, you must confirm that you are a UAR Designated Approver before submission can proceed.
         </v-alert>
         <v-checkbox
         v-model="da_confirm"
         label="I am a UAR Designated Approver">

         </v-checkbox>
           </v-col>
            </v-row>
  </FormShell>


</template>



<script>
  
import MultiSelect from '../components/MultiSelect.vue'
import MultiSelectStudent from '../components/MultiSelectStudent.vue'
import MandatoryList from '../components/MandatoryList.vue'
import SelectList from '../components/SelectList.vue'
import DateMenu from '../components/DateMenu.vue'
// import SelectFields from '../components/SelectFields.vue'
import TermSelect from '../components/TermSelect.vue'
import FormShell from '../components/FormShell.vue'
import RptFileInput from '../components/FileInput.vue'

import {get_strm_bounds, get_current_term, is_n_busdays_hence} from '../js_extra/utils.js';



export default {
   name: 'ReportingForm',
   components: { 
      MultiSelect,
      MultiSelectStudent,
      MandatoryList,
      SelectList,
      DateMenu,
      // SelectFields,
      TermSelect,
      FormShell,
      RptFileInput
   },
   data: function() {
      var current_term = get_current_term();
      const route_type=this.$route.params.type;
      var list_forms;
      var list_choices={};
      if (route_type=="admissions"){
         list_forms = ["careers_adm","admit_types","acad_loads_adm","app_statuses"];
      }else{
         list_forms = ["careers_student","term_statuses","acad_loads_student","student_statuses","campuses"];
      }
      var i;
      for (i=0;i<list_forms.length;i++){
         list_choices[list_forms[i]]=[];
      }

      const field_list_codes = this.$store.state.init_data.standard_fields[route_type];
      const field_defs = this.$store.state.init_data.field_defs;
      const field_list = field_list_codes.map(code => field_defs[code]);

      return {
         response_text: '',
         requestor_name: this.$store.state.user_data.real_name,
         requestor_dept: '',
         requestor_email: this.$store.state.user_data.email,
         requestor_position: '',
         due_date: '',
         subject: '',
         requested_before_selection: 0,
         extra_details: "",
         requestorEmailRules: [
            v => !!v || 'E-mail is required',
            v => /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || 'E-mail must be valid'
         ],
         requestorNameRules: [
         ],
         requested_before_rules: [
            v => !!v || "Information about the previous request is required."
         ],
         requestorDeptRules: [
         ],
         subjectRules: [
            v => !!v || 'Report title is required.'
         ],
         dueDateRules: [
            v => !!v || 'Due date is required',
            v => is_n_busdays_hence(v,5,this.$store.state.init_data.holidays) 
                     || 'Due date must be at least five business days in the future'
         ],
         requestorPositionRules: [
         ],
         reportPurposeRules: [
            v => !!v || 'Report purpose is required.'
         ],
         extraDetailsRules: [
         ],
         
         progs_selected: {},
         prev_report_info: '',
         report_purpose: '',
         terms_selected: [],
         term_label: this.$route.params.type=="admissions"?"Admit terms":"Terms",
         term_required: this.$route.params.type=="admissions"?true:false,
         term_label_extended: this.$route.params.type=="admissions"?"Admit terms":"Terms (if applicable)",
         requested_fields: [],
         acad_loads_show: false,
         current_term: current_term,
         term_bounds: get_strm_bounds(current_term),
         list_choices: list_choices,
         list_forms: list_forms,
         requestedFieldsRules: [
                v_list => {
                            if (v_list.length == 0) {
                                return "You must request one or more data fields.";
                            }else{
                                return true;
                            }
                        }
         ],
         field_list: field_list,
         route_type: route_type,
         files: [],
         da_dialog: true,
         da_confirm_alert: false,
         da_confirm: false
      };
   },
   methods: {
      compare_list_items: function(item_a,item_b){
         return item_a.toUpperCase()==item_b.toUpperCase();
      },
      requested_before: function(){
         return this.requested_before_selection==0;
      },
      close_date_dialog: function(){
         this.show_date_alert = false;
      },
      show_date_alert_maybe: function(){
         this.acad_loads_show = false;
         if (this.list_choices.acad_loads_student.includes("no_load")){
            return;
         }
         var i;
         for(i=0;i<this.terms_selected.length;i++){
            if (this.terms_selected[i]>this.current_term){
               this.acad_loads_show = true;
            }
         }
      },
      clear_func(){
         var item;
         this.requestor_dept="";
         this.requestor_position="";
         this.subject="";
         this.requested_before_selection=0;
         this.prev_report_info="";
         this.report_purpose="";
         this.extra_details="";
         for (item in this.list_choices){
            this.list_choices[item]=[];
         }
         this.progs_selected={};
         this.terms_selected=[];
         this.due_date='';
         this.requested_fields=[];
         this.files=[];
         this.da_confirm=false;
      }

   },
   computed:{
      submission_display: function() {
         return this.submission_data();
      },

      init_data: function(){
         return this.$store.state.init_data;
      },
     
      field_dict: function(){
         const field_list = this.$store.state.init_data.standard_fields[this.$route.params.type];
         var field_dict = {};
         var i;
         for (i=0;i<field_list.length;i++){
            const this_field = field_list[i];
            field_dict[this_field]= this.$store.state.init_data.field_defs[this_field];
         }
         return field_dict;

      },
      submission_data: function(){


         var content_data = {
            json: { 
               subject : this.subject,
               requested_fields: this.requested_fields,
               due_date: this.due_date
            }
         };

         if (this.requestor_dept){
            content_data.json.requestor_dept = this.requestor_dept;
         }
         if (this.requestor_position){
            content_data.json.requestor_position = this.requestor_position;
         }
         if (this.prev_report_info){
            content_data.json.prev_report_info = this.prev_report_info;
         }
         if (this.report_purpose){
            content_data.json.report_purpose = this.report_purpose;
         }

         if (this.terms_selected.length >0){
            content_data.json.terms = this.terms_selected;
         }
         if (Object.keys(this.progs_selected).length > 0){
            content_data.json.progs = this.progs_selected;
         }
         var list_choices_exist=false;
         var list_choices_local={};
         var item;
         for (item in this.list_choices){
            if (this.list_choices[item].length > 0){
               list_choices_exist=true;
               list_choices_local[item]=this.list_choices[item];
            }
         }
         if(list_choices_exist){
            content_data.json.list_choices = list_choices_local;
         }
         if (this.extra_details){
            content_data.json.extra_details = this.extra_details;
         }
         content_data.attachments=this.files;
         return content_data;
      }

      
   },
   watch:{ 
      requested_fields: function(val) {
         this.da_confirm_alert = val.includes("Applicant Email") && !this.da_confirm;
      },
      da_confirm(val){
         this.da_confirm_alert=!val;
      },

      terms_selected: {        
         handler() {
            if(this.$route.params.type=='student'){
               this.show_date_alert_maybe();
            }
         },
         deep: true
      },



      requested_before_selection: function(){
         if (this.requested_before_selection == 1 ){
            this.prev_report_info='';
         }
      },

      'list_choices.acad_loads_student': function(){
         this.show_date_alert_maybe();
      }
   }
}
</script>



