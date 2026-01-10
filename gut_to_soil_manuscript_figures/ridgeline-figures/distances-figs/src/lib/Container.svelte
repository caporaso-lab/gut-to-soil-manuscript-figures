<script>
    import * as d3 from "d3";

    import Plot from "./Plot.svelte";
    import Download from "./Download.svelte";

    const bucketNums = [...d3.range(1, 8), ...d3.range(9, 17)];
    const beginDir = "data/n3-beginning";
    const endDir = "data/n3-end";

    let filepaths = [];
    for (let bucketNum of bucketNums) {
        let beginFile = `${beginDir}/distances-bucket-${bucketNum}.json`;
        let endFile = `${endDir}/distances-bucket-${bucketNum}.json`;

        filepaths.push({
            bucket: bucketNum,
            start: beginFile,
            end: endFile,
        });
    }

    let grid = true;
</script>

<div class="container">
    {#each filepaths as pair, i}
        {#if grid}
            {#if i % 3 == 0}
                <Plot filepaths={pair} leftAxis={true} {grid} />
            {:else}
                <Plot filepaths={pair} leftAxis={false} {grid} />
            {/if}
        {:else}
            <Plot filepaths={pair} leftAxis={true} {grid} />
        {/if}
    {/each}
</div>
<Download />

<style>
</style>
