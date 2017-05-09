var subjects = null;
var groups = null;
var batches = null;


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
    rawHTML = "<tr><th class='resultsTableHeader'>Email</th><th class='resultsTableHeader'>Results</th><th class='resultsTableHeader'>Sent</th><th class='resultsTableHeader dropdown'><div class='dropbtn'>Groups</div><div class='dropdown-content' id='resultsTableGroupSelector'></div></th></tr>";
    table.innerHTML = rawHTML;
    updateGroupVisibilityHTML();
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

    if (!subjects || !groups || !batches)
        return;

    // empty the table
    table = document.getElementById("resultsTable")
    emptyNode(table);
    regenerateTableHeaderRow(table);

    // add the data
    for (batchKey in batches)
    {
        var groupFlags = generateGroupBooleans(batches[batchKey].group_ids);
        var groupHTML  = generateGroupHTML(groupFlags);

        if (groupHTML.active)
        {
            // compute the results!
            numPageHits = batches[batchKey]['results']['1'];
            if (!numPageHits)
                numPageHits = 0;

            resultValue =  ((numPageHits/ batches[batchKey]['results']['0']) * 100).toFixed(2);

            newRow = {};
            newRow['id']       = batches[batchKey].id;
            newRow['subject']  = "<a href=\"viewResultsDetail.py?id=" + batchKey + "\">" + subjects[batches[batchKey].subject_id] + "</a>";
            newRow['groups']   = groupHTML.html;
            newRow['sentTime'] = batches[batchKey].formatted_time;
            newRow['results']  = resultValue + " %";

            insertNewRow(newRow);
        }
    }
}


function getSubjects()
{
    $.getJSON( "getEmailSubjects.py", function( data )
    {
        subjects = {};
        for (var i = 0; i < data.length; i ++)
            subjects[data[i].id] = data[i].subject;

        updateTable();
    });
};


function getGroups()
{
    $.getJSON( "getGroupNames.py", function( data )
    {
        groups = {};
        for (var i = 0; i < data.length; i ++)
        {
            groupObj = {};
            groupObj.groupName = data[i].name;
            groupObj.visible = (data[i].id != 4);

            groups[data[i].id] = groupObj;
        }
        //* create the table with data in it *//
        updateTable();
    });
};


function getBatches()
{
    $.getJSON( "getCampaignResults.py", function( data )
    {
        batches = {};
        for (var i = 0; i < data.length; i ++)
            batches[data[i].id] = data[i];

        updateTable();
    });
};


function insertNewRow(newRow)
{
    var table = document.getElementById("resultsTable");
    var row = table.insertRow(-1);
    row.setAttribute("id", "resultsTableRow" + newRow['id'], 0);

    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var subjectCell = row.insertCell(0);
    var responseCell = row.insertCell(1);
    var sentCell = row.insertCell(2);
    var groupCell = row.insertCell(3);

    // Add some text to the new cells:
    subjectCell.innerHTML = newRow['subject'];
    sentCell.innerHTML = newRow['sentTime'];
    groupCell.innerHTML = newRow['groups'];
    responseCell.innerHTML = newRow['results'];
}


function when_loaded()
{
    getSubjects();
    getGroups();
    getBatches();
}
