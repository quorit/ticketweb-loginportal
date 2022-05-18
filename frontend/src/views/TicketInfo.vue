<template>
    <v-container>
        <div class="text-center">
        <v-icon
             x-large
             color="green"

            >
                mdi-check-bold
            </v-icon>
        </div>
        <v-row>
        <v-col cols="12">
                Ticket #{{id}} has been created. An accompanying email should be sent to the email address you supplied.
             </v-col>
        </v-row>
    </v-container>
  
</template>




<script>




export default {
    name: 'TicketInfo',
    props: {
        id: String
    },
    data: function() {
       return {};
    } 
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
