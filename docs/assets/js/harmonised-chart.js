/* Harmonised data chart for the documentation homepage */

(() => {
  const chartContainer = document.querySelector("#harmonised-chart");
  if (!chartContainer) {
    return;
  }

  const dataUrl = chartContainer.dataset.source;
  const measureContainer = document.querySelector("#measure-selector");
  const statusMessage = document.querySelector("#chart-status");

  const defaultColours = [
    "#66c2a5",
    "#fc8d62",
    "#8da0cb",
    "#e78ac3",
    "#a6d854",
    "#ffd92f",
    "#e5c494",
    "#b3b3b3",
    "#a1d99b",
    "#9e9ac8"
  ];

  let chartInstance;
  let harmonisedSeries = [];
  let indicatorLabels = {};

  const labelForIndicator = key => indicatorLabels[key] || key.replace(/_/g, " ");

  const setStatusMessage = message => {
    if (!statusMessage) {
      return;
    }
    const isActive = Boolean(message);
    statusMessage.textContent = message;
    statusMessage.classList.toggle("is-active", isActive);
    statusMessage.setAttribute("aria-hidden", isActive ? "false" : "true");
  };
  setStatusMessage("");

  const createCheckbox = (id, indicatorKey, index, checked = true) => {
    const wrapper = document.createElement("label");
    wrapper.className = "measure-option";
    wrapper.htmlFor = id;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.id = id;
    checkbox.value = indicatorKey;
    checkbox.checked = checked;
    checkbox.dataset.index = index.toString();

    const span = document.createElement("span");
    span.textContent = labelForIndicator(indicatorKey);

    wrapper.appendChild(checkbox);
    wrapper.appendChild(span);

    return wrapper;
  };

  const buildDatasets = selectedMeasures => {
    return selectedMeasures.map((key, idx) => {
      return {
        label: labelForIndicator(key),
        data: harmonisedSeries.map(row => row[key]),
        borderColor: defaultColours[idx % defaultColours.length],
        backgroundColor: defaultColours[idx % defaultColours.length],
        borderWidth: 2,
        pointRadius: 3,
        pointHoverRadius: 4,
        tension: 0.3
      };
    });
  };

  const renderChart = selectedMeasures => {
    const ctx = chartContainer.getContext("2d");
    const labels = harmonisedSeries.map(row => row.year);
    const datasets = buildDatasets(selectedMeasures);

    if (chartInstance) {
      chartInstance.data.labels = labels;
      chartInstance.data.datasets = datasets;
      chartInstance.update();
      return;
    }

    chartInstance = new window.Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Share of adults (%)"
            }
          },
          x: {
            title: {
              display: true,
              text: "FinScope survey year"
            }
          }
        },
        plugins: {
          legend: {
            position: "bottom"
          },
          tooltip: {
            callbacks: {
              label: context => {
                const { dataset, parsed } = context;
                return `${dataset.label}: ${parsed.y}%`;
              }
            }
          }
        }
      }
    });
  };

  const updateSelectedMeasures = () => {
    const selected = Array.from(
      measureContainer.querySelectorAll("input[type='checkbox']:checked")
    ).map(node => node.value);

    renderChart(selected);
    if (selected.length === 0) {
      setStatusMessage("Select at least one measure to display.");
      chartContainer.setAttribute("aria-hidden", "true");
      return;
    }

    setStatusMessage("");
    chartContainer.removeAttribute("aria-hidden");
  };

  const initializeMeasureSelector = measureKeys => {
    measureContainer.innerHTML = "";

    measureKeys.forEach((key, idx) => {
      const checkbox = createCheckbox(`measure-${key}`, key, idx, idx < 2);
      measureContainer.appendChild(checkbox);
    });

    measureContainer.addEventListener("change", updateSelectedMeasures);
    updateSelectedMeasures();
  };

  const hydrateControls = () => {
    if (!Array.isArray(harmonisedSeries) || harmonisedSeries.length === 0) {
      setStatusMessage("No harmonised data available to chart.");
      return;
    }

    const measureKeys = Object.keys(harmonisedSeries[0]).filter(
      key => key !== "year"
    );

    initializeMeasureSelector(measureKeys);
    setStatusMessage("");
  };

  const fetchData = async () => {
    try {
      const response = await fetch(dataUrl);
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const payload = await response.json();

      if (Array.isArray(payload)) {
        harmonisedSeries = payload;
        indicatorLabels = {};
      } else {
        harmonisedSeries = Array.isArray(payload.series) ? payload.series : [];
        indicatorLabels =
          payload.indicator_labels && typeof payload.indicator_labels === "object"
            ? payload.indicator_labels
            : {};
      }

      hydrateControls();
    } catch (error) {
      setStatusMessage("Unable to load chart data.");
      console.error("Harmonised chart error:", error);
    }
  };

  fetchData();
})();
