document.getElementById("taskForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const responseMsg = document.getElementById("responseMsg");
  responseMsg.style.color = "green"; // Default color

  const data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    title: document.getElementById("title").value,
    details: document.getElementById("details").value,
    datetime: formatDate(document.getElementById("datetime").value)
  };

  try {
    const response = await fetch("https://g8fbznaamg.execute-api.us-east-1.amazonaws.com/Dev/submit-task", { //replace with invoke URL
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      responseMsg.innerText = "Plan successfully submitted! Kindly check your mail to confirm the subscription";
      responseMsg.style.color = "green";
    } else {
      const error = await response.json();
      responseMsg.innerText = `Error: ${error.message || 'Something went wrong. Please try again.'}`;
      responseMsg.style.color = "red";
    }
  } catch (err) {
    responseMsg.innerText = "Network error. Please check your internet connection or try again later.";
    responseMsg.style.color = "red";
  }
});

function formatDate(dateTimeString) {
  const d = new Date(dateTimeString);
  return d.toLocaleDateString("en-GB") + " " + d.toTimeString().slice(0, 5);
}

