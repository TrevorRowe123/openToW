let conf = {
    "serverAddress": "localhost:5000", //Change this to match the address of your OpenToW server
    "refreshInterval": 10000, //Number of miliseconds between map refreshes
    "layoutseed": 805525 //Seed for map layout generation
}

var node_list = [];
var edge_list = [];
var edges = new vis.DataSet(edge_list);
var nodes = new vis.DataSet(node_list);
var container = document.getElementById('mynetwork');
var data = {
    nodes: nodes,
    edges: edges
};
var options = {
    "layout":{"randomSeed": conf.layoutseed}
};
var network = new vis.Network(container, data, {});
network.setOptions(options)

function get_network_map(){
    node_list = [];
    edge_list = [];

    var fac_request = new XMLHttpRequest();
    fac_request.open('GET', `http://${conf.serverAddress}/faction/all`, false);
    fac_request.send(null);
    var fac_response = JSON.parse(fac_request.responseText);
    document.getElementById("redwins").innerHTML = "Red Wins: " + fac_response.Red.wins;
    document.getElementById("bluewins").innerHTML = "Blue Wins: " + fac_response.Blue.wins;

    // create an array with nodes
    var sect_request = new XMLHttpRequest();
    sect_request.open('GET', `http://${conf.serverAddress}/sector/all`, false);
    sect_request.send(null);
    var response_list = JSON.parse(sect_request.responseText);
    for(var i = 0; i < response_list.length; i++){
        node_list.push(
            {
                "id": response_list[i].id,
                "color": response_list[i].owner,
                "physics": false
            }
        );
        if(response_list[i].active){
            node_list[i].shadow = {"enabled": true, "color": response_list[i].owner, "size": 20};
            node_list[i].color = "Purple";
        }
    }


    // create an array with edges
    var border_request = new XMLHttpRequest();
    border_request.open('GET', `http://${conf.serverAddress}/border`, false);
    border_request.send(null);
    edge_response_list = JSON.parse(border_request.responseText);
    for(var i = 0; i < edge_response_list.length; i++){
        edge_list.push(
            {
                "from": edge_response_list[i].from,
                "to": edge_response_list[i].to,
                "color":{"inherit":"both"},
                "smooth":{"enabled":false}
            }
        );
    }
    edges = new vis.DataSet(edge_list);
    nodes = new vis.DataSet(node_list);
    data = {
        nodes: nodes,
        edges: edges
    };
    network.setData(data);
}

get_network_map();
setInterval(get_network_map, conf.refreshInterval);
