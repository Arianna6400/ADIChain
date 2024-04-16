module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "5777"
    },
    loc_prova_prova: {
      network_id: "*",
      port: 8545,
      host: "127.0.0.1"
    }
  },
  mocha: {},
  compilers: {
    solc: {
      version: "0.8.21"
    }
  }
};
