const dropArea = document.getElementById("dropArea");

const fileInput = document.getElementById("resume");

const fileName = document.getElementById("fileName");

dropArea.addEventListener("click", () => {

    fileInput.click();

});

fileInput.addEventListener("change", () => {

    if(fileInput.files.length){

        fileName.innerHTML = fileInput.files[0].name;

    }

});

dropArea.addEventListener("dragover",(e)=>{

    e.preventDefault();

});

dropArea.addEventListener("drop",(e)=>{

    e.preventDefault();

    fileInput.files = e.dataTransfer.files;

    fileName.innerHTML = e.dataTransfer.files[0].name;

});

document.getElementById("submitBtn").addEventListener("click",()=>{

    const jd = document.getElementById("jobDescription").value;

    const resume = fileInput.files[0];

    console.log(jd);

    console.log(resume);

    alert("Submitted Successfully!");

});



const historyBtn = document.getElementById("historyBtn");
const historyMenu = document.getElementById("historyMenu");

historyBtn.addEventListener("click", () => {

    if(historyMenu.style.display === "block"){

        historyMenu.style.display = "none";

    }else{

        historyMenu.style.display = "block";

    }

});

const submitBtn = document.getElementById("submitBtn");
const btnText = document.getElementById("btnText");
const loader = document.getElementById("loader");

submitBtn.addEventListener("click", () => {

    const jd = document.getElementById("jobDescription").value;
    const resume = document.getElementById("resume").files[0];

    submitBtn.disabled = true;
    btnText.textContent = "Processing...";
    loader.style.display = "inline-block";

    // Simulate 10 seconds of processing
    setTimeout(() => {

        console.log(jd);
        console.log(resume);

        // Stop spinner
        loader.style.display = "none";

        // Show success
        btnText.textContent = "Process Done!";

        // Keep "Done!" visible for 5 seconds
        setTimeout(() => {

            btnText.textContent = "Submit";
            submitBtn.disabled = false;

        }, 5000);

    }, 10000);

});