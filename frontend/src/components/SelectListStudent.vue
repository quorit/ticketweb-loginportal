<template>
    <v-container>
    <v-row>
    <v-col cols="6">
    <v-list shaped>
        <v-list-item class="custom_list_top">
            <v-list-item-action>
                <v-checkbox color="primary" v-model="all_selected"/>
                
            </v-list-item-action>
             <v-list-item-content class="custom_list_top">
                    <v-list-item-title  v-text="heading"/>
            </v-list-item-content>
        </v-list-item>
        <v-list-item-group v-model="selected_internal" multiple>
            <v-list-item
                v-for = "item in list_vals_keys"
                :key = "item"
            >
                <template v-slot:default="{ active }">
                    <v-list-item-action>
                        <v-checkbox color="primary" :input-value="active"/>
                    </v-list-item-action>
                     <v-list-item-content>
                           
                           <v-list-item-subtitle  v-text="list_vals[item].longhand"/>
                    </v-list-item-content>
                </template>

            </v-list-item>

        </v-list-item-group>
    </v-list>
    </v-col>
    <v-col cols="6">
        <v-card v-for = "prog in selected_extended_progs()" class="mx-auto" :key = "prog">
            <v-toolbar  color="info lighten-2">
            <v-toolbar-title class="text-h6" color="primary">
               {{ list_vals[prog].extension.heading }}
            </v-toolbar-title>
            </v-toolbar>
            <v-container>
                
                <v-radio-group v-if = "list_vals[prog].extension.extension_type == 'some_all'" v-model = "extension_choices[prog].extension_all_some">
                    <v-radio
                        label = "Select all"
                        :value = "1"
                    />
                    <v-radio
                        label = "Choose a subset"
                        :value = "2"
                    >
                    </v-radio>
                </v-radio-group>
                <v-combobox v-if = "list_vals[prog].extension.extension_type == 'some' || list_vals[prog].extension.extension_type == 'some_all' && extension_choices[prog].extension_all_some==2"
                    v-model = "extension_choices[prog].extension_selection"
                    multiple
                    chips
                    deletable-chips
                    @update:error="error_handler"
                    :rules="combobox_rules"
                    :grules="[v => v.length > 0 || 'You must specifify one or more items']"
                >
                <template v-slot:label>
                     Enter items here.
                  </template>
                </v-combobox>
            </v-container>
        </v-card>
    </v-col>
    </v-row>
    </v-container>
</template>




<script>


