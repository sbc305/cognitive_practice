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

      <div>
        <label for="fileName">Название файла:</label>
        <input type="text" v-model="fileName" placeholder="Введите название файла" />
        <div v-if="fileNameError" style="color: red;">{{ fileNameError }}</div>
      </div>

      <button @click="plotGraphByTime">Построить график</button>
    </div>

    <div v-else>
      <h2>Выберите номер трассы для построения графика</h2>
      <input type="number" v-model="traceNumber" placeholder="Введите номер трассы" min="0" max="11" />
      <div>
        <label for="fileName">Название файла:</label>
        <input type="text" v-model="fileName" placeholder="Введите название файла" />
        <div v-if="fileNameError" style="color: red;">{{ fileNameError }}</div>
      </div>
      <button @click="plotGraphById">Построить график</button>
    </div>

    <!-- Сообщение о загрузке -->
    <div v-if="isLoading" style="color: blue;">Обработка данных, пожалуйста подождите...</div>

    <!-- Отображаем график -->
    <div id="myDiv" style="width: 100%; height: 400px;" v-if="isGraphView"></div>

    <!-- Выбор параметров для расчета и лимита -->
    <div v-if="isGraphView && graphBuilt">
      <h3>Выберите параметры для расчета:</h3>
      <label><input type="checkbox" v-model="selectedParams.cte"> cte</label><br />
      <label><input type="checkbox" v-model="selectedParams.yaw_rate"> yaw_rate</label><br />
      <label><input type="checkbox" v-model="selectedParams.steer_fb"> steer_fb</label><br />
      <h4>Выберите лимит:</h4>
      <input type="number" v-model.number="limitValue" min="-1" placeholder="Введите лимит"/>
      <!-- Сообщение о расчете -->
      <button @click="calculateAlgo">Сделать расчет</button>

      <!-- Сообщение об ошибке -->
      <div id="errorMessage" style="color: red;">{{ errorMessage }}</div>

      <!-- Сообщение о характере виляний -->
      <div v-if="vibrationMessage" style="color: green; margin-top: 10px;">
        Характер виляний: {{ vibrationMessage }}
      </div>

      <!-- Сообщение о загрузке при расчете -->
      <div v-if="isCalculating" style="color: blue;">Идет подсчет, подождите...</div>
    </div>

    <!-- Кнопка для переключения между графиком и данными -->
    <button @click="toggleView">{{ isGraphView ? 'Показать данные' : 'Показать график' }}</button>

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
      isGraphView: true,
      isTimeInput: true,
      traceNumber: null,
      fileName: '',
      fileNameError: '',
      dataPoints: [],
      isLoading: false,
      graphTitle: '',
      
      selectedParams: {
        cte: false,
        yaw_rate: false,
        steer_fb: false
      },
      
      limitValue: 0,
      
      graphBuilt: false,
      
      // Новое свойство для хранения сообщения о вилянии, для хранения данных мод, для хранения названий столбцов и для отображения сообщения о расчете
      vibrationMessage: '',
      
      etalonModesData: {},

      columns: [],

      isCalculating: false 
    };
  },
  
  methods: {
    validateFileNumber() {
       return '';
    },
    
    validateTimestamp(timestamp) {
       const datePattern = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;
       return datePattern.test(timestamp) ? '' : 'Неверный формат времени. Используйте YYYY-MM-DD HH:mm:ss.';
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
      
      this.fileNameError = this.validateFileNumber();
    },
    
    plotGraphByTime() {
       const url = 'http://localhost:8000/data/';
       
       this.errorMessage = '';
       this.validateTimes();

       if (this.startTimeError || this.finishTimeError || this.fileNameError) {
         return;
       }

       const user = {
         "start_time": this.startTime,
         "finish_time": this.finishTime,
         "device_id": this.fileName
       };

       this.isLoading = true;

       fetch(url, {
         method: "POST",
         headers: {
           "Content-type": "application/json; charset=UTF-8",
         },
         body: JSON.stringify(user)
       })
       .then(response => {
         if (!response.ok) { 
           return response.json().then(err => { 
             throw new Error(err.message || 'Ошибка при обработке запроса.');
           });
         }
         
         return response.json();
       })
       .then(data => {
         this.dataPoints = data;
         this.isGraphView = true;
         this.graphTitle = `График с ${this.startTime} по ${this.finishTime}`;
         this.renderGraph(data);
         this.graphBuilt = true;
       })
       .catch(error => {
         console.error('Ошибка при получении JSON:', error);
         this.errorMessage = error.message;
       })
       .finally(() => {
         this.isLoading = false;
       });
     },
     
     plotGraphById() {
       const url = 'http://localhost:8000/data/';
       
       if (this.traceNumber < 0 || this.traceNumber > 11) {
         this.errorMessage = 'Такой трассы нет. Введите номер от 0 до 11.';
         this.dataPoints = [];
         return;
       }

       const user = { 
         "file_id": this.traceNumber,
         "device_id": this.fileName
       };

       this.fileNameError = this.validateFileNumber();
       
       if (this.fileNameError) {
           return;
        }

        this.isLoading = true;

        fetch(url, {
          method: "POST",
          headers: {
            "Content-type": "application/json; charset=UTF-8",
          },
          body: JSON.stringify(user)
        })
        .then(response => {
          if (!response.ok) { 
            return response.json().then(err => { 
              throw new Error(err.message || 'Ошибка при обработке запроса.');
            });
          }
          
          return response.json();
        })
        .then(data => {
          this.dataPoints = data;
          this.isGraphView = true; 
          this.graphTitle = `График ID ${this.traceNumber}`;
          this.renderGraph(data);
          this.graphBuilt = true;
        })
        .catch(error => {
          console.error('Ошибка при получении JSON:', error);
          this.errorMessage = error.message;
        })
        .finally(() => {
          this.isLoading = false;
        });
     },
     
     renderGraph(data) {
       // Проверяем наличие данных перед построением графика
       if (!data || data.length === 0) return;

       // Используем nextTick для гарантии обновления DOM
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
         title: this.graphTitle,
         xaxis: { title: 'X координаты' },
         yaxis: { title: 'Y координаты' }
       };

       const graphDiv = document.getElementById('myDiv');
       if (graphDiv) {
         Plotly.newPlot(graphDiv, [trace], layout);
       } else {
         console.error("Элемент с id 'myDiv' не найден.");
       }
     },
     
     calculateAlgo() {
       const url = 'http://localhost:8000/algo/';
       
       const valuedBy = [];
       if (this.selectedParams.cte) valuedBy.push("cte");
       if (this.selectedParams.yaw_rate) valuedBy.push("yaw_rate");
       if (this.selectedParams.steer_fb) valuedBy.push("steer_fb");

       if (valuedBy.length === 0) {
           this.errorMessage = 'Не выбраны параметры для расчета.';
           return;
       }

       if (this.limitValue <= 0) { 
           return; 
       }

       const userData = {};
       userData.source_info = {};

       if (this.isTimeInput) { // Если запрос по времени
           userData.source_info.device_id = this.fileName; // Указываем device_id
           userData.source_info.start_time = this.startTime; // Начальное время
           userData.source_info.finish_time = this.finishTime; // Конечное время
       } else { // Если запрос по ID трассы
           userData.source_info.device_id = this.fileName; // Указываем device_id
           userData.source_info.file_id = this.traceNumber; // Номер трассы
       }

       userData.algo_id = 1; // Фиксированное значение алгоритма
       userData.valued_by = valuedBy; // Параметры, выбранные пользователем
       userData.limit = this.limitValue; // Лимит

       console.log('Отправляемые данные в POST-запросе:', JSON.stringify(userData)); 

       // Устанавливаем состояние загрузки во время расчета
       this.isCalculating = true;

       fetch(url, {
           method:"POST",
           headers:{
               "Content-Type":"application/json"
           },
           body : JSON.stringify(userData)
       })
       .then(response => {
           if (!response.ok) {
               throw new Error('Ошибка при обработке запроса.');
           }
           return response.json();
       })
       .then(data => {
           console.log('Результат расчета:', data);
           
           // Сохраняем названия столбцов из ответа
           this.columns = data.columns || []; 

           // Проверяем наличие поля "answer"
           if (data.answer) {
               // Устанавливаем сообщение о вилянии
               this.vibrationMessage = data.answer;

               // Рисуем график с трассами из etalon_modes
               if (data.etalon_modes && data.etalon_modes.cte) {

                   const tracesToPlot = data.etalon_modes.cte.map((track, index) => ({
                       x: track.map((_, i) => i), // Генерируем X координаты как индексы точек
                       y: track, // Y координаты из данных трассы
                       mode: 'lines+markers',
                       type: 'scatter',
                       name: `мода ${index + 1}`, 
                   }));

                   const layoutTracks = { 
                       title: 'График мод', 
                       xaxis: { title:'номер измерения' }, 
                       yaxis: { title:`${this.columns.join(', ')}` }
                   };
                   Plotly.newPlot('myDiv', tracesToPlot, layoutTracks); // Рисуем график с несколькими трассами
               }
           } else {
               alert('Ответ не содержит параметра "answer".');
               this.vibrationMessage = ''; // Сбрасываем сообщение, если его нет
           }
           
           console.log('Столбцы:', data.columns);
           console.log('Экстремумы:', data.extremes);
           console.log('Эталонные экстремумы:', data.etalon_extremes);
           
       })
       .catch(error => console.error('Ошибка при отправке данных:', error))
       .finally(() => {
           // Сбрасываем состояние загрузки после завершения расчета
           this.isCalculating = false;
       });
     },

     toggleView() {
       // Переключаем режим отображения
       this.isGraphView = !this.isGraphView;

     },
     
     toggleInputMode() {
       // Переключаем режим ввода
       this.isTimeInput = !this.isTimeInput; 
       
     }
   }
};
</script>

<style scoped>
input[type='number'] { width: 200px; }
input[type='checkbox'] { margin-right: 10px; }
</style>
