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

function request(idButton,callback) {
	var xhr = getXMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 0)) {
			callback(xhr.responseText);
		}
	};
	var text = document.getElementById(idButton).innerHTML
  var sVar1 = encodeURIComponent(document.getElementById("message").innerHTML+" "+text);
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
	document.getElementById("1").innerHTML = sData.split(" ")[0];
	document.getElementById("2").innerHTML = sData.split(" ")[1];
	document.getElementById("3").innerHTML = sData.split(" ")[2];
	document.getElementById("4").innerHTML = sData.split(" ")[3];

	//alert("C'est bon");
}

function testrequest(x){
	request(x.id,readData);
}
