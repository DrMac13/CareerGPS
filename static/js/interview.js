console.log("Interview JS loaded");

let currentSessionId = null;

document.addEventListener("DOMContentLoaded", () => {
    const startBtn = document.getElementById("startInterviewBtn");
    const finishBtn = document.getElementById("finishInterviewBtn");

    if (startBtn) {
        startBtn.addEventListener("click", startInterview);
    }

    if (finishBtn) {
        finishBtn.addEventListener("click", finishInterview);
    }
});

function startInterview() {
    const role = document.getElementById("roleSelect").value;

    fetch("/api/interviews/start/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            role: role
        })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert(data.error || "Could not start interview");
                return;
            }

            currentSessionId = data.session_id;

            renderQuestions(data.questions);

            document.getElementById("finishInterviewBtn").style.display = "inline-block";
            document.getElementById("reportContainer").innerHTML = "";
        })
        .catch(error => {
            console.error(error);
            alert("Error starting interview");
        });
}

function renderQuestions(questions) {
    const container = document.getElementById("questionsContainer");

    container.innerHTML = "";

    questions.forEach(question => {
        const card = document.createElement("div");

        card.innerHTML = `
            <hr>

            <h3>Question ${question.question_order}</h3>

            <p>${question.question_text}</p>

            <textarea
                id="answer-${question.id}"
                rows="5"
                cols="60"
                placeholder="Type your answer here..."
            ></textarea>

            <br><br>

            <button onclick="submitAnswer(${question.id})">
                Submit Answer
            </button>

            <div id="feedback-${question.id}"></div>
        `;

        container.appendChild(card);
    });
}

function submitAnswer(questionId) {
    const answerBox = document.getElementById(`answer-${questionId}`);
    const responseText = answerBox.value.trim();

    if (!responseText) {
        alert("Please type an answer first.");
        return;
    }

    fetch("/api/interviews/respond/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            session_id: currentSessionId,
            question_id: questionId,
            response_text: responseText,
            duration_seconds: 60
        })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert(data.error || "Could not submit answer");
                return;
            }

            const feedback = data.feedback;
            const feedbackBox = document.getElementById(`feedback-${questionId}`);

            feedbackBox.innerHTML = `
                <h4>Feedback</h4>
                <p><strong>Overall Score:</strong> ${feedback.overall_score}%</p>
                <p><strong>Confidence Score:</strong> ${feedback.confidence_score}%</p>
                <p><strong>STAR Score:</strong> ${feedback.star_score}%</p>
                <p><strong>Strengths:</strong> ${feedback.strengths}</p>
                <p><strong>Improvements:</strong> ${feedback.improvements}</p>
            `;
        })
        .catch(error => {
            console.error(error);
            alert("Error submitting answer");
        });
}

function finishInterview() {
    if (!currentSessionId) {
        alert("Start an interview first.");
        return;
    }

    fetch(`/api/interviews/report/${currentSessionId}/`)
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert(data.error || "Could not generate report");
                return;
            }

            const container = document.getElementById("reportContainer");

            container.innerHTML = `
                <hr>
                <h2>Interview Report</h2>

                <p><strong>Role:</strong> ${data.role}</p>
                <p><strong>Questions Answered:</strong> ${data.questions_answered}</p>
                <p><strong>Overall Score:</strong> ${data.overall_score}%</p>
                <p><strong>Confidence Score:</strong> ${data.confidence_score}%</p>
                <p><strong>STAR Score:</strong> ${data.star_score}%</p>

                <h3>Question Breakdown</h3>
            `;

            data.question_results.forEach((item, index) => {
                container.innerHTML += `
                    <div>
                        <hr>
                        <h4>Question ${index + 1}</h4>
                        <p><strong>Question:</strong> ${item.question}</p>
                        <p><strong>Your Answer:</strong> ${item.answer}</p>
                        <p><strong>Score:</strong> ${item.overall_score}%</p>
                        <p><strong>Strengths:</strong> ${item.strengths}</p>
                        <p><strong>Improvements:</strong> ${item.improvements}</p>
                    </div>
                `;
            });
        })
        .catch(error => {
            console.error(error);
            alert("Error generating report");
        });
}