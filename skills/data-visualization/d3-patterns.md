# D3.js Patterns Reference

Extended patterns for D3.js visualizations. Load only when building complex interactive graphics.

## Force-Directed Network

```javascript
function drawNetwork(nodes, links, svgElement) {
  const svg = d3.select(svgElement);
  svg.selectAll("*").remove();

  const width = 800, height = 600;

  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2));

  const link = svg.append("g")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6);

  const node = svg.append("g")
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", 8)
    .attr("fill", d => colorScale(d.group))
    .call(drag(simulation));

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
  });
}

function drag(simulation) {
  return d3.drag()
    .on("start", (event, d) => {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    })
    .on("drag", (event, d) => {
      d.fx = event.x;
      d.fy = event.y;
    })
    .on("end", (event, d) => {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    });
}
```

## Zoomable Treemap

```javascript
function drawTreemap(data, svgElement) {
  const svg = d3.select(svgElement);
  const width = 800, height = 600;

  const root = d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value);

  d3.treemap()
    .size([width, height])
    .padding(1)(root);

  const cell = svg.selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr("transform", d => `translate(${d.x0},${d.y0})`);

  cell.append("rect")
    .attr("width", d => d.x1 - d.x0)
    .attr("height", d => d.y1 - d.y0)
    .attr("fill", d => colorScale(d.parent.data.name));

  cell.append("text")
    .attr("x", 4)
    .attr("y", 14)
    .text(d => d.data.name)
    .attr("font-size", "11px")
    .attr("fill", "white");
}
```

## Brush + Zoom

```javascript
function setupBrushZoom(svg, xScale, yScale, updateFn) {
  const brush = d3.brush()
    .extent([[0, 0], [width, height]])
    .on("end", brushed);

  svg.append("g")
    .attr("class", "brush")
    .call(brush);

  function brushed(event) {
    if (!event.selection) return;
    const [[x0, y0], [x1, y1]] = event.selection;

    xScale.domain([xScale.invert(x0), xScale.invert(x1)]);
    yScale.domain([yScale.invert(y1), yScale.invert(y0)]);

    svg.select(".brush").call(brush.move, null);
    updateFn();
  }
}
```

## Geographic Map

```javascript
async function drawMap(svgElement, geoJsonUrl) {
  const svg = d3.select(svgElement);
  const width = 800, height = 600;

  const projection = d3.geoMercator()
    .fitSize([width, height], await d3.json(geoJsonUrl));

  const path = d3.geoPath().projection(projection);

  const geojson = await d3.json(geoJsonUrl);

  svg.selectAll("path")
    .data(geojson.features)
    .join("path")
    .attr("d", path)
    .attr("fill", d => colorScale(d.properties.value))
    .attr("stroke", "#fff")
    .attr("stroke-width", 0.5);
}
```

## Chord Diagram

```javascript
function drawChord(matrix, names, svgElement) {
  const svg = d3.select(svgElement);
  const width = 600, height = 600;
  const innerRadius = Math.min(width, height) * 0.3;
  const outerRadius = innerRadius + 20;

  const chord = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .radius(innerRadius);

  const chords = chord(matrix);

  const g = svg.append("g")
    .attr("transform", `translate(${width/2},${height/2})`);

  g.selectAll("path.arc")
    .data(chords.groups)
    .join("path")
    .attr("class", "arc")
    .attr("d", arc)
    .attr("fill", d => colorScale(names[d.index]));

  g.selectAll("path.ribbon")
    .data(chords)
    .join("path")
    .attr("class", "ribbon")
    .attr("d", ribbon)
    .attr("fill", d => colorScale(names[d.source.index]))
    .attr("opacity", 0.7);
}
```

## Tooltip Pattern

```javascript
// Create tooltip div (once)
const tooltip = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("position", "absolute")
  .style("visibility", "hidden")
  .style("background", "#fff")
  .style("border", "1px solid #ddd")
  .style("padding", "8px")
  .style("border-radius", "4px")
  .style("font-size", "12px");

// Attach to elements
selection
  .on("mouseover", (event, d) => {
    tooltip
      .style("visibility", "visible")
      .html(`<strong>${d.name}</strong><br/>Value: ${d.value}`);
  })
  .on("mousemove", (event) => {
    tooltip
      .style("top", (event.pageY - 10) + "px")
      .style("left", (event.pageX + 10) + "px");
  })
  .on("mouseout", () => {
    tooltip.style("visibility", "hidden");
  });
```

## Responsive Container

```javascript
function makeResponsive(containerId, drawFn, data) {
  const container = document.getElementById(containerId);
  const svg = d3.select(container).append("svg");

  function resize() {
    const { width, height } = container.getBoundingClientRect();
    svg.attr("width", width).attr("height", height);
    svg.selectAll("*").remove();
    drawFn(svg, data, width, height);
  }

  resize();
  new ResizeObserver(resize).observe(container);
}
```

## Animation Patterns

```javascript
// Staggered entrance
selection
  .attr("opacity", 0)
  .attr("y", height)
  .transition()
  .delay((d, i) => i * 50)
  .duration(500)
  .attr("opacity", 1)
  .attr("y", d => yScale(d.value));

// Morphing between states
selection
  .transition()
  .duration(750)
  .ease(d3.easeCubicInOut)
  .attrTween("d", function(d) {
    const previous = d3.select(this).attr("d");
    const current = pathGenerator(d);
    return d3.interpolatePath(previous, current);
  });
```
