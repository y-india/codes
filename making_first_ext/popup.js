document.getElementById("jokeBtn").onclick = function() {
    const jokes = [
        "Why did the computer sneeze? It had a virus.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "Why was the JavaScript developer sad? Because he didn't Node how to Express himself."
    ];

    const random = jokes[Math.floor(Math.random() * jokes.length)];
    document.getElementById("joke").textContent = random;
};


