
// console.log(day,hour2,hour1,stavka)
// eel.expose(say_hello_js); // Expose this function to Python
// eel.test(day,hour2,hour1,stavka); // Call a Python function
function createLabel(number, titles) {
    const cases = [2, 0, 1, 1, 1, 2];
    return `${titles[number % 100 > 4 && number % 100 < 20 ? 2 : cases[number % 10 < 5 ? number % 10 : 5]]}`;
}

eel.expose(update)// получаем данные с питона
function update(day,hour1,hour2,hour3,hour4,stavka,stavka2,day1,day2){
	document.getElementsByName("day")[0].value = day //2023-09-22
	document.getElementsByName("hour1")[0].value = hour1
	document.getElementsByName("hour2")[0].value = hour2
	document.getElementsByName("hour3")[0].value = hour3
	document.getElementsByName("hour4")[0].value = hour4
	document.getElementsByName("stavka")[0].value = stavka
	document.getElementsByName("stavka2")[0].value = stavka2
	document.getElementsByName("day1")[0].value = day1
	document.getElementsByName("day2")[0].value = day2
}
function add(){
stavka = document.getElementsByName("stavka")[0].value
stavka2 = document.getElementsByName("stavka2")[0].value
hour1 = document.getElementsByName("hour1")[0].value
hour2 = document.getElementsByName("hour2")[0].value
hour3 = document.getElementsByName("hour3")[0].value
hour4 = document.getElementsByName("hour4")[0].value
day = document.getElementsByName("day")[0].value

eel.add(day,hour1,hour2,hour3,hour4,stavka,stavka2)
}
function result1() {
day1 = document.getElementsByName("day1")[0].value
day2 = document.getElementsByName("day2")[0].value
eel.result(day1,day2)
}
eel.expose(result)
function result(summa,num_day,hours3,summa_2,hours3_2){
$('.rub_access').html(`вы получите ${summa}/${summa_2} ${createLabel(summa_2, ["рубль","рубля","рублей"])}`)
$('.day_access').html(`вы работали ${num_day} ${createLabel(num_day, ["день","дня","дней"])}`)
$('.hour_access').html(`вы отработали ${hours3}/${hours3_2} ${createLabel(hours3_2.split(":")[0], ["час","часа","часов"])}`)
}


