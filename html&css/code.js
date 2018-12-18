var compteur = 0;
var data = null;


function getXMLHttpRequest() {
	var xhr = null;

	if (window.XMLHttpRequest || window.ActiveXObject) {
		if (window.ActiveXObject) {
			try {
				xhr = new ActiveXObject("Msxml2.XMLHTTP");
			} catch(e) {
				xhr = new ActiveXObject("Microsoft.XMLHTTP");
			}
		} else {
			xhr = new XMLHttpRequest();
		}
	} else {
		alert("Votre navigateur ne supporte pas l'objet XMLHTTPRequest...");
		return null;
	}

	return xhr;
}

function request(idButton,callback,textToSend = "None") {
	var xhr = getXMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 0)) {
			callback(xhr.responseText);
		}
	};
	var text ;
	var sVar1 ;
	if (textToSend != "None") {
		text = textToSend
	  sVar1 = encodeURIComponent(document.getElementById("message").innerHTML+" "+text);
	}
	else {
		text = document.getElementById(idButton).innerHTML
	  sVar1 = encodeURIComponent(document.getElementById("message").innerHTML+" "+text);
	}

  //var sVar2 = encodeURIComponent("nothing wrong");

	xhr.open("GET", "http://localhost:5000/api"+"?"+ "var=" + sVar1, true);
	document.getElementById("message").innerHTML +=" "+text;
  //xhr.open("GET", "http://localhost:5000"+"?variable1=" + sVar1 + "&variable2= " + sVar2, true);
  xhr.send(null);
	// xhr.open("POST", "http://localhost:5000/Contact", true);
	// xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	// xhr.send("variable1=truc&variable2=bidule");
}

function readData(sData) {
	// On peut maintenant traiter les données sans encombrer l'objet XHR.
	//alert("recu " + sData)
	data = sData.split(" ");
	document.getElementById("1").innerHTML = data[0];
	document.getElementById("2").innerHTML = data[1];
	document.getElementById("3").innerHTML = data[2];
	document.getElementById("4").innerHTML = data[3];

	compteur = 0;

	//alert("C'est bon");
}

function nextFunction() {
	// On peut maintenant traiter les données sans encombrer l'objet XHR.
	//alert("recu " + sData)
	if (compteur < 9) {
		compteur += 1;
	}

	document.getElementById("1").innerHTML = data[0+(4*compteur)];
	document.getElementById("2").innerHTML = data[1+(4*compteur)];
	document.getElementById("3").innerHTML = data[2+(4*compteur)];
	document.getElementById("4").innerHTML = data[3+(4*compteur)];

	//alert("C'est bon");
}

function sendFunction() {
	document.getElementById("sendedMessage").innerHTML += "<br><mark>  "+document.getElementById("message").innerHTML.split("Message :")+"  </mark>" ;
	document.getElementById("message").innerHTML ="Message :";
	request("1",readData,"")
	//alert("C'est bon");
}

function testrequest(x){
	request(x.id,readData);
}
