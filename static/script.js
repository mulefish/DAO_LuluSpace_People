let groups = {}
let meta_columns = ["CLUSTER", "FREQUENCY", "GROUP", "N", "LOW", "HIGH", "LOOP", "ORIGINAL_TLV"]
let vector_columns = []
let colors = ["DarkRed",
    "DarkOrange",
    "DarkGoldenRod",
    "DarkGreen",
    "DarkCyan",
    "DarkSlateBlue",
    "DarkMagenta",
    "DarkViolet",
    "DarkSalmon",
    "DarkSeaGreen",
    "DarkTurquoise",
    "DarkOliveGreen",
    "DarkKhaki",
    "DarkGray",
    "DarkSlateGray",
    "DarkOrchid",
    "DarkCrimson",
    "DarkSlateGrey",
    "DarkBlue",
    "DarkChocolate"]

let backColor = ["LightSlateGray",
    "DarkSlateGray",
    "SteelBlue",
    "DarkOliveGreen",
    "RosyBrown",
    "CadetBlue"]

function makeUI(array_of_groups) {
    document.getElementById("output").innerHTML = ""
    let all_tables = "<table border='0'>"
    array_of_groups.forEach((group, loop) => {
        const clr = colors[loop]
        all_tables += `<tr><td class="small">${group}</td></tr>`
        for (let i = 0; i < groups[group].meta.length; i++) {
            const v = groups[group].vector[i]
            const m = groups[group].meta[i]

            const n_entries = m[0] // number in this group
            if (n_entries == 1) {
                // Ignore 1 offs
            } else {
                const tlv = parseInt(m[6]) // tlv ave of this group

                all_tables += `<tr><td class="small" valign="bottom">${n_entries}</td><td>&nbsp;</td><td class="small" valign="bottom">$${tlv}</td>`
                for (let i = 0; i < v.length; i++) {
                    let h = 300 * v[i] // array is scaled 1 to 0 : Scale up!
                    const td = `<td valign="bottom" style="width:4px;" onmouseover="emit(${i}, ${v[i]})"><div style="height:${h}px; background-color:${clr};" ></div></td>`
                    all_tables += td
                }
                all_tables += "</tr>"
            }
        }
    })
    all_tables += "</table>"
    document.getElementById("output").innerHTML = all_tables;


}
function emit(columnIndex, value) {
    document.getElementById("column").innerHTML = vector_columns[columnIndex]
    document.getElementById("value").innerHTML = value
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
