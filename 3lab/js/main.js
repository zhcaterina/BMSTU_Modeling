const BACKEND_ORIGIN = 'http://localhost:3000';

///////////////////////////////////////UNIFORM//////////////////////////////////////////////////////////////////////////
function getUniformData(a, b, start, stop, func) {
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
}

function uniformDensity(a, b, x) {
    if ((x >= a) && (x <= b))
        return 1 / (b - a);
    return 0;
}

function uniformFunction(a, b, x) {
    if (x < a)
        return 0;
    else if (x >= b)
        return 1;
    return (x - a)/(b - a);
}
///////////////////////////////////////ERLANG///////////////////////////////////////////////////////////////////////////
function factorial(n) {
    if (n < 0)
        return -Infinity;
    return n ? n * factorial(n - 1) : 1;
}

function getErlangData(start, stop, lambda, k, func) {
    const N = 100;

    if (start >= stop) {
        console.assert('check');
        return undefined;
    }

    const h = (stop - start) / N;
    let x = [];
    for (let i = 0; i < N; ++i)
        x.push(start + h * i);
    return x.map(value => [{'x': value, 'y': func(value, lambda, k)}]).reduce((acc, val) => acc.concat(val));
}

/**
 * @return {number}
 */
function ErlangDensity(x, lambda, k) {
    if (x < 0 || k < 0) {
        return 0;
    }
    return ((Math.pow(lambda, k)) * (Math.pow(x, (k - 1))) * Math.exp(-lambda * x))/factorial(k - 1);
}

/**
 * @return {number}
 */
function ErlangFunction(x, lambda, k) {
    if (x < 0 || k < 0)
        return 0;

    let sum = 0;
    for (let i = 0; i < k; i++)
        sum += (Math.exp(-lambda * x) * (Math.pow((lambda * x), i)))/ factorial(i);

    return 1 - sum;
}

// Все используемые нами элементы из DOM
const elements = {
    selectForm: document.querySelector('#select-form'),
    viewFormUniform: document.querySelector('#form-view-uniform'),
    formUniform: document.querySelector('#form-uniform'),
    submitButtonUniform: document.querySelector('#submit-uniform'),
    viewFormErlang: document.querySelector('#form-view-erlang'),
    formErlang: document.querySelector('#form-erlang'),
    submitButtonErlang: document.querySelector('#submit-erlang'),
    body: document.body
};

// Функция забирает данные из формы ввода и возвращает объект с этими данными
function getFormData(element) {
    // Тут вот так [['start-a', '...'], ['stop-b', '...']]
    const keyValuePairs = new FormData(element);
    // А теперь так {start-a: '...', stop-b: '...'}
    const formObject = Object.fromEntries(keyValuePairs);
    return formObject;
}

// Чистим канвасы
function destroyCanvas() {
    if (densityChart !== null) {
        console.log('destroy');
        densityChart.destroy();
    }
    if (functionChart !== null) {
        console.log('destroy');
        functionChart.destroy();
    }
}

async function drawChart(funcGetData, funcDensity, funcFunction, dataForm) {
    // Чистим канвасы
    destroyCanvas();

    let densityCanvas = document.getElementById("densityChart");
    let functionCanvas = document.getElementById("functionChart");
    Chart.defaults.global.defaultFontFamily = "Roboto";
    Chart.defaults.global.defaultFontColor = "#000";
    Chart.defaults.global.defaultFontSize = 18;
    Chart.defaults.global.defaultColor = "#FFDEAD";


    //
    let data = Object.values(dataForm).reduce((prev, curr) => [...prev,Number(curr)], []);
    let densityPoints = funcGetData(...data, funcDensity);
    let densityLabels = [], densityData = [];
    densityPoints.forEach(value => {
        densityLabels.push(value.y);
        densityData.push(value.x);
    });
    //
    let functionPoints = funcGetData(...data, funcFunction);
    let functionLabels = [], functionData = [];
    functionPoints.forEach(value => {
        functionLabels.push(value.y);
        functionData.push(value.x);
    });

    //
    let chartOptions = {
        legend: {
            display: true,
            position: 'top',
            labels: {
                boxWidth: 80,
                fontColor: 'black'
            }
        }
    };
    let densData = {
        labels:  densityData,
        datasets: [{
            label: 'Плотность распределения',
            data: densityLabels,
            backgroundColor: "#FFDEAD",
        }]
    };
    densityChart = new Chart(densityCanvas, {
        type: 'line',
        data: densData,
        options: chartOptions
    });

    let funcData = {
        labels:  functionData,
        datasets: [{
            label: 'Функция распределения',
            data: functionLabels,
            backgroundColor: "#FFDEAD",
        }]
    };
    functionChart = new Chart(functionCanvas, {
        type: 'line',
        data: funcData,
        options: chartOptions
    });
}

// Акивируем кнопку для переключения между распределениями
async function activateMath() {
    elements.selectForm.addEventListener('click', (event) => {
        // Чистим канвасы
        destroyCanvas();

        // Получаем активную кнопку
        let active = event.target.valueOf().querySelector('input');

        // Получаем форму по выбранному распределению и отрисоываем графики
        switch (active.id) {
            case "option1":
                // Показ Равномерного распределение, сокрытие Распределения Эрланга
                elements.viewFormUniform.style.display = 'block';
                elements.viewFormErlang.style.display = 'none';
                // Очистка формы Распределения Эрланга
                elements.formErlang.reset();
                // Обработчик на нажатие кнопки отправки формы
                elements.submitButtonUniform.addEventListener('click', async (event) => {
                    const data = getFormData(elements.formUniform);
                    // Отрисовка графиков
                    if (data !== null)
                        await drawChart(getUniformData, uniformDensity, uniformFunction, data);
                });
                break;
            case "option2":
                // Сокрытие Равномерного распределение, показ Распределения Эрланга
                elements.viewFormUniform.style.display = 'none';
                elements.viewFormErlang.style.display = 'block';
                // Очистка формы Равномерного Распределения
                elements.formUniform.reset();
                // Обработчик на нажатие кнопки отправки формы
                elements.submitButtonErlang.addEventListener('click', async (event) => {
                    const data = getFormData(elements.formErlang);
                    // Отрисовка графиков
                    if (data !== null)
                        await drawChart(getErlangData, ErlangDensity, ErlangFunction, data);
                });
                break;
        }
    });
}

// Главная асинхронная точка входа в программу
async function main() {
    await activateMath();
    console.log('App was successfully initialized');
}

let densityChart = null;
let functionChart = null;
//Погнали!)
main();
