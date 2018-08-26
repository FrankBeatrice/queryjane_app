const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const webpack = require('webpack');

module.exports = {
  entry: {
    'layout/layout': './app/static/js/new_layout.js',
    'landing_page': './app/static/js/landing_page.js',
    'signup': './app/static/js/signup.js',
    'account/login': './app/static/js/account/login.js',
    'account/password_reset_form': './app/static/js/account/password_reset_form.js',
    'account/signup_landing': './app/static/js/account/signup_landing.js',
    'account/profile_update': './app/static/js/account/profile_update.js',
    'account/professional_profile': './app/static/js/account/professional_profile.js',
    'account/address_book': './app/static/js/account/address_book.js',
    'entrepreneur/company_list': './app/static/js/entrepreneur/company_list.js',
    'entrepreneur/job_offers_list': './app/static/js/entrepreneur/job_offers_list.js',
    'entrepreneur/company_detail': './app/static/js/entrepreneur/company_detail.js',
    'entrepreneur/general_company_form': './app/static/js/entrepreneur/general_company_form.js',
    'entrepreneur/contact_venture_form': './app/static/js/entrepreneur/contact_venture_form.js',
    'entrepreneur/role_userprofile_autocomplete': './app/static/js/entrepreneur/role_userprofile_autocomplete.js',
    'entrepreneur/job_offer_actions': './app/static/js/entrepreneur/job_offer_actions.js',
    'entrepreneur/job_offer_form': './app/static/js/entrepreneur/job_offer_form.js',
    'entrepreneur/venture_form': './app/static/js/entrepreneur/venture_form.js',
    'corporative/contact_form': './app/static/js/corporative/contact_form.js',
    'corporative/staff_company_actions': './app/static/js/corporative/staff_company_actions.js'
  },
  output: {
    filename: 'js/[name].min.js',
    path: path.resolve(__dirname, './app/static/dist/')
  },
  plugins: [
    new CleanWebpackPlugin(['./app/static/dist/']),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    })
  ]
}
