const { defineConfig } = require('@vue/cli-service')


module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: process.env.VUE_APP_PUBLIC_PATH,

  devServer: (process.env.NODE_ENV=='development')?{
    port: process.env.VUE_APP_PORT,
    proxy: {
         '^/apps/reporting/shared_data': {
            target: process.env.VUE_APP_SHARED_DATA_SERVER_URL,
            pathRewrite: {
               '^/apps/reporting/shared_data': '/'
            }
         },
         '^/authsystem_server': {
              target: process.env.VUE_APP_AUTHSYSTEM_SERVER_URL,
              pathRewrite: {
                '^/authsystem_server': '/'
              }
         },
         '^/apps/reporting/server': {
            target: process.env.VUE_APP_APP_SERVER_URL,
            pathRewrite: {
               '^/apps/reporting/server': '/'
            }
         }




   }
  }:{}
  // options...
}
