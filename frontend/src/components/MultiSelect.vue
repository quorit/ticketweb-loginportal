<template>
    <v-input 
     :rules="progsSelectRules"
     :value="value"
     >
     <v-container :style="{'border-style':'solid','border-width':'2px','border-radius':'5px','padding':'3px'}">
        <v-card tile :style="{'border-style':'solid'}"> 
            <v-card-title class="text-h4">
                Programs
            </v-card-title>
            <v-toolbar color="primary lighten-2">
                <v-toolbar-title>First year</v-toolbar-title>
            </v-toolbar>
            <v-container>
                <v-row>
                    <v-col cols="6"
                     v-for = "faculty in Object.keys(faculties)"
                     :key = "faculty">
                        <SelectList
                         :list_data="{ heading: faculty, items: faculties[faculty] }"
                         v-model = "progs_selected_by_faculty[faculty]"
                         :list_vals = "faculties[faculty]"> 
                        </SelectList>
                    </v-col>
                </v-row>
            </v-container>
            <v-toolbar color="primary lighten-2">
                <v-toolbar-title>Upper Year</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
            <v-combobox
                  v-model="upper_year_progs_selected"
                  :items="[]"
                  multiple
                  chips
                  deletable-chips
               >
                  <template v-slot:label>
                     Enter programs manually here.
                  </template>
               </v-combobox>
           </v-card-text>
        </v-card>
    </v-container>
    </v-input>
</template>


<script>
import SelectList from '../components/SelectList.vue'

export default {
    name: 'MultiSelect',
    components: { 
      SelectList,
    },
    props: {
        value: Object,
        // this can look like this
        // {
        //     first_year: {
        //          "FHS": ['QH'],
        //          "BISC": ['QIH','QIA']
        //     }
        //     upper_year: ['freehand text 1','freehand text 2']
        // }
        // the 'first_year' field won't exist in the object if the list would be empty.
        // The equivalent is true of the 'upper_year' field.

        faculties: Object,
        // faculties should look something like this
        // "FHS": {
        //    "QH": "Health Sciences (QH)",
        //    "QN": "Nursing (QN)"
        // },
        // "BISC": {
        //    "QIH": "BISC Health Sci (QIH)",
        //    "QIA": "BISC Arts (QIA)",
        //    "QIS": "BISC Science (QIS)",
        //    "QIB": "BISC ConEd/Arts (QIB)",
        //    "QIF": "BISC ConEd/Science (QIF)"
        // },
        // "FEAS":{
        //    "QE": "Engineering (QE)",
        //    "QEC": "Engineering, Elec & Comp (QEC)",
        //    "QEM": "Mechatronic and Robotics (QEM)"
        // }

        heading: String,
        
    },
    data: function() {
        var progs_selected_by_faculty = {};
        for (const faculty in this.faculties){
            progs_selected_by_faculty[faculty]=[];
        }
        return {
            progs_selected_by_faculty: progs_selected_by_faculty,
            progsSelectRules: [
                v => {
                        if (!("first_year" in v) && !("upper_year" in v) ){
                            //this.general_error_state=true;
                            return "You must specify one or more programs.";
                        } else {
                            return true;
                        }
                }
            ],
            upper_year_progs_selected: [],
        }

    },
    methods:{
        say: function(v){
            alert(v);
        },
        set_model_maybe: function(){
            var emit_result = {};
            var first_year_selected = false;
            var faculty;
            for (faculty in this.progs_selected_by_faculty){
                const progs_selected = this.progs_selected_by_faculty[faculty];
                if (progs_selected.length > 0){
                    first_year_selected = true;
                }
            }
            if (first_year_selected){
                emit_result.first_year = {};
                for (faculty in this.progs_selected_by_faculty){
                    const progs_selected = this.progs_selected_by_faculty[faculty];
                    if (progs_selected.length > 0){
                        emit_result.first_year[faculty]=[...progs_selected];
                    }   
                }
            }
            if(this.upper_year_progs_selected.length > 0){
                emit_result.upper_year = [...this.upper_year_progs_selected];
            }
            if (JSON.stringify(this.emit_result) != JSON.stringify(this.value)){
                this.$emit("input",emit_result);
            }
        }
    },
    computed: {
        progs_selected_txt: function(){
            return JSON.stringify(this.value);
        }
    },

    watch: {
        value(v) {
            var ideal_progs_selected_by_faculty = {};
            var faculty;
            for (faculty in this.faculties){
                ideal_progs_selected_by_faculty[faculty]=[];
            }
            if ("first_year" in v){
                for (faculty in v.first_year){
                    ideal_progs_selected_by_faculty[faculty]=[...v.first_year[faculty]];
                }
            }
            if(JSON.stringify(ideal_progs_selected_by_faculty)!=JSON.stringify(this.progs_selected_by_faculty)){
                this.progs_selected_by_faculty=ideal_progs_selected_by_faculty;
            }
            var ideal_upper_year_progs_selected=[];
            if ("upper_year" in v){
                ideal_upper_year_progs_selected = [...v.upper_year];
            }
            if(JSON.stringify(ideal_upper_year_progs_selected) != JSON.stringify(this.upper_year_progs_selected)){
                this.upper_year_progs_selected = ideal_upper_year_progs_selected;
            }


        },
        progs_selected_by_faculty: {
            handler: function() {
                this.set_model_maybe();
            },
            deep: true
        },
        upper_year_progs_selected: function(){
            this.set_model_maybe();
        }
        //we really should be watching on value too and setting progs_selected_by_faculy
         //when value changes, to make the 2-way bind actually work but we aren't ever
         //using the two-way ness so I didn't bother to implement this.
    }
}
</script>