const path = require('path');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: {
    'layout/layout': './app/static/src/js/new_layout.js'
  },
  output: {
    filename: 'js/[name].min.js',
    path: path.resolve(__dirname, './app/static/public/')
  },
  plugins: [
    new CleanWebpackPlugin(['./app/static/public/'])
  ]
}
