<template>

    <v-list shaped>
        <v-list-item class="custom_list_top">
            <v-list-item-action>
                <v-checkbox color="primary" v-model="all_selected"/>
                
            </v-list-item-action>
             <v-list-item-content class="custom_list_top">
                    <v-list-item-title  v-text="list_data.heading + (hdr_extra?' (if applicable)':'')"/>
            </v-list-item-content>
        </v-list-item>
        <v-list-item-group v-model="selected_internal" multiple>
            <v-list-item
                v-for = "item in Object.keys(list_vals)"
                v-bind:key = "item"
            >
                <template v-slot:default="{ active }">
                    <v-list-item-action>
                        <v-checkbox color="primary" :input-value="active"/>
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
        value: Array,
        // this will look like
        // ['application','accepted']
        hdr_extra: {  //use this to add "if applicable" to the header
            type: Boolean,
            default: function (){
                return false;
            }
        }
        
    },
    name: 'SelectList',
    data: function () {
        return {
            heading: this.list_data.heading,
            list_vals: this.list_data.items,
            selected_internal: [],
            all_selected: false
        };
    },
    watch: {
        value(v){
            var i;
            var ideal_selected_internal = [];
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

        },

        all_selected: function(v) {
            var all_already_selected = this.selected_internal.length == Object.keys(this.list_vals).length;
            var none_already_selected = this.selected_internal.length == 0;
            if (v && all_already_selected || !v && none_already_selected){
                return;
            }
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
                var list_keys = Object.keys(this.list_vals);
                if (len == list_keys.length && !this.all_selected){
                    this.all_selected = true;
                }else if (len==0 && this.all_selected){
                    this.all_selected = false;
                }

                var ideal_value=[];
                
                for (var i=0; i< len;i++){

                    ideal_value.push(list_keys[this.selected_internal[i]]);
                }
                if(JSON.stringify(ideal_value)!=JSON.stringify(this.value)){
                    this.$emit('input',ideal_value);
                }

            },
            deep: true
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