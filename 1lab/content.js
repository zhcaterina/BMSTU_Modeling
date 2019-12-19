// noinspection JSClosureCompilerSyntax
/**
 * Файл для разового считывания и хранения таблицы рандомных чисел
 * * @returns {[
 * positionAndCount - позиция в таблице и размер результирующей таблицы,
 * table - таблица рандомных чисел
 * ]}
 */
const fs = require("fs");

module.exports = {
    positionAndCount: {pos: 0, count: 10}, // позиция в таблице и размер результирующей таблицы
    table: fs.readFileSync("numbers.txt", "utf8").replace(/\s/g,'')
};