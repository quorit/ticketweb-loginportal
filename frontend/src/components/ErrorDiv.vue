<template>
   <span v-if="error_obj.name=='SessionAuthenticationError'">
       <h3>Auth system authentication error</h3>
       {{ error_obj.message }}
   </span>
   <span v-else-if="error_obj.name=='RT_HTTPResponseError'">
       <h3>Application Server HTTP Response Error - {{ error_obj.status_code }}</h3>
       {{ error_obj.message }}
   </span>
   <span v-else-if="error_obj.name=='RT_ConnectionError'">
       <h3>Application Server network Error</h3>
       {{ error_obj.message }}
   </span>
   <span v-else-if="error_obj.name=='AuthSystemHTTPResponseError'">
       <h3>Authorization system HTTP Response Error - {{ error_obj.status_code }}</h3>
       {{ error_obj.message }}
   </span>
   <span v-else-if="error_obj.name=='AuthSystemConnectionError'">
       <h3>Authorization system network Error</h3>
       {{ error_obj.message }}
   </span>

   <span v-else-if="error_obj.name=='FormValidationError'">
       Form did not validate
   </span>
   <span v-else-if="error_obj.name=='NotDAError'">
       You must be a UAR Designated Approver if <i>Applicant Email</i> is included among the requested fields you have selected.
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