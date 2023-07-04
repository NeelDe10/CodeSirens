const express = require('express');
const router = express.Router();
const marketDataController = require('../controller/marketDataController');

router.post('/marketdata', marketDataController.createMarketData);

module.exports = router;
