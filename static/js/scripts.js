function analyzeResume() {
    const jobDescription = document.getElementById("job-description").value;
    const resumeFile = document.getElementById("resume-upload").files[0];
    processRequest('analyze', jobDescription, resumeFile);
}

function improveSkill() {
    const jobDescription = document.getElementById("job-description").value;
    const resumeFile = document.getElementById("resume-upload").files[0];
    processRequest('improve', jobDescription, resumeFile);
}

function percentageMatch() {
    const jobDescription = document.getElementById("job-description").value;
    const resumeFile = document.getElementById("resume-upload").files[0];
    processRequest('match', jobDescription, resumeFile);
}

function processRequest(action, jobDescription, resumeFile) {
    const formData = new FormData();
    formData.append('action', action);
    formData.append('job_description', jobDescription);
    formData.append('resume', resumeFile);

    fetch('/process', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response-content").textContent = data.response;
    })
    .catch(error => console.error('Error:', error));
}
