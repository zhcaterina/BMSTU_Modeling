const express = require("express"),
    expressLogging = require('express-logging'),
    logger = require('logops');

const app = express();
const PORT=3000;

app.use(expressLogging(logger), function (req, res, next) {
    next();
});
app.use(express.static(__dirname ));

app.listen(3000, function () {
    console.log("Сервер начал прослушивание 3000 порта");
});