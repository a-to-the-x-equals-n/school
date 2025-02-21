const CURSOR = document.getElementById('cursor');

const HAPPY_LIST = [];


function todays_msg()
{
    let randomIndex = Math.floor(Math.random() * HAPPY_LIST.length);
    return [
        "Come human!",
        "Come and bask in the belles-lettres of my people!"
        // HAPPY_LIST[randomIndex] // random message
    ];
}


function populateText(messages, delay) 
{
    let messageIndex = 0;
    const textElement = document.getElementById('text');

    function typeMessage(message) 
    {
        let index = 0;
        textElement.textContent = "> "; // Reset text with prompt
        textElement.appendChild(CURSOR); // Ensure cursor stays at the end

        const intervalId = setInterval(function () 
        {
            textElement.insertBefore(document.createTextNode(message[index++]), CURSOR);
            if (index === message.length) 
            {
                clearInterval(intervalId); // Stop typing this message
                if (messageIndex < messages.length - 1) 
                {
                    messageIndex++;
                    setTimeout(() => clearText(() => typeMessage(messages[messageIndex]), delay), 1800); // Pause before clearing
                }
            }
        }, delay);
    }

    function clearText(callback, delay) 
    {
        let currentLength = textElement.textContent.length - 2; // Ignore "> "
        const eraseInterval = setInterval(() => 
        {
            if (currentLength > 0) 
            {
                textElement.textContent = textElement.textContent.slice(0, currentLength--); // Keep cursor
            } 
            else 
            {
                clearInterval(eraseInterval);
                textElement.textContent = "> "; // Reset with prompt
                textElement.appendChild(CURSOR); // Keep cursor
                setTimeout(callback, delay); // Start next message
            }
        }, 50); // Speed of erasing
    }
    typeMessage(messages[messageIndex]); // Start with the first message
}


// run on page load
document.addEventListener("DOMContentLoaded", function () 
{
    let positivity = todays_msg();
    populateText(positivity, 125);
});