<script>
    import * as d3 from "d3";

    import { getColor } from "../util.js";

    export let density;
    export let comp;
    export let time;
    export let compScale;
    export let distScale;
    export let bucket;

    let direction = -1;
    if (time == "end") {
        direction = 1;
    }
    let padding = 3;
    let halfway = compScale(comp) + compScale.bandwidth() / 2;

    let cloudScale = d3
        .scaleLinear()
        .domain(d3.extent(density.map((d) => d[1])))
        .range([
            halfway + direction * padding,
            halfway +
                (direction * compScale.bandwidth()) / 2 -
                direction * padding,
        ]);

    let area = d3
        .area()
        .x((d) => distScale(d[0]))
        .y0(compScale(comp) + compScale.bandwidth() / 2 + direction * padding)
        .y1((d) => cloudScale(d[1]))
        .curve(d3.curveBasis);

    d3.select(`.bucket-${bucket}`)
        .append("path")
        .datum(density)
        .attr("fill", getColor(comp, time))
        .attr("stroke", "gray")
        .attr("stroke-width", 1.5)
        .attr("d", area)
        .attr("clip-path", `url(#clip-${bucket})`);
</script>
