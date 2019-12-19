/**
 *
 * @param lst
 * @returns {number}
 */
function serial_criterion(lst) {
    let n = lst.length;
    let sumUU = 0;
    let sumU = 0;
    let sumU2 = 0;
    for (let i = 0; i < n; i++) {
        let numj = Number(lst[(i+1) % n]);
        let numi = Number(lst[i]);

        sumU += numi;
        sumU2 += numi * numi;
        sumUU += numi * numj;
    }
    let top = n * sumUU - sumU ** 2;
    let bottom = n * sumU2 - sumU ** 2;

    let a = top / bottom;
    let coef = Math.abs(a);

    return isNaN(coef) ? 0 : 1 - coef;
}

/**
 *
 * @param a
 * @param b
 * @param lst
 * @param uni
 * @param cor
 * @param ent
 * @returns {number}
 */
module.exports = function(a, b, lst, uni=true, cor=true, ent=true) {
    let res = uni ? serial_criterion(lst) : 1;
    console.log(res);
    return res;
};
