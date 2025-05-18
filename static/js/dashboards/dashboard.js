// -------------------------------------------------------------------------------------------------------------------------------------------
// Dashboard 1 : Chart Init Js
// -------------------------------------------------------------------------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function () {

  //****************************
  // Theme Onload Toast
  //****************************
  window.addEventListener("load", () => {
    let myAlert = document.querySelectorAll('.toast')[0];
    if (myAlert) {
      let bsAlert = new bootstrap.Toast(myAlert);
      bsAlert.show();
    }
  })

  // -----------------------------------------------------------------------
  // Recent orders
  // -----------------------------------------------------------------------

  var options_sales_overview = {
    series: [
      {
        name: "Ample Admin",
        data: [355, 390, 300, 350, 390, 180],
      },
      {
        name: "Pixel Admin",
        data: [280, 250, 325, 215, 250, 310],
      },
    ],
    chart: {
      type: "bar",
      height: 265,
      toolbar: {
        show: false,
      },
      foreColor: "#adb0bb",
      fontFamily: "inherit",
      sparkline: {
        enabled: false,
      },
    },
    grid: {
      show: false,
      borderColor: "transparent",
      padding: {
        left: 0,
        right: 0,
        bottom: 0,
      },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "42%",
        endingShape: "rounded",
        borderRadius: 5,
      },
    },
    colors: ["var(--bs-primary)", "var(--bs-secondary)"],
    dataLabels: {
      enabled: false,
    },
    yaxis: {
      show: true,
      min: 100,
      max: 400,
      tickAmount: 3,
    },
    stroke: {
      show: true,
      width: 5,
      lineCap: "butt",
      colors: ["transparent"],
    },
    xaxis: {
      type: "category",
      categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
      axisBorder: {
        show: false,
      },
    },
    fill: {
      opacity: 1,
    },
    tooltip: {
      theme: "dark",
    },
    legend: {
      show: false,
    },
  };

  var chart_column_basic = new ApexCharts(
    document.querySelector("#sales-overview"),
    options_sales_overview
  );
  chart_column_basic.render();

  // -----------------------------------------------------------------------
  // Monthly Sales
  // -----------------------------------------------------------------------
  var option_monthly_sales = {
    series: [
      {
        colors: ["var(--bs-primary)"],
        name: "Monthly Sales",
        data: [35, 60, 30, 55, 40],
      },
    ],

    colors: ["var(--bs-primary)"],
    fill: {
      type: "gradient",
      colors: "var(--bs-primary)",
      gradient: {
        opacityFrom: 0.1,
        opacityTo: 0.01,
        stops: [100],
      },
    },
    chart: {
      type: "area",
      height: 75,
      toolbar: {
        show: false,
      },
      foreColor: "#adb0bb",
      fontFamily: "inherit",
      sparkline: {
        enabled: true,
      },
    },
    dataLabels: {
      enabled: false,
    },
    markers: {
      size: 0,
    },
    legend: {
      show: false,
    },
    stroke: {
      show: true,
      width: 2,
      curve: "smooth",
    },
    tooltip: {
      theme: "dark",
    },
  };

  var chart_monthly_sales = new ApexCharts(
    document.querySelector("#monthly-sales"),
    option_monthly_sales
  );
  chart_monthly_sales.render();

  // -----------------------------------------------------------------------
  // Total Sales
  // -----------------------------------------------------------------------
  var option_total_sales = {
    series: [25, 25, 25, 25],
    labels: ["2024", "2023", "2022", "2021"],
    chart: {
      height: 280,
      type: "donut",
      foreColor: "#adb0bb",
      fontFamily: "inherit",
    },
    colors: [
      "var(--bs-primary)",
      "var(--bs-info)",
      "var(--bs-warning)",
      "var(--bs-primary-bg-subtle)",
    ],
    dataLabels: {
      enabled: false,
    },
    legend: {
      show: false,
    },
    grid: {
      show: false,
      borderColor: "transparent",
      padding: {
        top: 0,
        right: 0,
      },
    },
    stroke: {
      colors: ["transparent"],
    },
    plotOptions: {
      pie: {
        donut: {
          size: "78%",
          background: "transparent",
          labels: {
            show: false,
            name: {
              show: true,
              fontSize: "18px",
              color: undefined,
              offsetY: -10,
            },
            value: {
              show: false,
              color: "#98aab4",
            },
            total: {
              show: false,
              label: "Our Visitors",
              color: "#98aab4",
            },
          },
        },
      },
    },
    tooltip: {
      theme: "dark",
      fillSeriesColor: false,
    },
  };

  var chart_total_sales = new ApexCharts(
    document.querySelector("#total-sales"),
    option_total_sales
  );
  chart_total_sales.render();

  // --------------------------------
  // Weekly Stats
  // --------------------------------

  var weekly_stats_options = {
    series: [
      {
        colors: ["var(--bs-primary)"],
        name: "Weekly Stats",
        data: [40, 60, 50, 65],
      },
    ],
    chart: {
      height: 165,
      type: "area",
      foreColor: "#adb0bb",
      fontFamily: "inherit",
      toolbar: {
        show: false,
      },
      sparkline: {
        enabled: true,
      },
    },
    colors: ["var(--bs-primary)"],
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "smooth",
      width: 2,
    },
    fill: {
      type: "gradient",
      colors: "var(--bs-primary)",
      gradient: {
        opacityFrom: 0.1,
        opacityTo: 0.01,
        stops: [100],
      },
    },
    tooltip: {
      theme: "dark",
    },
    grid: {
      show: false,
      padding: {
        right: 0,
        left: 0,
      },
    },
  };

  var weekly_stats_chart = new ApexCharts(
    document.querySelector("#weekly-stats"),
    weekly_stats_options
  );
  weekly_stats_chart.render();
});
