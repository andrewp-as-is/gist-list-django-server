const path = require("path");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
//const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const ExtractCssChunks = require('extract-css-chunks-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require("terser-webpack-plugin");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

const public = 'localhost:3000';

module.exports = {
  context: __dirname,
  //entry: [path.resolve(path.dirname(__dirname), 'entry.js')],
  entry: ['../entry.js'],
  output: {
    path: path.resolve('./assets/webpack_bundles/dev/'),
    publicPath:'http://'+public+'/',
    filename: "[name]-[fullhash].js"
  },
  module: {
   rules: [
      {
        test: /\.(css)$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: { url: false }
          }
          //'style-loader',
          //{
          //  loader: 'css-loader',
          //  options: {
         //     url: false
         //   }
         // },
        ],
      },
      {
        test: /\.s[ac]ss$/i,
        sideEffects: true,
        use: [
          MiniCssExtractPlugin.loader,
          "style-loader", // Creates `style` nodes from JS strings
          {
            loader: 'css-loader',
            options: {
              url: false
            }
          },   // Translates CSS into CommonJS
          'resolve-url-loader', // add this before sass-loader
          "sass-loader",  // Compiles Sass to CSS
        ],
      }
   ],
  },
  optimization: {
    minimize: true,
    minimizer: [
    new TerserPlugin({
      terserOptions: {
          format: {
              comments: false,
          },
      },
      extractComments: false,
    }),
    new CssMinimizerPlugin({
        minimizerOptions: {
          preset: [
            'default',
            {
              discardComments: { removeAll: true },
            },
          ],
        },
      }),
      //new OptimizeCSSAssetsPlugin({
     //   cssProcessorPluginOptions: {
      //    preset: ['default', { discardComments: { removeAll: true } }],
      //  }
      //})
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
        filename: '[name]-[fullhash].css',
        chunkFilename: '[id]-[fullhash].css'
    }),
    //new ExtractCssChunks({
    //    filename: '[name]-[fullhash].css',
    //    chunkFilename: '[id]-[fullhash].css'
    //}),
    new CleanWebpackPlugin(),  // removes outdated assets from the output dir
    new WebpackManifestPlugin(),  // generates the required manifest.json file
  ],
  resolve: {
    modules: ['/usr/local/lib/node_modules'],
    preferRelative:true,
    extensions: ['.js']
  },
  resolveLoader: {
    modules: ['/usr/local/lib/node_modules'],
    extensions: ['.js'],
    mainFields: ['loader', 'main'],
  },
  devServer: {
    hot: true,
    inline: true,
    historyApiFallback: true,
    disableHostCheck: true,
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
    host: '0.0.0.0',
    port: 3000,
    public: public,
    writeToDisk: true,
  },
}
