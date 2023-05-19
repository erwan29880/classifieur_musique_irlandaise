var data;
var myChart1;
var myChart2;
var myChart3;
var canvas1 = document.getElementById("myChart1");
var ctx1 = canvas1.getContext('2d');
var canvas2 = document.getElementById("myChart2");
var ctx2 = canvas2.getContext('2d');
var canvas3 = document.getElementById("myChart3");
var ctx3 = canvas3.getContext('2d');


document.getElementById("histo").onchange = function(){
    historique(this.value);
};


// effacer le canvas et recréer un graphe
function genNewGraph(){
    ctx1.clearRect(0, 0, canvas1.width, canvas1.height);
    ctx2.clearRect(0, 0, canvas2.width, canvas2.height);
    ctx3.clearRect(0, 0, canvas3.width, canvas3.height);
    myChart1.destroy();
    myChart2.destroy();
    myChart3.destroy(); 
    
    myChart1 = new Chart(ctx1, genLoss(data));
    myChart2 = new Chart(ctx2, genPrecision(data));
    myChart3 = new Chart(ctx3, genRecall(data));
}



async function historique(newFile){

    const histoFile = "1680246032"
    const url = "/1431766f-b5ce-4603-9e17-1de15d0e6c81";
    
    await fetch(url,
      {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
      body: JSON.stringify({jsonFile: newFile})
      })
      .then((prom) => prom.json())
      .then(myVar => {
            data = myVar;
            document.getElementById("titre").innerHTML = data["title"];
            genNewGraph();
      }) 
}


async function onloadGet(){
    const url = "7eb9e62c-f64c-11ed-b67e-0242ac120002";
    await fetch(url)
    .then((prom) => prom.json())
    .then(myJson => {
        data = myJson;
        myChart1 = new Chart(ctx1, genLoss(data));
        myChart2 = new Chart(ctx2, genPrecision(data));
        myChart3 = new Chart(ctx3, genRecall(data));
        document.getElementById("titre").innerHTML = data["title"];
    })
}

onloadGet();