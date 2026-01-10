<script>
import domtoimage from 'dom-to-image';


function handleDownload(e) {
    let all = document.querySelector('.container');
    domtoimage.toSvg(all)
        .then(dataUrl => {
            const downloadLink = document.createElement("a");
            downloadLink.href = dataUrl;
            downloadLink.download = "all-buckets.svg";
            downloadLink.click();
        })

}

function handleIndividualDownload(e) {
    for (let i = 0; i < 17; i++) {
        let fig = document.querySelector(`.bucket-${i}-plot`);

        if (fig == null) {
            continue;
        }

        domtoimage.toSvg(fig)
            .then(dataUrl => {
                const downloadLink = document.createElement("a");
                downloadLink.href = dataUrl;
                downloadLink.download = `bucket-${i}.svg`;
                downloadLink.click();
            })
            .catch(error => {
                console.log('error: ', error);
            })
        }
}

let bucket = '';
</script>

<input type="submit" on:click={handleDownload} value="Download" />
<button on:click={handleIndividualDownload}>Download Individual</button>

