var elementId = "d3-graph"

// dynamically set height and width to that of parent element
var parentElement = getParentElement();
var w = parentElement.offsetWidth;
var h = parentElement.offsetHeight;
console.log(w, h);

// 获取betweenness centrality值的范围，后序需要高亮处理
var bc_min = 0;
var bc_max = 0.1;

// D3 variables
var rootSelection;
var svgSelection;
var gSelection;
var nodeSelection;
var linkSelection;
var circleSelection;
var textSelection;
var force;
// 记录这个graph
var Ggraph;

var color = d3.scale.linear()
    .domain([minScore, (minScore + maxScore) / 2, maxScore])
    .range(["lime", "yellow", "red"]);

function getParentElement() {
    return document.getElementById(elementId).parentElement
}

rootSelection = d3.select("#" + elementId);
svgSelection = rootSelection.append("svg")
svgSelection.attr("class", "graph-svg");
gSelection = svgSelection.append("g");
d3.json("/data", function (error, graph) {
    if (error) throw error;
    console.log(graph);
    Ggraph = graph.data;
    console.log(graph);
    update(Ggraph.links, Ggraph.nodes);
    applyGlow();
});
