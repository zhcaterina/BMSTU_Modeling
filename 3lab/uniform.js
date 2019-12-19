/**
 * Равномерное распределение:
 * @param a - Левая граница;
 * @param b - Правая граница;
 * @param x - СВ.
 */
module.exports = {
    getUniformData: function (start, stop, a, b, func) {
        const N = 100;

        if ((a >= b) || (start >= stop)) {
            console.assert('check');
            return undefined;
        }

        const h = (stop - start) / N;
        let x = [];
        for (let i = 0; i < N; ++i)
            x.push(start + h * i);
        return x.map(value => [{'x': value, 'y': func(a, b, value)}]).reduce((acc, val) => acc.concat(val));
    },


    uniformDensity: function (a, b, x) {
        if ((x >= a) && (x <= b))
            return 1 / (b - a);
        return 0;
    },

    uniformFunction: function (a, b, x) {
        if (x < a)
            return 0;
        else if (x >= b)
            return 1;
        return ((x - a) / (b - a));
    }
};

