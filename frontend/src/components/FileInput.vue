<template>
   <v-file-input
    v-model="files"
    colorg="deep-purple accent-4"
    @change="change_event()"
    @click:clear="clear_event()"
    counter
    label="Attachments"
    multiple
    placeholder="Select your files"
    prepend-icon="mdi-paperclip"
    outlined
    :show-size="1000"
    :rules="fileRules"
  >
    <template v-slot:selection="{ index, text }">
      <v-chip
        v-if="index < 2"
        color="deep-purple accent-4"
        dark
        label
        small
      >
        {{ text }}
      </v-chip>

      <span
        v-else-if="index === 2"
        class="text-overline grey--text text--darken-3 mx-2"
      >
        +{{ files.length - 2 }} File(s)
      </span>
    </template>
  </v-file-input>


</template>

<script>

export default {
    name: 'RptFileInput',
    props: {
        value: Array
    },
    data: function() {
        const max_file_count = process.env.VUE_APP_MAX_ATTACHCOUNT || 5;
        const max_upload=process.env.VUE_APP_MAX_UPLOAD_SIZE_MB || 6;
        const max_upload_bytes = max_upload * 1000000;
        return {
            files: this.value.slice(), //shallow copy
            fileRules: [
            v => v.length <= max_file_count || 'No more than ' + max_file_count + ' attachments permitted',
            v => {
               
               var total_file_size = 0;
               for (const f of v){
                  const f_size=f.size;
                  if(f_size==0){
                    return 'Files uploaded cannot be empty'
                  }
                  total_file_size = total_file_size + f_size;
                  if (total_file_size > max_upload_bytes){
                     return 'Total file upload should not exceed ' + max_upload + ' MB';
                  }
               }
               return true;
            },
            ],
            old_files: [],
            clear_happend: false
        };
    },
    methods: {
      change_event(){
        if (!this.clear_happened && this.files.length==0){
          this.files=this.old_files.slice();
        }
        this.clear_happened=false;
        this.old_files=this.files.slice();
      },
      clear_event(){
        this.clear_happened=true;
      },


    },
    watch: {
        files: function(){
            this.old_files=this.files;
            const new_val = this.files.slice();
            this.$emit('input',new_val);
            console.log(JSON.stringify(this.files));
        },
        value: function(){
          if (this.files.length != this.value.length){
             this.files = this.value.slice();
          }
        }
    }
}


</script>