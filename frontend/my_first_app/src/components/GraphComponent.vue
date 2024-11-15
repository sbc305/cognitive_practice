<template>
  <div>
    <h2>Выберите номер трассы для построения графика</h2>
    <input type="number" v-model="traceNumber" placeholder="Введите номер трассы" min="0" max="9" />
    <button @click="plotGraph">Построить график</button>
    <button @click="toggleView">{{ isGraphView ? 'Показать данные' : 'Показать график' }}</button>

    <div v-if="isGraphView" id="myDiv" style="width: 100%; height: 400px;"></div>

    <div v-if="!isGraphView">
      <h3>Данные трассы {{ traceNumber }}</h3>
      <table border="1">
        <thead>
          <tr>
            <th>X координаты</th>
            <th>Y координаты</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="point in dataPoints" :key="point.x">
            <td>{{ point.x }}</td>
            <td>{{ point.y }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div id="errorMessage" style="color: red;">{{ errorMessage }}</div>
  </div>
</template>

<script>
import Plotly from 'plotly.js'; // Или 'plotly.js-dist', если вы установили этот пакет

export default {
  data() {
    return {
      traceNumber: null,
      errorMessage: '',
      isGraphView: true,
      dataPoints: []
    };
  },
  methods: {
    plotGraph() {
      const url = 'http://localhost:8000/data_by_id/'; // Укажите правильный URL
      this.errorMessage = ''; // Сбрасываем сообщение об ошибке

      // Проверяем, что номер трассы в допустимых пределах
      if (this.traceNumber < 0 || this.traceNumber > 9) {
        this.errorMessage = 'Такой трассы нет. Введите номер от 0 до 9.';
        this.dataPoints = []; // Очищаем данные
        return; // Прерываем выполнение функции
      }

      const user = { "id": this.traceNumber };

      fetch(url, {
        method: "POST",
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify(user)
      })
      .then(response => {
        if (!response.ok) throw new Error('Сетевая ошибка: ответ не был успешным');
        return response.json();
      })
      .then(data => {
        this.dataPoints = data; // Сохраняем данные для таблицы
        this.renderGraph(data); // Рисуем график с полученными данными
      })
      .catch(error => {
        console.error('Ошибка при получении JSON:', error);
        this.errorMessage = 'Произошла ошибка при загрузке данных.';
      });
    },
    renderGraph(data) {
      const x = data.map(point => point.x);
      const y = data.map(point => point.y);

      const trace = {
        x: x,
        y: y,
        mode: 'lines+markers',
        type: 'scatter',
        name: `Трасса ${this.traceNumber}`
      };

      const layout = {
        title: `График для трассы ${this.traceNumber}`,
        xaxis: { title: 'X координаты' },
        yaxis: { title: 'Y координаты' }
      };

      Plotly.newPlot('myDiv', [trace], layout);
    },
    toggleView() {
      this.isGraphView = !this.isGraphView; // Переключаем режим отображения
    }
  }
};
</script>

<style scoped>

</style>