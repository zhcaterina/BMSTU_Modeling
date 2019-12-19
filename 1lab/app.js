const express = require("express");
const bodyParser = require("body-parser");
const content = require("./content");
const random = require("./random");
const criterions = require("./criterions");

const app = express();
const jsonParser = bodyParser.json();
// Таблица рандомных чисел
const table = content.table;
// Позиция в таблице и используемый размер
const positionAndCount = content.positionAndCount;

// Загрузка страницы
app.use(express.static(__dirname + "/public"));

// Получение табличных значений рандомных чисел
app.get("/api/table", function(request, response){
    let points = []; // таблица с точками
    // Проверка, что позиция в таблице случайных чисел не выйдет за пределы таблицы
    if (positionAndCount.pos > table.length + positionAndCount.count * 6)
        positionAndCount.pos = 0;
    // Одноразрядные числа
    let firstPoints = table.slice(positionAndCount.pos).match(/\d/g).slice(0, positionAndCount.count);
    positionAndCount.pos += positionAndCount.count;
    // Двухразрядные числа
    let secondPoints = table.slice(positionAndCount.pos).match(/[1-9]\d/g).slice(0, positionAndCount.count);
    positionAndCount.pos += positionAndCount.count * 2;
    // Трехразрядные числа
    let thirdPoints = table.slice(positionAndCount.pos).match(/[1-9]\d\d/g).slice(0, positionAndCount.count);
    positionAndCount.pos += positionAndCount.count * 3;
    // Заполнение словаря для таблицы
    for (let i = 0; i < positionAndCount.count; ++i)
        points.push({
            id: (i+1).toString(),
            oneDigit:   firstPoints[i].toString(),
            twoDigit:   secondPoints[i].toString(),
            threeDigit: thirdPoints[i].toString()
        });
    //
    let resCriterions = {
        oneDigit: (criterions(0, 9, firstPoints)*100).toFixed(2),
        twoDigit: (criterions(10, 99, secondPoints)*100).toFixed(2),
        threeDigit: (criterions(100, 999, thirdPoints)*100).toFixed(2)
    };
    // Отправление структуры
    response.send({points: points, resCriterions: resCriterions});
});

// Получение алгоритмических значений рандомных чисел
app.get("/api/random", function (request, response) {
    let points = []; // таблица с точками
    // Одноразрядные числа
    let firstPoints = random(0, 9, table[positionAndCount.pos], positionAndCount.count);
    // Двухразрядные числа
    let secondPoints = random(10, 99, table[positionAndCount.pos+1], positionAndCount.count);
    // Трехразрядные числа
    let thirdPoints = random(100, 999, table[positionAndCount.pos+2], positionAndCount.count);

    positionAndCount.pos += 6;
    // Заполнение словаря для таблицы
    for (let i = 0; i < positionAndCount.count; ++i)
        points.push({
            id: (i+1).toString(),
            oneDigit:   firstPoints[i].toString(),
            twoDigit:   secondPoints[i].toString(),
            threeDigit: thirdPoints[i].toString()
        });
    //
    let resCriterions = {
        oneDigit: (criterions(0, 9, firstPoints)*100).toFixed(2),
        twoDigit: (criterions(10, 99, secondPoints)*100).toFixed(2),
        threeDigit: (criterions(100, 999, thirdPoints)*100).toFixed(2)
    };
    // Отправление структуры
    response.send({points: points, resCriterions: resCriterions});
});
//
app.post('/api/check', jsonParser, function (request, response) {
    if(!request.body) return response.sendStatus(400);

    let digital = request.body.digital;
    console.log(digital);
    let resCriterions = (criterions(0, 9, digital)*100).toFixed(2);
    console.log(resCriterions);
    response.send(resCriterions);
});

app.listen(3000, function () {
    console.log("Сервер начал прослушивание 3000 порта");
});
