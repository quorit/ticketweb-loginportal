<template>
<v-combobox
 v-model="value_internal"
 :items ="items_internal"
 multiple
 chips
 deletable-chips
 :rules="requestedFieldsRules"
 :halue-comparator="value_comparator"
>
    <template v-slot:label>
        <b>Requested Fields.</b> (Fields not available in the drop-down can be added manually.)
    </template>
</v-combobox>
</template>

<script>
export default {
    name: 'SelectFields',
    props: {
        value: Array,
        // Each item of the array can look like *this*:
        // {
        //    input_type: "from_items"    
        //    key: "name_last"
        // }
        //
        // *OR*
        //
        // {
        //    input_type: "freehand"
        //    text: "I entered this myself"
        // }


        items: Object
        // items looks like
        // {
        //    "id": "ID",
        //    "name_last": "Last Name",
        //    "name_first": "Preferred First Name (when available)",
        //    "campus_email": "CAMPUS Email",
        //    "program": "Program",
        //    "plan": "Plan",
        //    "campus": "Campus",
        //    "level": "Level",
        //    "load": "Load",
        //    "term": "Term",
        //    "status": "Status"
        // }
    },
    data: function() {

        var items_internal = [];                                                
        var canonical_lookup = {};
        var key;
        for (key in this.items){
            const canonical_text = this.items[key];
            const search_text = canonical_text.toUpperCase();
            canonical_lookup[search_text] = key;
            items_internal.push(canonical_text);
        }

        return {
            items_internal: items_internal,
            value_internal: [],
            requestedFieldsRules: [
                v_list => {
                            if (v_list.length == 0) {
                                return "You must request one or more data fields.";
                            }else{
                                return true;
                            }
                        }
            ],
            canonical_lookup: canonical_lookup
        }
    },
    methods: {

        value_comparator: function(a_item,b_item){
            return a_item.toUpperCase() == b_item.toUpperCase();
        }
        
    },

    watch: {
        value(v){
            var i;
            var ideal_value_internal = [];
            var item;
            for (i=0;i<v.length;i++){
                item = v[i]
                if (item.input_type=="from_items"){
                    ideal_value_internal.push(this.items[item.key])
                }else{
                    ideal_value_internal.push(item.text);
                }
            }
            if(JSON.stringify(ideal_value_internal)!=JSON.stringify(this.value_internal)){
                this.value_internal=ideal_value_internal;
            }
        },

        value_internal: {
            handler: function() {
                var emit_result = [];
                var i;
                for (i=0;i<this.value_internal.length;i++){
                    var push_object = {};

                    var key;
                    const field_upper = this.value_internal[i].toUpperCase();
                    const values_upper = this.value_internal.map(text => text.toUpperCase());
                    if (values_upper.indexOf(field_upper) == values_upper.lastIndexOf(field_upper)){
                        if (field_upper in this.canonical_lookup){
                            key = this.canonical_lookup[field_upper];
                            var canonical_str=this.items[key];
                            push_object.input_type = "from_items";
                            push_object.key = key;
                            this.value_internal[i]=canonical_str;
                        }else{
                            push_object.input_type = "freehand";
                            push_object.text = this.value_internal[i];
                        }
                        emit_result.push(push_object);
                    }else{
                        this.value_internal.splice(i,1);
                        i--;
                    }
                    
                }
                if(JSON.stringify(this.value)!=JSON.stringify(emit_result)){
                        this.$emit('input',emit_result);
                }

            },
            deep: true
        }
    }



}
</script>
