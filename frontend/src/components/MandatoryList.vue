<template>

    <v-list shaped>
        <v-list-item class="custom_list_top">
            <v-list-item-action>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn 
                         color="primary" 
                         icon 
                         @click="select_all"
                         v-bind="attrs"
                         v-on="on">
                            <v-icon>
                                mdi-check
                            </v-icon>
                        </v-btn>
                    </template>
                    <span>Select all items</span>
                </v-tooltip>
                
            </v-list-item-action>
             <v-list-item-content class="custom_list_top">
                    <v-list-item-title  v-text="heading"/>
            </v-list-item-content>
        </v-list-item>
        <v-list-item-group v-model="selected_internal" multiple mandatory> 
            <v-list-item
                v-for = "item in Object.keys(list_vals)"
                v-bind:key = "item"
            >
                <template v-slot:default="{ active }">
                    <v-list-item-action>
                        <v-checkbox color="primary" :input-value="active" readonly/>
                    </v-list-item-action>
                     <v-list-item-content>
                           
                           <v-list-item-subtitle  v-text="list_vals[item]"/>
                    </v-list-item-content>
                </template>

            </v-list-item>

        </v-list-item-group>
    </v-list>

</template>




<script>


export default {
    props: {
        list_data: Object,
        // this will look like
        // {
        //    "heading": "Application statuses",
        //    "items": {
        //        "application": "Application",
        //        "offered": "Offered",
        //        "accepted": "Accepted"
        //    }     
        // }

        value: Array

    },
    name: 'MandatoryList',
    data: function () {
        return {
            heading: this.list_data.heading,
            list_vals: this.list_data.items,
            selected_internal: []
        };
    },
    watch: {
        selected_internal: {
            handler: function() {
                var result=[];
                var list_keys = Object.keys(this.list_vals);
                for (var i=0; i< this.selected_internal.length;i++){
                    result.push(list_keys[this.selected_internal[i]])
                }
                if(JSON.stringify(result)!=JSON.stringify(this.value)){
                    this.$emit('input',result);
                }
            },
            deep: true
        },
        value: function(v){
            var i;
            var ideal_selected_internal=[];
            const keys = Object.keys(this.list_vals);
            var index;
            var key;
            for (i=0;i<v.length;i++){
                key = v[i];
                index = keys.indexOf(key);
                ideal_selected_internal.push(index);

            }
            if (JSON.stringify(ideal_selected_internal)!=JSON.stringify(this.selected_internal)){
                this.selected_internal=ideal_selected_internal;
            }

        }
    },
    methods: {
        select_all: function (){
            this.selected_internal=[];

            var i;
            var list_keys = Object.keys(this.list_vals);
            for (i=0;i<list_keys.length;i++){
                this.selected_internal.push(i);
                      
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