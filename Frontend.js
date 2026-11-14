WCinput = 0;
ECinput = 0;




function ViewTeamsRedirect()// In the event that the user wants to return to the index page
{
    window.location.href = "Teams.html"
}
function ViewStatComparisonRedirect()// In the event that the user wants to return to the index page
{
    window.location.href = "StatComparison.html"
}
function ShowWCTeamButtonDisplay(tag)
{
    if (WCinput == 0)
    {
      WCinput = 1
     document.getElementById(tag).style.display = "inline"

    }
    else if (WCinput == 1)
      {
          document.getElementById(tag).style.display = "none"
          WCinput = 0         
      }    
}
function ShowECTeamButtonDisplay(tag)
{
    if (ECinput == 0)
    {
      ECinput = 1
     document.getElementById(tag).style.display = "inline"

    }
    else if (ECinput == 1)
      {
          document.getElementById(tag).style.display = "none"
          ECinput = 0         
      }    
}
function DisplayTeamData(tag)
{
  document.getElementById("TeamData").innerHTML = ""
  
  fetch("http://127.0.0.1:5000/api/TeamData?tag=" + tag)
  .then(response => response.json())
  .then(data => {
    document.getElementById("TeamData").innerHTML = data.value

  })
   // document.getElementById("TeamData").innerHTML = document.getElementById(tag).innerHTML
}
function submitButtonPressed()
{ 
 Teams = getTeams()
 Filter = getFilter()

 generateStatistics(Teams,Filter)
 

}
function getTeams()
{
  const Teams = [Team1,Team2,Team3,Team4,Team5]
 
 
 for (let x=0;x<= Teams.length-1; x++)
 {
    if(document.getElementById("Team" + String(x + 1) + "Box").value != "None" || document.getElementById("Team" + String(x + 1) + "Box").value != "None")
    {
        Teams[x]= document.getElementById("Team" + String(x + 1) + "Box").value 
    }
  
   
 }

 

 return Teams
}
function getFilter()
{
  Filter = document.getElementById("FilterBox").value
  return String(Filter)
}
function generateStatistics(Teams,Filter)
{
  temp = []
  info = []
  fetch("http://127.0.0.1:5000/api/StatComparison?teams=" + Teams + "&Filter=" + Filter)
  .then(response => response.json())
  .then(data => {
    info = data.value
    temp = info
    temp = temp.split(",")
    
  document.getElementById("TestBox").innerHTML = temp.toString()
   makeTable(temp)
   
 
  })
  

  
}
function makeTable(TeamData) // at this point youll have a team and their stat
{
  
  ratingpattern = new RegExp('[0-9]+(\\.[0-9]+)?')
  namepattern = new RegExp('\\w[A-z]+\\W{1}[A-z]+')
  const xvalues = []
  const yvalues = []
  for (let x=0;x<=TeamData.length-1; x++)
 {
   xvalues[x] =TeamData[x].match(namepattern)[0]
   yvalues[x]=TeamData[x].match(ratingpattern)[0]
 }

 let dataset1 = {
      labels: xvalues,
            datasets: [{
                label: document.getElementById("FilterBox").value,
                data: yvalues,
                backgroundColor: 'rgba(70, 192, 192, 0.6)',
                borderColor: 'rgba(150, 100, 255, 1)',
                borderWidth: 1
            }]

 }
  let options = {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        };
 let Chart1 = document.getElementById('statchart').getContext('2d'); 
        // Create the bar chart
        let myBarChart = new Chart(Chart1, {
            type: 'bar',
            data: dataset1,
            options: options
        });
}



  
  
  
 
 
  










