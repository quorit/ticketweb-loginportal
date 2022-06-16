const { defineConfig } = require('@vue/cli-service')


module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: process.env.VUE_APP_PUBLIC_PATH,

  devServer: (process.env.NODE_ENV=='development')?{
    proxy: {
         '^/application/shared_data': {
            target: process.env.VUE_APP_SHARED_DATA_SERVER_URL,
            pathRewrite: {
               '^/application/shared_data': '/'
            }
         },
         '^/authsystem_server': {
              target: process.env.VUE_APP_AUTHSYSTEM_SERVER_URL,
              pathRewrite: {
                '^/authsystem_server': '/'
              }
         },
         '^/application/server': {
            target: process.env.VUE_APP_APP_SERVER_URL,
            pathRewrite: {
               '^/application/server': '/'
            }
         }




   }
  }:{}
  // options...
}
