const mongoose = require('mongoose');

const marketDataSchema = new mongoose.Schema({
  symbol: {
    type: String,
    required: true,
  },
  oi: {
    type: Number,
    required: true,
  },
  chngInOi: {
    type: Number,
    required: true,
  },
  volume: {
    type: Number,
    required: true,
  },
  iv: {
    type: Number,
    required: true,
  },
  ltp: {
    type: Number,
    required: true,
  },
  chng: {
    type: Number,
    required: true,
  },
  bidQty: {
    type: Number,
    required: true,
  },
  bid: {
    type: Number,
    required: true,
  },
  ask: {
    type: Number,
    required: true,
  },
  askQty: {
    type: Number,
    required: true,
  },
  strike: {
    type: Number,
    required: true,
  },
});

const MarketData = mongoose.model('MarketData', marketDataSchema);

module.exports = MarketData;
