
// Arrays to store metadata and vectors
let array_meta = [];
let array_vector = [];


function doit() {

    array_meta = [];
    array_vector = [];

    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    // Define the request URL
    const url = 'static/cluster.csv';
    console.info(url)
    // Open a new GET request
    xhr.open('GET', url, true);

    // Set the response type to text
    xhr.responseType = 'text';

    // Define a callback function for when the request is completed
    xhr.onload = function () {
        console.log(xhr.status)
        if (xhr.status === 200) {
            console.log("status ")
            // Split the CSV data into rows
            const rows = xhr.responseText.split('\n');

            // Parse each row into an array of values
            rows.forEach(row => {
                const values = row.split(',');

                // Extract metadata and vector values
                const meta = values.slice(0, 6); // Cluster, X, Y, Frequency, Group, N
                const vector = values.slice(6); // Remaining values

                // Push metadata and vector arrays to respective arrays
                array_meta.push(meta);
                array_vector.push(vector);
            });


            // Log the arrays
            // console.log('Metadata array:', array_meta);
            // console.log('Vector array:', array_vector);
        } else {
            console.error('Request failed. Status:', xhr.status);
        }
    };

    // Define a callback function for handling errors
    xhr.onerror = function () {
        console.error('Request failed. Network error.');
    };

    // Send the request
    xhr.send();

}


function createColorTable(array) {
    let table = "<table border='0'> <tr>"
    
    for ( let i = 0 ; i < array.length; i++) { 
        let h = 10000 * array[i] // array is scaled 1 to 0. css is scale 100 to 0 
     const td = `<td valign="bottom" style="width: 1px;"><div style="height:${h}px; background-color:orange; color:orange;" ></div></td>`
        table += td 
    }
    table += "</tr></table>"
    return table 
}


function pickone() { 
    const table = createColorTable(array_vector[1])
    document.getElementById("output").innerHTML = table
}