export default {
    props: {
        heading: String,
        list_vals: Object, //look like
                           // {
                           //      Arts: {
                           //               extension: false
                           //      },
                           //      Computing: {
                           //               extension: true
                           //      }
                           //      Fine Art: {
                           //               extension: false     
                           //      },
                           //      Certificates: {
                           //                extension: true
                           //      }
                           // }
        value: Object,     // Might looks something like like
                          // { 
                          //    Arts: []
                          //    Computing: [sub1,sub2]
                          //    Certificates: true
                          // }
                          //
                          //
                          // Fine Art is missing which means that "Fine art" was not chosen
                          //

    },
    name: 'SelectListStudent',
    data: function () {
        var extension_choices = {};
        for (const prog in this.list_vals){
            var extension_data = this.list_vals[prog].extension;
            if (extension_data){
                extension_choices[prog] = {
                    extension_selection: [],
                };
                if(extension_data.extension_type=="some_all"){
                    extension_choices[prog].extension_all_some = 1;
                }

            }
        }

        return {
            // selected internal might look like [0,3]  //these are indices of list_vals_keys
            // extention_choices Might looks something like like
            // { 
            //    Computing: {
            //        extension_all_some: 1,   //this is the model for the "All/some menu, if there is one"
                                               //1 means that "*all* has been chosen"
            //        extension_selection [], //this is the model for the freehand certs/concentrations input, if there is one 
            //    },
            //    Certificates: {
            //         extension_all_some: 2,   //2 means that some has been chosen
            //         extension_selection: ["some_cert"]
            //    },
            //    Other: {
            //         extension_selection: []  //In this situation there is no all/some menu.
            //    }
            // }
            //
            //
            // Everything with a non-false extension value will be in this list. We won't add and remove to match with whatever is in selected internal.
            //

            selected_internal: [],
            extension_choices: extension_choices,
            all_selected: false,
            list_vals_keys: Object.keys(this.list_vals),
            combobox_rules: [(v)=>{
            if (v.length==0){
                this.$emit('errordetected');
                // I do not like doing this "emit" here (inside a rules function). We should be able to use the "update:error"
                // event on the combobox and emit from a handler for that, but *that* does not work due to vuetify bug..
                // This trick is *almost* as good.
                return 'You must specify one or more items';
            }else{
                return true;
            }
        }],

        };
    },
    
    methods: {
        error_handler(err_state){ 
            console.log("error_detected" + err_state);
            if (err_state){
                this.$emit('errordetected');
            }
        },



        get_ideal_extension_choices(){
            //we are computing a new extension_choices object based on a new *value*.
            var extension_choices = {};
            for (const prog in this.list_vals){
                var extension_data = this.list_vals[prog].extension;
                if (extension_data){
                    extension_choices[prog] = {
                        extension_selection: []
                    };
                    if(prog in this.value && typeof(this.value[prog])=="object"){ //arrays return "object" type"
                        extension_choices[prog].extension_selection = [...this.value[prog]]
                    }
                    if(extension_data.extension_type=="some_all"){
                        extension_choices[prog].extension_all_some = 1;
                        if(prog in this.value && !(this.value[prog]===true)){
                            extension_choices[prog].extension_all_some = 2;
                        }
                    }
                    

                }
            }
            return extension_choices;
        },


        selected_extended_progs: function(){
            var result = [];
            var i;
            for (i=0;i<this.selected_internal.length;i++){
                var prog = this.list_vals_keys[this.selected_internal[i]];
                if(this.list_vals[prog].extension){
                    result.push(prog)
                }
            }
            return result;

        },

        emit_new_value_maybe: function() {
            var ideal_value={};
            for (var i=0; i< this.selected_internal.length;i++){
                var prog = this.list_vals_keys[this.selected_internal[i]];
                console.log("PROG");
                console.log(prog);
                var list_val = this.list_vals[prog];
                var extension = [];
                if (list_val.extension){
                    const extension_choices = this.extension_choices[prog];
                    if (list_val.extension.extension_type == "some_all" && extension_choices.extension_all_some==1){
                        extension = true;
                    } else if ( list_val.extension.extension_type == "some" || list_val.extension.extension_type == "some_all" && extension_choices.extension_all_some==2){
                        const extension_selection = extension_choices.extension_selection;
                        extension = [...extension_selection]
                    }
                }
                ideal_value[prog]=extension;
            }
            if (JSON.stringify(ideal_value) != JSON.stringify(this.value)){
                this.$emit('input',ideal_value);
            }
        }
    },
    watch: {
        value: {
            handler(v){
                var ideal_selected_internal = [];
                const keys = this.list_vals_keys;
                var index;
                var key;

                for (key in v){
                    index = keys.indexOf(key);
                    ideal_selected_internal.push(index);
                }
                if (JSON.stringify(ideal_selected_internal)!=JSON.stringify(this.selected_internal)){
                    this.selected_internal=ideal_selected_internal;
                }

                var ideal_extension_choices = this.get_ideal_extension_choices();
                
                if (JSON.stringify(ideal_extension_choices)!=JSON.stringify(this.extension_choices)){
                    this.extension_choices=ideal_extension_choices;
                }


            },
            deep: true
        },


        all_selected: function(v) {
            var all_already_selected = this.selected_internal.length == Object.keys(this.list_vals).length;
            var none_already_selected = this.selected_internal.length == 0;
            if (v && all_already_selected || !v && none_already_selected){
                return;
            }
            console.log(none_already_selected);
            console.log(all_already_selected);
            this.selected_internal=[];
            if(this.all_selected){
                var i;
                for (i=0;i<Object.keys(this.list_vals).length;i++){
                    this.selected_internal.push(i);
                }                
            }
        },

        selected_internal: {
            handler: function() {
                const len = this.selected_internal.length;
                if (len == this.list_vals_keys.length && !this.all_selected){
                    this.all_selected = true;
                }else if (len==0 && this.all_selected){
                    this.all_selected = false;
                }
                this.emit_new_value_maybe();
            },
            deep: true
        },
        extension_choices: {
            handler: function (){
                this.emit_new_value_maybe();
            },
            deep: true

        },

    }
    
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.custom_list_top{
    background-color: var(--v-success-lighten4);
}

</style>