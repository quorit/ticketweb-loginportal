<template>
    
    <v-container>
        <div class="text-center">
        <v-icon
             x-large
             color="red"

            >
                mdi-alert
            </v-icon>
        </div>
        <ErrorDiv :error_obj="props_to_error()">

        </ErrorDiv>
    </v-container>
    
</template>




<script>

const rt_network = require("rt_network");

const authsystem_network = require ("authsystem_network");

import ErrorDiv from '../components/ErrorDiv.vue'


export default {
    name: 'ErrorPage',
    props: {
        error_type: String,
        status_code: String
    },
    components: {
      ErrorDiv
    },
    data: function() {
       return {
       };
    },
    methods: {
        props_to_error: function(){
            if (this.error_type=='SessionAuthenticationError'){
                return new authsystem_network.SessionAuthenticationError("");
            }else if (this.error_type=='AuthSystemHTTPResponseError'){
                return new authsystem_network.HTTPResponseError(parseInt(this.status_code),"")
            }else if (this.error_type=='AuthSystemConnectionError'){
                return new authsystem_network.ConnectionError("");
            }else if (this.error_type=='RT_HTTPResponseError'){
                return new rt_network.HTTPResponseError(parseInt(this.status_code),"")
            }else if (this.error_type=='RT_ConnectionError'){
                return new rt_network.ConnectionError("");
            }else{
                return new Error("");
            }
        }

    }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
