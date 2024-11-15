const webpack = require('webpack');

module.exports = {
  configureWebpack: {
    resolve: {
      fallback: {
        "assert": require.resolve("assert/"),
        "buffer": require.resolve("buffer/"),
        "process": require.resolve("process/browser"),
        "stream": require.resolve("stream-browserify"),
        "crypto": require.resolve("crypto-browserify")
      }
    },
    plugins: [
      new webpack.ProvidePlugin({
        process: 'process/browser',
        Buffer: ['buffer', 'Buffer'],
      }),
    ]
  }
};
