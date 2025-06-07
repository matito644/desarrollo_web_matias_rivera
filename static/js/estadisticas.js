// Función para cargar el gráfico de actividades por día
function loadChartPorDia() {
  fetch("/api/estadisticas/por-dia")
    .then((response) => response.json())
    .then((data) => {
      const chartData = data.map((item) => [
        new Date(item.dia).getTime(),
        item.cantidad,
      ]);

      Highcharts.chart("chart-por-dia", {
        chart: {
          type: "line",
        },
        title: {
          text: null,
        },
        xAxis: {
          type: "datetime",
          title: {
            text: "Días",
          },
        },
        yAxis: {
          title: {
            text: "Cantidad de Actividades",
          },
          min: 0,
        },
        series: [
          {
            name: "Actividades",
            data: chartData,
            color: "#007bff",
          },
        ],
        legend: {
          enabled: false,
        },
      });
    })
    .catch((error) => {
      console.error("Error cargando gráfico por día:", error);
      document.getElementById("chart-por-dia").innerHTML =
        '<div class="loading">Error al cargar el gráfico</div>';
    });
}

// Función para cargar el gráfico de actividades por tema
function loadChartPorTema() {
  fetch("/api/estadisticas/por-tema")
    .then((response) => response.json())
    .then((data) => {
      const chartData = data.map((item) => ({
        name: item.tema,
        y: item.cantidad,
      }));

      Highcharts.chart("chart-por-tema", {
        chart: {
          type: "pie",
        },
        title: {
          text: null,
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: "pointer",
            dataLabels: {
              enabled: true,
              format: "<b>{point.name}</b>: {point.percentage:.1f}%",
            },
            showInLegend: true,
          },
        },
        series: [
          {
            name: "Actividades",
            data: chartData,
          },
        ],
      });
    })
    .catch((error) => {
      console.error("Error cargando gráfico por tema:", error);
      document.getElementById("chart-por-tema").innerHTML =
        '<div class="loading">Error al cargar el gráfico</div>';
    });
}

// Función para cargar el gráfico de actividades por mes y horario
function loadChartPorMesHorario() {
  fetch("/api/estadisticas/por-mes-horario")
    .then((response) => response.json())
    .then((data) => {
      const meses = data.map((item) => item.mes);
      const mañanaData = data.map((item) => item.mañana);
      const tardeData = data.map((item) => item.tarde);
      const nocheData = data.map((item) => item.noche);

      Highcharts.chart("chart-por-mes-horario", {
        chart: {
          type: "column",
        },
        title: {
          text: null,
        },
        xAxis: {
          categories: meses,
          title: {
            text: "Meses",
          },
        },
        yAxis: {
          title: {
            text: "Cantidad de Actividades",
          },
          min: 0,
        },
        plotOptions: {
          column: {
            pointPadding: 0.2,
            borderWidth: 0,
          },
        },
        series: [
          {
            name: "Mañana (6:00-11:59)",
            data: mañanaData,
            color: "#ffc107",
          },
          {
            name: "Tarde (12:00-17:59)",
            data: tardeData,
            color: "#28a745",
          },
          {
            name: "Noche (18:00-23:59)",
            data: nocheData,
            color: "#6f42c1",
          },
        ],
      });
    })
    .catch((error) => {
      console.error("Error cargando gráfico por mes y horario:", error);
      document.getElementById("chart-por-mes-horario").innerHTML =
        '<div class="loading">Error al cargar el gráfico</div>';
    });
}

// Cargamos todos los gráficos cuando la página esté lista
document.addEventListener("DOMContentLoaded", function () {
  loadChartPorDia();
  loadChartPorTema();
  loadChartPorMesHorario();
});
