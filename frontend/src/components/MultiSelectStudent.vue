<template>
     <v-container>
        <v-card tile>
            <v-card-title class="text-h4">
                Programs and Plans (if applicable)
            </v-card-title>
            <v-toolbar color = "primary lighten-2">
                <v-toolbar-title>Commonly selected programs</v-toolbar-title>
            </v-toolbar>
            <v-expansion-panels>
                <v-expansion-panel
                      v-for = "faculty in Object.keys(faculties)"
                     :key = "faculty"
                >
                   <v-expansion-panel-header>
                        {{  faculties[faculty]['longhand'] + ' (' + faculty + ')' }}
                   </v-expansion-panel-header> 
                   <v-expansion-panel-content>
                        <SelectListStudent
                         heading = "Select All Programs"
                         v-model = "progs_selected_by_faculty[faculty]"
                         :list_vals = "faculties[faculty]['progs']"
                         :faculty_has_certs = "faculties[faculty]['certs']"
                        />
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
            <v-toolbar color="primary lighten-2">
                <v-toolbar-title>Other programs and plans</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
            <v-combobox
                  v-model="other_plans_progs_selected"
                  :items="[]"
                  multiple
                  chips
                  deletable-chips
               >
                  <template v-slot:label>
                     Enter other programs and plans manually here.
                  </template>
               </v-combobox>
           </v-card-text>
        </v-card>
    </v-container>
</template>


<script>
import SelectListStudent from '../components/SelectListStudent.vue'

export default {
    name: 'MultiSelectStudent',
    components: { 
      SelectListStudent,
    },
    props: {
        value: Object, //list of stuff
                      //looks like
                      //
                      //{ 
                      //   common_progs: {
                      //      ASC: {
                      //          Arts: [],
                      //          Computing: []  //no concentrations/certificates chosen but none are available anyway
                      //          Certificates: True   //True means "all" selected for certificates
                      //          //Note that fine art is not in this list because it was not selected
                      //      },
                      //      SGS: 
                      //      {
                      //          masters: ["math","engl"],
                      //          phd: ["eng"]
                      //          "non-degree": [] 
                      //      }
                      //      // Note that some faculties will be excluded from this object when none of their programs are chosen                    
                      //    },
                      //    other_plans_progs: [
                      //       "plan1", "plan2"
                      //    ] 
                      // }
                      // Be aware that if no programs are selected under common_progs
                      // then the common_progs property won't exist
                      // Also if no items are selected for other_plans_progs, then other_plans_progs won't exist.
        faculties: Object,
        //see the faculties_student object in the init_data.json file for what this will look like
        heading: String
        
    },
    data: function() {
        return {
            progs_selected_by_faculty: this.progs_selected_by_faculty_from_value(),   
                                            //this will have the same format as the common_progs poperty of the
                                             // "value" model, should this property exist.
                                             // However it includes all faculties,
                                             // even the ones for which no programs are selected.
            other_plans_progs_selected: this.other_plans_progs_from_value()   
                                             //this is a mirror of the other_plans_progs field of the "value"
                                             // model should this property exist
        };
    },
    methods:{
        say: function(v){
            alert(v);
        },
        progs_selected_by_faculty_from_value: function(){
            var result = {};
            for (const faculty in this.faculties){
                result[faculty]={}
            }
            var faculty;
            if ("common_progs" in this.value){
                for (faculty in this.value.common_progs){
                    result[faculty] = JSON.parse(JSON.stringify(this.value.common_progs[faculty]))
                }
            }
            return result;
           


        },   
        other_plans_progs_from_value: function(){
            var result;
            if ("other_plans_progs" in this.value){
                result = [...this.value.other_plans_progs];
            }else{
                result = [];
            }
            return result;
        },
        emit_new_value_maybe: function(){
            var emit_result = {};
            var common_progs_selected = false;
            for (const faculty in this.progs_selected_by_faculty){
                if (Object.keys(this.progs_selected_by_faculty[faculty]).length > 0){
                    common_progs_selected = true;
                    break;
                }
            }
            if (common_progs_selected){
                emit_result.common_progs = {};
                for (const faculty in this.progs_selected_by_faculty){
                    if (Object.keys(this.progs_selected_by_faculty[faculty]).length > 0){
                        emit_result.common_progs[faculty]=JSON.parse(JSON.stringify(this.progs_selected_by_faculty[faculty]));
                    }
                }
            }

            if (this.other_plans_progs_selected.length > 0){
                emit_result.other_plans_progs = [...this.other_plans_progs_selected];
            }
            if (JSON.stringify(emit_result) != JSON.stringify(this.value)){
                this.$emit('input',emit_result);
            }
        }
    },
    computed: {
        progs_selected_txt: function(){
            return JSON.stringify(this.value);
        }
    },

    watch: {
        value: {
            handler(){
                var ideal_progs_selected_by_faculty = this.progs_selected_by_faculty_from_value();
                if (JSON.stringify(ideal_progs_selected_by_faculty)!=JSON.stringify(this.progs_selected_by_faculty)){
                    this.progs_selected_by_faculty = ideal_progs_selected_by_faculty;
                }
                var ideal_other_plans_progs = this.other_plans_progs_from_value();
                if (JSON.stringify(ideal_other_plans_progs) !=JSON.stringify(this.other_plans_progs)){
                    this.other_plans_progs = ideal_other_plans_progs;
                }
            },
            deep: true
        },
        progs_selected_by_faculty: {
            handler: function() {
                this.emit_new_value_maybe();
            },
            deep: true
        },
        other_plans_progs_selected: function() {
            this.emit_new_value_maybe();
        }
    }
}
</script>
