<template>

   
               <v-menu
                  ref = "dateMenu"
                  v-model="dateMenu"
                  :close-on-content-click="false"
                  :return-value.sync= "dueDate"
                  transition="scale-transition"
                  persistent
                  min-width="auto"
                  offset-y
               >
                  <template v-slot:activator="slotProps">
                    

                     <v-text-field
                        maxlength = "50"
                        v-model = "dueDate"
                        :rules="rules"
                        prepend-icon = "mdi-calendar"
                        label = "Date due"
                        readonly
                        v-bind = "slotProps.attrs"
                        v-on = "slotProps.on"
                        required
                        clearable/>
                  </template>
                  <v-date-picker
                     v-model= "dueDate"
                     no-title
                     scrollable
                  >
                     <v-spacer/>
                     <v-btn
                        text
                        color="primary"
                        @click = "dateMenu = false"
                     >
                        Cancel
                     </v-btn>
                     <v-btn
                        text
                        color = "primary"
                        @click = "$refs.dateMenu.save(dueDate)"
                     >
                        Ok
                     </v-btn>

                  </v-date-picker>
   </v-menu>
</template>

<script>
export default {
    props: {
        value: String,
        rules: Array
    },
    name: 'DateMenu',
    data: function () {
         return {
            dueDate: this.value,
            dateMenu: false,
            show_date_message: false
         }
    },
    watch: {
         value(v){
            if(v != this.dueDate){
               this.dueDate=v;
            }
         },
         dueDate: function (){
            if (this.value != this.dueDate){
               this.$emit('input',this.dueDate);
            }
         },
         dateMenu: function(){
            if (this.dateMenu){
              this.show_date_message=true;
              }
         }
    }
}
</script>