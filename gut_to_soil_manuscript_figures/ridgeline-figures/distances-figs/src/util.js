import * as d3 from "d3";

export async function parseData(file) {
  const distances = await d3.json(file);

  let distancesLong = [];
  let comparisons = ["food compost", "soil", "fecal", "bulking material"];
  comparisons.forEach((comp) => {
    distances[comp].forEach((dist) => {
      distancesLong.push({ comparison: comp, distance: dist });
    });
  });
  const data = distancesLong;

  return data;
}

export function kde(kernel, thresholds, data) {
  let estimates = thresholds.map((t) => [
    t,
    d3.mean(data, (d) => kernel(t - d)),
  ]);

  return estimates;
}

export function epanechnikov(bandwidth) {
  return (x) => {
    if (Math.abs((x /= bandwidth)) <= 1) {
      return (0.75 * (1 - x * x)) / bandwidth;
    } else {
      return 0;
    }
  };
}

export function getThresholds(data, numThresholds) {
  const extent = d3.extent(data);
  const niceExtent = d3.nice(...extent, 10);
  const thresholds = d3.ticks(...niceExtent, numThresholds);

  return thresholds;
}

export function getColor(comp, timepoints) {
  let opacity;
  if (timepoints == "start") {
    opacity = "77";
  } else if (timepoints == "end") {
    opacity = "dd";
  }

  let color;
  if (comp == "fecal") {
    color = "8c564b";
  } else if (comp == "soil") {
    color = "000000";
  } else if (comp == "food compost") {
    color = "ff0000";
  } else if (comp == "bulking material") {
    color = "008000";
  }

  return `#${color}${opacity}`;
}

export function calculateDensity(data) {
  const bandwidth = 0.01;
  let thresholds = getThresholds(data, 20);
  let density = kde(epanechnikov(bandwidth), thresholds, data);

  // normalize densities by area
  let area = 0;
  for (let i = 1; i < density.length; i++) {
    let [x0, y0] = density[i - 1];
    let [x1, y1] = density[i];
    area += ((y0 + y1) / 2) * (x1 - x0);
  }
  density = density.map(([x, y]) => [x, y / area]);

  let max = d3.max(density, (d) => d[1]);

  console.log("density is", density, "area is", area, "max is", max);

  return { density, max };
}
