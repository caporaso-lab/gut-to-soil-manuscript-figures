<script>
    export let dim;
    export let margin;
    export let scale;

    const ticks = scale.ticks();
</script>

<g>
    <line
        x1={margin.left}
        y1={dim.height - margin.bottom}
        x2={dim.width - margin.right}
        y2={dim.height - margin.bottom}
        stroke="black"
        stroke-width="2"
        stroke-linecap="round"
    />
    {#each ticks as tick, i}
        {#if i == 0}
            <g
                transform="translate(
                    {scale(tick)}, {dim.height - margin.bottom}
                )"
            >
                <text y={20} transform="translate(5, 0)">{tick}</text>
                <line
                    y2="5"
                    stroke="black"
                    stroke-width="2"
                    stroke-linecap="round"
                />
            </g>
        {:else}
            <g
                transform="translate(
                    {scale(tick)}, {dim.height - margin.bottom}
                )"
            >
                <text y={20}>{tick}</text>
                <line
                    y2="5"
                    stroke="black"
                    stroke-width="2"
                    stroke-linecap="round"
                />
            </g>
        {/if}
    {/each}
</g>

<style>
    text {
        text-anchor: middle;
        font-size: 17px;
        font-family: sans-serif;
    }
</style>
