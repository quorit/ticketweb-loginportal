const { defineConfig } = require('@vue/cli-service')
const path = require("path")

module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: process.env.VUE_APP_PUBLIC_PATH,
  outputDir: path.resolve(process.env.VUE_APP_VENV_ROOT,"srv/ticketweb/applications/reporting/frontend"),
  devServer: (process.env.NODE_ENV=='development')?{
    port: process.env.VUE_APP_PORT,
    proxy: {
         ['^' + process.env.VUE_APP_SHARED_DATA_PATH]: {
            target: process.env.VUE_APP_SHARED_DATA_SERVER_URL,
            pathRewrite: {
               ['^' + process.env.VUE_APP_SHARED_DATA_PATH]: '/'
            }
         },
	 ['^' + process.env.VUE_APP_AUTHSYSTEM_PATH]: {
              target: process.env.VUE_APP_AUTHSYSTEM_SERVER_URL,
              pathRewrite: {
                ['^' + process.env.VUE_APP_AUTHSYSTEM_PATH]: '/'
              }
         },
         ['^' + process.env.VUE_APP_APP_SERVER_PATH]: {
            target: process.env.VUE_APP_APP_SERVER_URL,
            pathRewrite: {
               ['^' + process.env.VUE_APP_APP_SERVER_PATH]: '/'
            }
         }




   }
  }:{}
  // options...
}