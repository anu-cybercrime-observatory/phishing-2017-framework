var groups = null;
var activities = null;


function emptyNode(myNode)
{
    while (myNode.firstChild)
        myNode.removeChild(myNode.firstChild);
}

function updateGroupVisibilityHTML()
{
    var element = document.getElementById("resultsTableGroupSelector");
    emptyNode(element);

    var newDiv;
    for (key in groups)
    {
        newDiv = document.createElement('div');
        newDiv.id = key;
        newDiv.innerHTML = groups[key].groupName;
        newDiv.onclick = function () { toggleGroupVisibility(this); }

        if (groups[key].visible === true)
            newDiv.className = "ddResultsGroupYes";
        else
            newDiv.className = "ddResultsGroupNo";

        element.appendChild(newDiv);
    }
}


function toggleGroupVisibility(object)
{
    groupId = object.id;
    groups[groupId].visible = !groups[groupId].visible;
    updateTable();
}


function regenerateTableHeaderRow(table)
{
    rawHTML = "<tr><th class='resultsTableHeader'>Action</th><th class='resultsTableHeader'>Results</th><th class='resultsTableHeader'>% age</th></tr>";
    table.innerHTML = rawHTML;
//    updateGroupVisibilityHTML();
}


function generateGroupHTML(isOnArray)
{
    var yesHTML = "";
    var noHTML = "";
    var results = {}

    for (key in groups)
    {
        if (groups[key].visible)
        {
            if (isOnArray[key] === true)
                yesHTML += "<div class='resultsGroup resultsGroupYes'>" + groups[key].groupName + "</div>";
            else
                noHTML  += "<div class='resultsGroup resultsGroupNo'>" + groups[key].groupName + "</div>";
        }
    }

    results.html = yesHTML + noHTML;
    results.active = (!(yesHTML === ''));

    return results;
}


function generateGroupBooleans(groupArray)
{
    res = {};
    for (key in groups)
        if (groups[key].visible === true)
            res[key] = false;

    for (key in groupArray)
        if (groups[groupArray[key]].visible === true)
            res[groupArray[key]] = true;

    return res;
}


function updateTable()
{
    // Make certain that data for all parts of the table has been received, before attempting
    // to display the table.

    if (!activities) // || !groups)
        return;

    // empty the table
    table = document.getElementById("resultsTable")
    emptyNode(table);
    regenerateTableHeaderRow(table);

    // add the data
    var emailsSent = 0;
    for (activityKey in activities)
    {
        var total = 0;
        var percentage = 0;

        for (group in activities[activityKey].results)
        {
            total += activities[activityKey].results[group].count;
        }

        if (activityKey === "0")
            emailsSent = total;
        else
            percentage = (total / emailsSent * 100).toFixed(2);

        newRow = {};
        newRow['id'] = activityKey;
        newRow['activity'] = activities[activityKey].activity_type;
        newRow['response'] = "Total: " + total;
        newRow['percentage'] = percentage + " %";

        insertNewRow(newRow);

        for (group in activities[activityKey].results)
        {
            groupD = activities[activityKey].results[group]
            totalSent = activities[0].results[group].count;

            if (activityKey === "0" || totalSent === 0)
                percentage = "-";
            else
                percentage = (groupD.count / totalSent * 100).toFixed(2) + " %";

            newRow = {};
            newRow['id'] = "sub" + groupD.group_id + "dot" + activityKey;
            newRow['parent_id'] = activityKey;
            newRow['response'] = groupD.group_name + ": " + groupD.count;
            newRow['percentage'] = percentage;

            insertNewSubRow(newRow);
        }
    }

    createChart();
}


function insertNewRow(newRow)
{
    var table = document.getElementById("resultsTable");
    var row = table.insertRow(-1);
    row.setAttribute("id", "resultsTableRow" + newRow['id'], 0);
    row.setAttribute("class", "hoverable", 0)
    row.onclick = function () { toggleSubgroupVisibility(this); }

    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var activityCell = row.insertCell(0);
    var responseCell = row.insertCell(1);
    var percentCell = row.insertCell(2);

    // Add some text to the new cells:
    activityCell.innerHTML = newRow['activity'];
    responseCell.innerHTML = newRow['response'];
    percentCell.innerHTML = newRow['percentage'];
}


function insertNewSubRow(newRow)
{
    var table = document.getElementById("resultsTable");
    var row = table.insertRow(-1);
    row.setAttribute("id", "resultsTableRow" + newRow['id'], 0);
    row.setAttribute("class", "resultsGroup resultsTableRow" + newRow['parent_id'], 0);

    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var activityCell = row.insertCell(0);
    var responseCell = row.insertCell(1);
    var percentCell = row.insertCell(2);

    // Add some text to the new cells:
    activityCell.innerHTML = "";
    responseCell.innerHTML = newRow['response'];
    percentCell.innerHTML = newRow['percentage'];

    row.style.display = 'none';
}


function toggleSubgroupVisibility(object)
{
    classId = object.id;
    elements = document.getElementsByClassName(classId);

    if (elements.length === 0)
        return;

    currentValue = elements[0].style.display;
    newValue = (currentValue === "none") ? "table-row" : "none";

    for(var i = 0; i < elements.length; i++)
       elements.item(i).style.display = newValue;
}


function getData()
{
    var table = document.getElementById("resultsTable");
    var batch_id = table.getAttribute("data-id");

    $.getJSON( "getResultsDetail.py", { "id": batch_id }, function( data )
    {
        groups = {};
        activities = {};
        for (var i = 0; i < data.length; i ++)
        {
            activities[data[i].activity_id] = data[i];

            // Not only the activities - iterate over these things, and extract the
            // group names as well, noting that they may not all be represented in this data set.
            for (var j = 0; j < data[i].results.length; j ++)
                groups[data[i].results[j].group_id] = data[i].results[j].group_name;
        }
        updateTable();
    });
}


function rgbSequence(sequenceId, alpha)
{
    var sequences = [
        'rgba(255, 99, 132, ',
        'rgba(255, 99, 132, ',
        'rgba(99, 255, 132, ',
        'rgba(132, 99, 255, '
    ]

    return sequences[sequenceId] + alpha + ")";
}


function createChart()
{
    // Lets create some data structures.
    labels = [];
    for (var i = 0; i < 24; i ++)
        labels[i] = (i * 2) + " - " + ((i + 1) * 2);

    dataSets = [];
    for (activityKey in activities)
    {
        if (activityKey != 0)
        {
            dataSet = {};
            dataSet['label'] = activities[activityKey].activity_type;
            dataSet['backgroundColor'] = rgbSequence(activityKey, 0.2);
            dataSet['borderColor'] = rgbSequence(activityKey, 1);
            dataSet['borderWidth'] = 1;

            dataNumbers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
            for (groupKey in activities[activityKey].results)
                for (var counter = 0; counter < 24; counter ++)
                    dataNumbers[counter] += activities[activityKey].results[groupKey].time_intervals[counter];
            dataSet['data'] = dataNumbers;
            dataSets.push(dataSet);
        }
    }

    var ctx = document.getElementById("timeSeriesChart");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: dataSets
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}

function when_loaded()
{
    getData();
}
