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

import { SessionAuthenticationError,HTTPResponseError,NetworkError } from "../js_extra/network.js";
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
                return new SessionAuthenticationError("");
            }else if (this.error_type=='HTTPResponseError'){
                return new HTTPResponseError(parseInt(this.status_code),"")
            }else if (this.error_type=='NetworkError'){
                return new NetworkError("");
            }else{
                return new Error("");
            }
        }

    }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
