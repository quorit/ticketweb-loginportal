// vue.config.cjs
const j5 = require('json5');
const path = require("path");

const config_data = j5.parse(process.env.VUE_APP_CONFIG_DATA);




module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: config_data.vue_app_path_roots.frontend,
  outputDir: path.resolve(process.env.VUE_APP_VENV_ROOT,"srv/ticketweb/loginportal/frontend"),
  devServer: (process.env.NODE_ENV=='development')?{
    port: config_data.devel_server.port,
    proxy: {

         ['^' + config_data.vue_app_path_roots.server]: {
            target: config_data.devel_server.proxies.server,
            pathRewrite: {
               ['^' + config_data.vue_app_path_roots.server]: '/'
            }
         }


   }
  }:{}
  // options...
}
