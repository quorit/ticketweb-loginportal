<template>
<v-combobox
 v-model="internal_model"
 :items="term_texts"
 multiple
 chips
 deletable-chips
 :rules="rules"
 :halue-comparator = "(a,b) => (a.toUpperCase() == b.toUpperCase())"
>
    <template v-slot:label>
        <h3>{{ label }}</h3>
    </template>
</v-combobox>
</template>


<script>

import {term_lookup, strm_get_prev} from '../js_extra/utils.js';

export default {
    name: 'TermSelect',
    props: {
        value: Array,
        input_required: Boolean,
        term_bounds: Object,
        // looks like
        // {
        //    begin: '2131'
        //    end: '2249'
        // }
        label: String
    },
    data: function(){
        var term_reverse_lookup = {};
        var term_texts = [];
        var term_texts_upper = [];
        var term_iterator = this.term_bounds.end;
        var rules;
        if (this.input_required){
            rules = [
                v_list => {
                        if (v_list.length == 0) {
                           return "You must select one or more admit terms.";
                        }else{
                           return true;
                        }
                    }
            ];
        } else {
            rules = [];
        }
        while (term_iterator >= this.term_bounds.begin){
            var text = term_lookup(term_iterator);
            var text_upper = text.toUpperCase();
            term_reverse_lookup[text_upper] = term_iterator;
            term_texts.push(text);
            term_texts_upper.push(text_upper);
            term_iterator = strm_get_prev(term_iterator);
        }
        return {
            term_reverse_lookup: term_reverse_lookup,
            term_texts: term_texts,
            term_texts_upper: term_texts_upper,
            rules: rules,
            internal_model: []
        };
    },
    watch: {
        value(v){
            var ideal_internal_model = [];
            var i;
            for (i=0;i<v.length;i++){
                ideal_internal_model.push(term_lookup(v[i]));
            }
            if (JSON.stringify(ideal_internal_model)!=JSON.stringify(this.internal_model)){
                this.internal_model=ideal_internal_model;
            }
        },
        internal_model: function () {
            var i;

            for (i=0;i<this.internal_model.length;i++){
                const term_upper = this.internal_model[i].toUpperCase();
                const model_upper = this.internal_model.map(val => val.toUpperCase());
                if (!this.term_texts_upper.includes(term_upper) || model_upper.indexOf(term_upper)!= model_upper.lastIndexOf(term_upper)){
                    this.internal_model.splice(i,1);
                    i--;
                }
            }


            var emit_result = [];
            for (i=0; i< this.internal_model.length; i++){
                var ps_term = this.term_reverse_lookup[this.internal_model[i].toUpperCase()]
                var text_canonical = term_lookup(ps_term);
                this.internal_model[i]=text_canonical;
                emit_result.push(ps_term);
            }
            if(JSON.stringify(emit_result) != JSON.stringify(this.value)){
                this.$emit('input',emit_result);
            }

        }
        
    }
}
</script>