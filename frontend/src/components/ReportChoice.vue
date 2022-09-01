<template>
    <v-card>
        <v-card-title>
            Source of report
        </v-card-title>
        <v-container>
        <v-select
          v-model="combobox_value"
          :items="combobox_choices"
          label="Select a source"
          :rules="[v => !!v || 'Source selection required']"
          outlined
        >
        </v-select>
  
          <v-text-field v-if="combobox_value=='other'"
            maxlength="50"
            v-model="other_source"
            :counter="50"
            :rules="[v => !!v || 'You must specify a source']"
            label="Specify the report source"
            required
        />
              </v-container>



    </v-card>
   

</template>




<script>


export default {
    props: {
        data_support_choices: Object,
        value: Object

        
    },
    name: 'ReportChoice',
    data: function () {
        var combobox_choices = [];
        var key;
        var new_obj;
        for (key in this.data_support_choices){
            new_obj = {
                text: this.data_support_choices[key],
                value: key
            }
            combobox_choices.push(new_obj);
        }
        new_obj = {
            divider: true
        }
        combobox_choices.push(new_obj);

        new_obj = {
            text: "Other...",
            value: "other"
        }
        combobox_choices.push(new_obj);


        combobox_choices.push(new_obj);


        return {
            combobox_choices: combobox_choices,
            combobox_value: null,
            other_source: ""
        };
    },
    methods: {
        emit_value_maybe(){
            var ideal_value = null;
            if(this.combobox_value){
                if(this.combobox_value != "other"){ //not null
                    ideal_value = {
                        rpt_source_type: "standard",
                        source_key: this.combobox_value
                    }
                } else {
                    ideal_value = {
                        rpt_source_type: "other",
                        description: this.other_source
                    }
                }
            }
            if (JSON.stringify(ideal_value)!=JSON.stringify(this.value)){
                    this.$emit('input',ideal_value);
            }
        }
        
    },
    watch: {
        combobox_value(){
            this.emit_value_maybe();

        },
        other_source(){
            this.emit_value_maybe()
        },
        value(v){
            if (!v && this.combobox_value){ //value is null
                this.combobox_value = null;
            }else if(v && v.rpt_source_type=="standard" && v.source_key != this.combobox_value){
                this.combobox_value = v.source_key;
            }else if(v && v.rpt_source_type=="other" && this.combobox_value!="other"){
                this.combobox_value="other";
            }
            if (v && v.rpt_source_type=="other" && v.description != this.other_source){
                this.other_source=v.description;
            }
    
        }

    }

    
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.custom_list_top{
    background-color: var(--v-success-lighten4);
}

</style>