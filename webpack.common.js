const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const webpack = require('webpack');

module.exports = {
  entry: {
    'layout/layout': './app/static/src/js/new_layout.js',
    'landing_page': './app/static/src/js/landing_page.js',
    'signup': './app/static/src/js/signup.js',
    'account/login': './app/static/src/js/account/login.js',
    'account/password_reset_form': './app/static/src/js/account/password_reset_form.js',
    'account/signup_landing': './app/static/src/js/account/signup_landing.js',
    'account/profile_update': './app/static/src/js/account/profile_update.js',
    'account/professional_profile': './app/static/src/js/account/professional_profile.js',
    'entrepreneur/company_list': './app/static/src/js/entrepreneur/company_list.js',
    'entrepreneur/job_offers_list': './app/static/src/js/entrepreneur/job_offers_list.js',
    'corporative/contact_form': './app/static/src/js/corporative/contact_form.js'
  },
  output: {
    filename: 'js/[name].min.js',
    path: path.resolve(__dirname, './app/static/public/')
  },
  plugins: [
    new CleanWebpackPlugin(['./app/static/public/']),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    })
  ]
}
