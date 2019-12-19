/**
 * Получение рандомного элемента ЛКМ
 * @param a - Левая граница
 * @param b - Правая граница
 * @param k - Первое случайное число
 * @param count - Кол-во случайных чисел
 * @returns {[]}
 */
module.exports = function (a, b, k=0, count=10) {
    let points = [];
    for (let i = 0; i < count; ++i) {
        k = a+randomLKG(k) % (b - a + 1);
        points.push(k);
    }
    return points;
};

// Получение рандомных чисел ЛКМ
/**
 * Линейно Конгруентный Метод
 * @param k - Прыдущий случайный элемент
 * @returns {number} - Случайный элемент, полученный ЛКМ
 */
function randomLKG(k) {
    const c = 2**10;
    const a = 25214903917;
    const b = 11;
    return (a*k - 1+b) % c;
}