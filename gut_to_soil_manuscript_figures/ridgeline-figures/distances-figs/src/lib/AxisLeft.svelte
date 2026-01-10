<script>
    export let dim;
    export let margin;
    export let scale;

    const ticks = scale.domain();
</script>

<g>
    <line
        x1={margin.left}
        y1={margin.top}
        x2={margin.left}
        y2={dim.height - margin.bottom}
        stroke="black"
        stroke-width="2"
        stroke-linecap="round"
    />
    {#each ticks as tick}
        <g transform="translate({margin.left - 5}, {scale(tick)})">
            <text transform="translate(0, {scale.bandwidth() / 2})">
                {tick}
            </text>
            <line
                x2="5"
                stroke="black"
                stroke-width="2"
                stroke-linecap="round"
            />
        </g>
    {/each}
</g>

<style>
    text {
        text-anchor: end;
        font-size: 17px;
        font-family: sans-serif;
    }
</style>
