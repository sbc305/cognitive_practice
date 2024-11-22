<template>
  <div>
    <h2>Выберите временной интервал для построения графика</h2>
    
    <div>
      <label for="startTime">Начальное время (YYYY-MM-DD HH:mm:ss):</label>
      <input type="text" v-model="startTime" placeholder="2024-08-21 09:26:38" />
      <div v-if="startTimeError" style="color: red;">{{ startTimeError }}</div>
    </div>
    
    <div>
      <label for="finishTime">Конечное время (YYYY-MM-DD HH:mm:ss):</label>
      <input type="text" v-model="finishTime" placeholder="2024-08-21 09:27:38" />
      <div v-if="finishTimeError" style="color: red;">{{ finishTimeError }}</div>
    </div>

    <button @click="plotGraph">Построить график</button>
    <button @click="toggleView">{{ isGraphView ? 'Показать данные' : 'Показать график' }}</button>

    <div v-if="isGraphView" id="myDiv" style="width: 100%; height: 400px;"></div>

    <div v-if="!isGraphView">
      <h3>Данные по выбранному интервалу</h3>
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
//библиотеки
import Plotly from 'plotly.js'; 

export default {
  data() {
    return {
      startTime: '',
      finishTime: '',
      startTimeError: '',
      finishTimeError: '',
      errorMessage: '',
      isGraphView: true,
      dataPoints: []
    };
  },
  methods: {
    validateTimestamp(timestamp) {
      const regex = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;
      if (!regex.test(timestamp)) {
        return 'Неверный формат времени. Используйте YYYY-MM-DD HH:mm:ss.';
      }

      const date = new Date(timestamp);
      if (isNaN(date.getTime())) {
        return 'Неверная дата или время.';
      }

      return '';
    },

    validateTimes() {
      this.startTimeError = this.validateTimestamp(this.startTime);
      this.finishTimeError = this.validateTimestamp(this.finishTime);

      // Проверка на то, что начальное время не больше конечного
      if (!this.startTimeError && !this.finishTimeError) {
        const startDate = new Date(this.startTime);
        const finishDate = new Date(this.finishTime);
        
        if (startDate > finishDate) {
          this.startTimeError = 'Начальное время не может быть больше конечного времени.';
        }
      }
    },
    
    plotGraph() {
      const url = 'http://localhost:8000/data/'; 
      this.errorMessage = ''; // Сбрасываем сообщение об ошибке
      this.validateTimes(); // Выполняем валидацию

      // Проверяем наличие ошибок
      if (this.startTimeError || this.finishTimeError) {
        return; // Прерываем выполнение функции, если есть ошибки
      }

      const user = {
        "start_time": this.startTime,
        "finish_time": this.finishTime
      };

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
        name: `Данные с ${this.startTime} по ${this.finishTime}`
      };

      const layout = {
        title: `График с ${this.startTime} по ${this.finishTime}`,
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

input {
  width: 200px;
}
</style>