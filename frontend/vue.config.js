const { defineConfig } = require('@vue/cli-service')


module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: process.env.VUE_APP_PUBLIC_PATH_ROOT + 'reporting/',

  devServer: (process.env.NODE_ENV=='development')?{
    proxy: {
         '^/reporting_static': {
            target: process.env.VUE_APP_LOCAL_STATIC_SERVER,
            pathRewrite: {
               '^/reporting_static': '/'
            }
         },
         '^/tokenserver': {
              target: process.env.VUE_APP_TOKEN_SERVER,
              pathRewrite: {
                '^/tokenserver': '/'
              }
         },
         '^/reporting_api': {
            target: process.env.VUE_APP_APP_SERVER,
            pathRewrite: {
               '^/reporting_api': '/'
            }
         }




   }
  }:{}
  // options...
}
