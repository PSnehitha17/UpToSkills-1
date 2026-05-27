async function generateSpeech(){

    const text = document.getElementById("textInput").value;

    if(text.trim() === ""){
        alert("Please enter text");
        return;
    }

    const response = await fetch("/generate",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            text:text
        })
    });

    const data = await response.json();

    // Show status
    document.getElementById("status").innerHTML =
        `${data.status}<br><small>Normalized: ${data.normalized_text}</small>`;

    // Play audio
    const audioPlayer = document.getElementById("audioPlayer");

    audioPlayer.src = "/cache/" + data.audio;

    audioPlayer.play();
}



async function clearCache(){

    const response = await fetch("/clear-cache",{
        method:"POST"
    });

    const data = await response.json();

    document.getElementById("status").innerHTML = data.message;

    document.getElementById("audioPlayer").src = "";
}