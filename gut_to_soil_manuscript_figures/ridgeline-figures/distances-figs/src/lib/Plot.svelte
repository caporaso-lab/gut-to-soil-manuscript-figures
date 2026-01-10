<script>
    import * as d3 from "d3";
    import { onMount } from "svelte";

    import { parseData, calculateDensity } from "../util.js";

    import AxisBottom from "./AxisBottom.svelte";
    import AxisLeft from "./AxisLeft.svelte";
    import Cloud from "./Cloud.svelte";

    export let filepaths;
    export let leftAxis;
    export let grid;

    let promise = massageData();
    async function massageData() {
        let densities = {
            start: {},
            end: {},
        };

        let startData = await parseData(filepaths.start);
        let endData = await parseData(filepaths.end);
        let data = { start: startData, end: endData };

        for (let direction of ["start", "end"]) {
            for (let sampleType of compScale.domain()) {
                let compData = data[direction]
                    .filter((d) => d.comparison == sampleType)
                    .map((d) => d.distance);

                let { density, max } = calculateDensity(compData);
                densities[direction][sampleType] = density;
            }
        }

        return densities;
    }

    let leftMargin = 10;
    if (leftAxis) {
        leftMargin = 150;
    }

    const dim = {
        width: 600 + leftMargin,
        height: 600,
    };
    const margin = {
        top: 50,
        right: 20,
        bottom: 100,
        left: leftMargin,
    };

    let distScale = d3
        .scaleLinear()
        .domain([0.5, 1])
        .range([margin.left, dim.width - margin.right]);

    let compScale = d3
        .scaleBand()
        .domain(["fecal", "bulking material", "soil", "food compost"])
        .range([dim.height - margin.bottom, margin.top]);

    onMount(() => {
        d3.select(`.bucket-${bucket}`)
            .append("clipPath")
            .attr("id", `clip-${bucket}`)
            .append("rect")
            .attr("x", leftMargin)
            .attr("y", 50)
            .attr("width", dim.width)
            .attr("height", dim.height);
    });

    let bucket = filepaths.bucket;
</script>

<div
    class={`bucket-${bucket}-plot`}
    style="display: {grid ? 'inline-block' : 'block'}"
>
    <svg
        class={`bucket-${bucket}`}
        xmlns="http://www.w3.org/2000/svg"
        style="height: {dim.height}px; width: {dim.width}px;"
    >
        <text
            transform="translate(
                {leftAxis ? dim.width / 2 + 50 : dim.width / 2 - 25}, 20
            )"
        >
            Bucket {bucket}
        </text>

        <AxisBottom {dim} {margin} scale={distScale} />
        {#if leftAxis}
            <AxisLeft {dim} {margin} scale={compScale} />
        {/if}

        {#await promise}
            <p>Loading...</p>
        {:then densities}
            {#each ["start", "end"] as time}
                {#each compScale.domain() as comp}
                    <Cloud
                        density={densities[time][comp]}
                        {comp}
                        {time}
                        {compScale}
                        {distScale}
                        {bucket}
                    />
                {/each}
            {/each}
        {:catch error}
            <p>Error: {error}</p>
        {/await}
    </svg>
</div>

<style>
    svg {
        width: 600px;
        height: 600px;
    }
    text {
        font-size: 20px;
        font-family: sans-serif;
    }
</style>
