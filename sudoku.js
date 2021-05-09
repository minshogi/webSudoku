
function getRandomInt() {
  min = Math.ceil(0);
  max = Math.floor(9);
  return Math.floor(Math.random() * (max - min)) + min; //최댓값은 제외, 최솟값은 포함
}

let answerBoard;
let usrBoard;

var callMatAPI = (level) => {
    // instantiate a headers object
    var myHeaders = new Headers();
    // add content type header to object
    myHeaders.append("Content-Type", "application/json");
    // using built in JSON utility package turn object to string and store in a variable
    var raw = JSON.stringify({
        "Level": level
    });
    // create a JSON object with parameters for API call and store in a variable
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    // make API call with parameters and use promises to get response
    fetch("https://v2ri4l5ybk.execute-api.us-west-2.amazonaws.com/boardPost", requestOptions)
        .then(function (response) {
            return response.text();
        }).then(function (result) {
            let data = JSON.parse(JSON.parse(result).body);
            answerBoard = data["board"];
            usrBoard = data["usr_board"];
            make_matrix(data["usr_board"]);
        })
        .catch(error => console.log('error', error));

}



function make_matrix(barray)
{
    var tag = '<table border="1">';
    for (let i = 0; i < 9; i++) {
        tag+='<tr>';
        for (let j = 0; j < 9; j++)  {
            var id = 'b' + i + ',' + j;
            tag += '<td class="sudokumat" id='+'"'+id + '"' + '>';
            if (barray[i][j] == 0)
            {
                tag += '<form><input type="number" min="1" max="9" value="0" id="'+id+'_"/></form>';
            }else
            {
                tag += barray[i][j];
            }
           tag+='</td>';
        }
        tag+='</tr>'
    }
    tag+='</table>';
    
    document.getElementById("board").innerHTML = tag;
    document.getElementById("boardsubmit").style.visibility = "visible";
    document.getElementById("Hint").style.visibility = "visible";
}


function Value(r, c)
{
    var id = 'b' + r + ',' + c;
    var x = document.getElementById(id).innerHTML;
    if (x.length > 1) x = document.getElementById(id + '_').value;
    
    return x;
}

function wrongAnswer(r, c)
{
    const id = 'b' + r + ',' + c;
    const cell = document.getElementById(id);
    if (cell.classList.contains("runAnimation"))
    {
        cell.classList.remove("runAnimation");
    }
    cell.classList.add("runAnimation");
}

function Hint(r, c)
{
    alert(answerBoard[r][c]);
}

const submitButton = document.getElementById("boardsubmit");
const passBox = document.querySelector(".passBox");

submitButton.addEventListener("click", e => {
    e.preventDefault;

    let isPassed = true;
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            if (answerBoard[i][j] !== parseInt(Value(i, j))) {
                wrongAnswer(i, j);
                isPassed = false;
            }
        }
    }
    if (isPassed)
        passBox.innerHTML = "Good job!";
    else
        passBox.innerHTML = "Wrong answer😥"; 
})