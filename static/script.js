let groups = {}
let meta_columns = ["CLUSTER", "FREQUENCY", "GROUP", "N", "LOW", "HIGH", "LOOP", "ORIGINAL_TLV"]
let vector_columns = []



function makeUI(array_of_groups) {
    console.log("makeUI")
    document.getElementById("output").innerHTML = ""
    let all_tables = ""
    array_of_groups.forEach((group) => {

        // console.log(group + "   " + Math.random() )
        // console.log("group=" + group + " meta=" + groups[group].meta.length + " vector=" + groups[group].vector.length ) 

        for (let i = 0; i < groups[group].meta.length; i++) {
            let table = "<table border='0'> <tr>"
            const v = groups[group].vector[i]
            for (let i = 0; i < v.length; i++) {
                let h = 500 * v[i] // array is scaled 1 to 0. css is scale 100 to 0 
                console.log( h + "   " + v[i] )
                const td = `<td valign="bottom" style="width:4px;"><div style="height:${h}px; background-color:orange; color:orange;" ></div></td>`
                table += td
            }
            table += "</tr></table>"
            all_tables += table
        }
    })

 document.getElementById("output").innerHTML = all_tables; 


}


function getSelectedOptions() {
    const selectElement = document.getElementById('groupChoices');
    const selectedGroups = Array.from(selectElement.selectedOptions).map(option => option.value);

    makeUI(selectedGroups)



}

function createSelector() {
    const keys = Object.keys(groups)
    const n = 1 + keys.length;
    let x = `<select size='${n}' multiple  onchange="getSelectedOptions()" id="groupChoices">`
    keys.forEach((key) => {
        x += `<option>${key}</option>`
    })
    x += "</select>"
    document.getElementById("control").innerHTML = x
}

function getCsv() {
    array_meta = [];
    array_vector = [];
    const meta_headers = ["CLUSTER", "FREQUENCY", "GROUP", "N", "LOW", "HIGH", "LOOP", "ORIGINAL_TLV"]
    const vector_headers = []
    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    const url = 'static/cluster.csv';
    xhr.open('GET', url, true);

    xhr.responseType = 'text';
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Split the CSV data into rows
            const rows = xhr.responseText.split('\n');

            // Set up the column names
            const ary = rows[0].split(',');
            ary.forEach((thing) => {
                if (meta_columns.includes(thing)) {
                } else {
                    vector_columns.push(thing)
                }
            })
            groups = {}
            // Parse each row into an array of values
            for (let i = 1; i < rows.length; i++) {
                if (rows[i].length < 200) {
                    // it is empty! ignore it 
                } else {
                    let headers = []
                    let vector = []
                    const values = rows[i].split(',');

                    /// The headers in the csv
                    for (let j = 1; j < values.length; j++) {
                        if (j < meta_columns.length) {
                            headers.push(values[j])
                        } else {
                            vector.push(values[j])
                        }
                    }

                    /// The information in the csv
                    const group_name = headers[3] + "_" + headers[4] // low_high                    
                    if (!groups.hasOwnProperty(group_name)) {
                        groups[group_name] = {
                            "meta": [],
                            "vector": []
                        }
                    }
                    groups[group_name]["meta"].push(headers)
                    groups[group_name]["vector"].push(vector)
                }
            }
            createSelector()
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



getCsv()