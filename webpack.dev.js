const path = require('path');
const webpack = require('webpack');
const merge = require('webpack-merge');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',
  plugins: [
    new webpack.HotModuleReplacementPlugin()
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
        }
      },
      {
        test: /\.(css|sass|scss)$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: ['css-loader', 'sass-loader']
        })
      },
      {
        test: /\.(png|jp(e*)g|svg)$/,
        use: [{
          loader: 'file-loader',
          options: {
            context: path.resolve(__dirname, './app/static/src/img'),
            name: '[path][name].[ext]',
            outputPath: 'img/',
            publicPath: '/static/public/img/'
          }
        }]
      }
    ]
  },
  devtool: 'inline-source-map',
  plugins: [
    new ExtractTextPlugin({
      filename: 'css/[name].min.css',
      allChunks: true
    })
  ],
  devServer: {
    publicPath: '/static/public/',
    port: 8080,
    proxy: {
      '/': 'http://127.0.0.1:8000'
    }
  }
});
