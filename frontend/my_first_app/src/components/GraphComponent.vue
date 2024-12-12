<template>
  <div>
    <h2>Выберите режим ввода</h2>
    <button @click="toggleInputMode">{{ isTimeInput ? 'Переключить на ввод ID трассы' : 'Переключить на ввод времени' }}</button>

    <div v-if="isTimeInput">
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

      <button @click="plotGraphByTime">Построить график</button>
    </div>

    <div v-else>
      <h2>Выберите номер трассы для построения графика</h2>
      <input type="number" v-model="traceNumber" placeholder="Введите номер трассы" min="0" max="11" />
      <button @click="plotGraphById">Построить график</button>
    </div>

    <!-- Сообщение о загрузке -->
    <div v-if="isLoading" style="color: blue;">Обработка данных, пожалуйста подождите...</div>

    <!-- Кнопка для переключения между графиком и данными -->
    <button @click="toggleView">{{ isGraphView ? 'Показать данные' : 'Показать график' }}</button>

    <!-- Отображаем график -->
    <div id="myDiv" style="width: 100%; height: 400px;" v-if="isGraphView"></div>

    <!-- Отображаем данные, если не график -->
    <div v-if="!isGraphView">
      <h3>Данные по выбранному интервалу или трассе</h3>
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

    <!-- Сообщение об ошибке -->
    <div id="errorMessage" style="color: red;">{{ errorMessage }}</div>
  </div>
</template>

<script>
// библиотеки
import Plotly from 'plotly.js'; 

export default {
  data() {
    return {
      startTime: '',
      finishTime: '',
      startTimeError: '',
      finishTimeError: '',
      errorMessage: '',
      isGraphView: true, // Изначально показываем график
      isTimeInput: true, // Начинаем с режима ввода времени
      traceNumber: null,
      dataPoints: [],
      isLoading: false, // состояние для отображения загрузки
      graphTitle: '' // Заголовок графика
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

      if (!this.startTimeError && !this.finishTimeError) {
        const startDate = new Date(this.startTime);
        const finishDate = new Date(this.finishTime);
        
        if (startDate > finishDate) {
          this.startTimeError = 'Начальное время не может быть больше конечного времени.';
        }
      }
    },

    plotGraphByTime() {
      const url = 'http://localhost:8000/data/';
      this.errorMessage = '';
      this.validateTimes();

      if (this.startTimeError || this.finishTimeError) {
        return;
      }

      const user = {
        "start_time": this.startTime,
        "finish_time": this.finishTime
      };

      this.isLoading = true; // Устанавливаем состояние загрузки

      fetch(url, {
        method: "POST",
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify(user)
      })
      .then(response => {
        if (!response.ok) { 
          return response.json().then(err => { // Считываем сообщение об ошибке из ответа
            throw new Error(err.message || 'Ошибка при обработке запроса.');
          });
        }
        
        return response.json();
       })
       .then(data => {
         this.dataPoints = data;
         this.isGraphView = true;
         this.graphTitle = `График с ${this.startTime} по ${this.finishTime}`; // Устанавливаем заголовок графика
         this.renderGraph(data); // Рисуем график сразу после получения данных
       })
       .catch(error => {
         console.error('Ошибка при получении JSON:', error);
         this.errorMessage = error.message; // Устанавливаем сообщение об ошибке
       })
       .finally(() => {
         this.isLoading = false; // Сбрасываем состояние загрузки
       });
    },

    plotGraphById() {
      const url = 'http://localhost:8000/data/';
      
      if (this.traceNumber < 0 || this.traceNumber > 11) {
        this.errorMessage = 'Такой трассы нет. Введите номер от 0 до 11.';
        this.dataPoints = [];
        return;
      }

      const user = { "file_id": this.traceNumber };

      this.isLoading = true; // Устанавливаем состояние загрузки

      fetch(url, {
        method: "POST",
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify(user)
      })
      .then(response => {
        if (!response.ok) { 
          return response.json().then(err => { // Считываем сообщение об ошибке из ответа
            throw new Error(err.message || 'Ошибка при обработке запроса.');
          });
        }
        
        return response.json();
       })
       .then(data => {
         this.dataPoints = data;
         this.isGraphView = true; 
         this.graphTitle = `График ID ${this.traceNumber}`; // Устанавливаем заголовок графика
         this.renderGraph(data); // Рисуем график сразу после получения данных
       })
       .catch(error => {
         console.error('Ошибка при получении JSON:', error);
         this.errorMessage = error.message; // Устанавливаем сообщение об ошибке
       })
       .finally(() => {
         this.isLoading = false; // Сбрасываем состояние загрузки
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
         name: `Данные`
       };

       const layout = {
         title: this.graphTitle, // Используем заголовок графика из переменной
         xaxis: { title: 'X координаты' },
         yaxis: { title: 'Y координаты' }
       };

       Plotly.newPlot('myDiv', [trace], layout);
     },

     toggleView() {
       // Переключаем режим отображения
       this.isGraphView = !this.isGraphView;

       // Если переключаемся на график, перерисовываем его
       if (this.isGraphView && this.dataPoints.length > 0) {
         this.renderGraph(this.dataPoints);
       }
     },

     toggleInputMode() {
       this.isTimeInput = !this.isTimeInput; // Переключаем режим ввода
       // Сбрасываем ошибки и данные при переключении
       this.startTime = '';
       this.finishTime = '';
       this.startTimeError = '';
       this.finishTimeError = '';
       this.traceNumber = null;
       this.dataPoints = [];
       this.errorMessage = '';
     }
   }
};
</script>

<style scoped>
input {
  width: 200px;
}
</style>