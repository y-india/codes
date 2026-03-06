document.getElementById("jokeBtn").onclick = function() {
    const jokes = [
        "Why did the computer sneeze? It had a virus.",
        "Why was the computer cold? It left its Windows open.",
        "Why did the phone go to school? To get smarter.",
        "Why did the keyboard break up with the computer? It felt no connection.",
        "Why did the computer get glasses? To improve its web sight.",
        "Why did the programmer quit his job? He didn’t get arrays.",
        "Why was the robot tired? It worked all night.",
        "Why did the computer go to sleep? It had too many tabs open.",
        "Why did the laptop go to the doctor? It had a bad byte.",
        "Why did the mouse stay at home? It lost its click.",
        "Why did the computer bring a ladder? To reach the cloud.",
        "Why did the programmer stay calm? He kept his cool code.",
        "Why did the computer eat snacks? It needed more bytes.",
        "Why did the robot cross the road? To recharge.",
        "Why did the computer fail the test? It had too many bugs.",
        "Why did the tablet feel lonely? It had no contacts.",
        "Why did the computer go to the gym? To get more memory.",
        "Why did the coder bring a pencil? To draw a program.",
        "Why did the phone run fast? It had 4G energy.",
        "Why did the computer smile? It found a good connection."
    ];

    const random = jokes[Math.floor(Math.random() * jokes.length)];
    document.getElementById("joke").textContent = random;
};


