---
layout: default
title: Home
nav_order: 1
description: "Overview of the Harmonise FinScope documentation."
permalink: /
---

# FinScope Harmonisation
{: .fs-9 }

Consistent, researcher-friendly indicators assembled from the FinScope Consumer South Africa surveys.
{: .fs-6 .fw-300 }

Start with the setup guide, follow the end-to-end workflow, and lean on the mapping notes as you extend the project to new waves.

## Why harmonise?
- Compare financial inclusion trends across survey years with shared definitions.
- Preserve the detailed question wording that underpins each indicator.
- Produce wide and long analytical tables for downstream econometric work.

## Jump in
- [Get set up](getting-started){: .btn .btn-primary } Configure Python, environment variables, and local data paths.
- [Run the workflow](workflow){: .btn} Clean, harmonise, and summarise survey waves with the provided make targets.
- [Consult the notes](harmonisation_notes){: .btn} Track questionnaire quirks and year-specific adjustments.

## Documentation map
- **Getting started** covers prerequisites, installation, and environment configuration.
- **Workflow** walks through the typical commands for cleaning, harmonising, and summarising outputs.
- **Mappings & outputs** explains the CSV lookup tables, generated datasets, and directory layout.
- **Harmonisation notes** capture contextual insights for each survey year.

Looking to contribute? Open the mappings in your preferred spreadsheet editor, update the harmonised indicators, and document rationale as you go.

## Explore the data

Pick one or more harmonised measures to see how they evolve through time. Values are expressed as the share of adults reporting the indicator in each survey year.

<div class="chart-panel">
  <div class="chart-controls">
    <strong class="chart-controls__title">Measures</strong>
    <div id="measure-selector" class="chart-controls__options"></div>
  </div>
  <div class="chart-visual">
    <p id="chart-status" class="chart-status" role="status"></p>
    <canvas id="harmonised-chart" data-source="{{ '/assets/data/harmonised-summary.json' | relative_url }}"></canvas>
  </div>
</div>

<style>
.chart-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}
.chart-controls {
  border: 1px solid var(--nav-border-color);
  border-radius: 0.375rem;
  padding: 1rem;
  width: 100%;
}
.chart-controls__title {
  display: block;
  margin-bottom: 0.75rem;
}
.chart-controls__options {
  display: grid;
  gap: 0.5rem;
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
}
.measure-option {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.9rem;
}
.measure-option input[type="checkbox"] {
  margin-top: 0.15rem;
}
.chart-visual {
  position: relative;
  border: 1px solid var(--nav-border-color);
  border-radius: 0.375rem;
  padding: 1rem;
  min-height: 20rem;
  height: clamp(20rem, 50vw, 28rem);
}
.chart-status {
  position: absolute;
  top: 1rem;
  left: 1rem;
  margin: 0;
  font-size: 0.9rem;
  color: var(--color-text-muted);
  background-color: var(--body-background-color, #fff);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
  pointer-events: none;
}
.chart-status.is-active {
  opacity: 1;
}
#harmonised-chart {
  width: 100% !important;
  height: 100% !important;
}
</style>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<script src="{{ '/assets/js/harmonised-chart.js' | relative_url }}"></script>
