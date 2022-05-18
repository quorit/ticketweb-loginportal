<template>
   <span v-if="error_obj.name=='SessionAuthenticationError'">
       <h3>Authentication error</h3>
       {{ error_obj.message }}
   </span>
   <span v-else-if="error_obj.name=='HTTPResponseError'">
       <h3>HTTP Response Error - {{ error_obj.status_code }}</h3>
       {{ error_obj.message }}
   </span>
   <span v-else-if="error_obj.name=='NetworkError'">
       <h3>Network Error</h3>
       {{ error_obj.message }}
   </span>
   <span v-else-if="error_obj.name=='FormValidationError'">
       Form did not validate
   </span>
   <span v-else>
       <h3>Uncategorized error</h3>
       {{ error_obj.message }}
   </span>


   

</template>

<script>




export default {
    props: {
        error_obj: Error
    },
    name: 'ErrorDiv',
}
</script>