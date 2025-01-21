// Populates text gradually
function populateText(text, delay) 
{
    let index = 0;

    const intervalId = setInterval(function() 
    {
        document.getElementById('text').textContent += text[index++];

        if (index === text.length) 
            clearInterval(intervalId);
    }, 
    delay);
}

populateText("Bianca... \n", 100);

setTimeout(function() 
{
    document.getElementById('text').innerHTML += "<br>"; // Add the line break
    populateText("you lil'bitch.", 100);
},
2000);