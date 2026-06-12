console.log("Dashboard JS loaded");

document.addEventListener("DOMContentLoaded", () => {
    loadRecommendations();
    loadApplications();
    loadInterviewHistory();
    loadInterviewAnalytics();

    const searchBtn = document.getElementById("searchBtn");

    if (searchBtn) {
        searchBtn.addEventListener("click", loadOpportunities);
    }
});


function loadRecommendations() {

    fetch("/api/recommendations/")
        .then(response => response.json())
        .then(data => {

            const container =
                document.getElementById(
                    "recommendationsList"
                );

            if (
                !data.success ||
                data.recommendations.length === 0
            ) {
                container.innerHTML =
                    "<p>No recommendations found.</p>";
                return;
            }

            container.innerHTML = "";

            data.recommendations.forEach(item => {

                const card =
                    document.createElement("div");

                card.innerHTML = `
                    <hr>

                    <h3>${item.title}</h3>

                    <p>
                        <strong>Company:</strong>
                        ${item.company}
                    </p>

                    <p>
                        <strong>Location:</strong>
                        ${item.location}
                    </p>

                    <p>
                        <strong>Type:</strong>
                        ${item.opportunity_type}
                    </p>

                    <p>
                        <strong>Match Score:</strong>
                        ${item.match_score}%
                    </p>

                    <p>
                        <strong>Why:</strong>
                        ${item.reasons}
                    </p>

                    <button onclick="toggleBookmark(${item.id})">
                        Save Job
                    </button>

                    <button onclick="applyToOpportunity(${item.id})">
                        Track Application
                    </button>

                    <a
                        href="${item.application_url}"
                        target="_blank"
                    >
                        Apply
                    </a>
                `;

                container.appendChild(card);

            });

        })
        .catch(error => {

            console.error(error);

            document.getElementById(
                "recommendationsList"
            ).innerHTML =
                "<p>Error loading recommendations.</p>";

        });

}



function loadOpportunities() {

    const search =
        document.getElementById(
            "searchInput"
        ).value;

    const type =
        document.getElementById(
            "typeFilter"
        ).value;

    fetch(
        `/api/opportunities/?search=${search}&type=${type}`
    )
        .then(response => response.json())
        .then(data => {

            const container =
                document.getElementById(
                    "opportunityResults"
                );

            if (
                !data.success ||
                data.opportunities.length === 0
            ) {

                container.innerHTML =
                    "<p>No opportunities found.</p>";

                return;
            }

            container.innerHTML = "";

            data.opportunities.forEach(job => {

                const card =
                    document.createElement("div");

                card.innerHTML = `
                    <hr>

                    <h3>${job.title}</h3>

                    <p>
                        <strong>Company:</strong>
                        ${job.company}
                    </p>

                    <p>
                        <strong>Location:</strong>
                        ${job.location}
                    </p>

                    <p>
                        <strong>Type:</strong>
                        ${job.opportunity_type}
                    </p>

                    <p>
                        <strong>Experience:</strong>
                        ${job.experience_level}
                    </p>

                    <button onclick="toggleBookmark(${job.id})">
                        Save Job
                    </button>

                    <button onclick="applyToOpportunity(${job.id})">
                        Track Application
                    </button>

                    <a
                        href="${job.application_url}"
                        target="_blank"
                    >
                        Apply
                    </a>
                `;

                container.appendChild(card);

            });

        })
        .catch(error => {

            console.error(error);

            document.getElementById(
                "opportunityResults"
            ).innerHTML =
                "<p>Error loading opportunities.</p>";

        });

}



function toggleBookmark(opportunityId) {

    fetch("/api/bookmarks/toggle/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            opportunity_id: opportunityId
        })

    })
        .then(response => response.json())
        .then(data => {

            alert(
                data.message ||
                "Bookmark updated"
            );

        })
        .catch(error => {

            console.error(error);

            alert(
                "Error saving opportunity"
            );

        });

}


function applyToOpportunity(opportunityId) {

    fetch("/api/opportunities/apply/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            opportunity_id: opportunityId
        })

    })
        .then(response => response.json())
        .then(data => {

            alert(
                data.message ||
                "Application updated"
            );

            loadApplications();

        })
        .catch(error => {

            console.error(error);

            alert(
                "Error applying"
            );

        });

}

function loadApplications() {

    fetch("/api/applications/")
        .then(response => response.json())
        .then(data => {

            const container =
                document.getElementById(
                    "applicationsList"
                );

            if (
                !data.success ||
                data.applications.length === 0
            ) {

                container.innerHTML =
                    "<p>No applications yet.</p>";

                return;
            }

            container.innerHTML = "";

            data.applications.forEach(app => {

                const card =
                    document.createElement("div");

                card.innerHTML = `
                    <hr>

                    <h3>${app.title}</h3>

                    <p>
                        <strong>Company:</strong>
                        ${app.company}
                    </p>

                    <p>
                        <strong>Location:</strong>
                        ${app.location}
                    </p>

                    <p>
                        <strong>Status:</strong>
                        ${app.status}
                    </p>

                    <p>
                        <strong>Applied:</strong>
                        ${app.applied_at}
                    </p>

                    <a
                        href="${app.application_url}"
                        target="_blank"
                    >
                        View Application
                    </a>
                `;

                container.appendChild(card);

            });

        })
        .catch(error => {

            console.error(error);

            document.getElementById(
                "applicationsList"
            ).innerHTML =
                "<p>Error loading applications.</p>";

        });

}

function loadInterviewHistory() {
    fetch("/api/interviews/history/")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("interviewHistoryList");

            if (!data.success || data.history.length === 0) {
                container.innerHTML = "<p>No interviews completed yet.</p>";
                return;
            }

            container.innerHTML = "";

            data.history.forEach(session => {
                const card = document.createElement("div");

                card.innerHTML = `
                    <hr>
                    <h3>${session.role}</h3>
                    <p><strong>Started:</strong> ${session.started_at}</p>
                    <p><strong>Completed:</strong> ${session.completed_at || "Not completed"}</p>
                    <p><strong>Questions Answered:</strong> ${session.responses_count}</p>
                    <p><strong>Overall Score:</strong> ${session.overall_score ?? "Pending"}%</p>
                    <a href="/interview/">
                        Practice Again
                    </a>
                `;

                container.appendChild(card);
            });
        })
        .catch(error => {
            console.error(error);
            document.getElementById("interviewHistoryList").innerHTML =
                "<p>Error loading interview history.</p>";
        });
}


function loadInterviewAnalytics() {

    fetch("/api/interviews/analytics/")
        .then(response => response.json())
        .then(data => {

            const container =
                document.getElementById(
                    "interviewAnalytics"
                );

            if (
                !data.success ||
                data.analytics.total_interviews === 0
            ) {

                container.innerHTML = `
                    <p>
                        No completed interviews yet.
                    </p>
                `;

                return;
            }

            const analytics =
                data.analytics;

            renderInterviewTrendChart(
                analytics.trend
            );

            container.innerHTML = `
                <div>

                    <p>
                        <strong>Total Interviews:</strong>
                        ${analytics.total_interviews}
                    </p>

                    <p>
                        <strong>Average Score:</strong>
                        ${analytics.average_score}%
                    </p>

                    <p>
                        <strong>Highest Score:</strong>
                        ${analytics.highest_score}%
                    </p>

                    <p>
                        <strong>Lowest Score:</strong>
                        ${analytics.lowest_score}%
                    </p>

                    <p>
                        <strong>Strongest Role:</strong>
                        ${analytics.strongest_role}
                    </p>

                    <p>
                        <strong>Weakest Role:</strong>
                        ${analytics.weakest_role}
                    </p>

                </div>
            `;
            renderInterviewTrendChart(analytics.trend);

        })
        .catch(error => {

            console.error(error);

            document.getElementById(
                "interviewAnalytics"
            ).innerHTML =
                "<p>Error loading analytics.</p>";

        });
}

function renderInterviewTrendChart(trendData) {
    const canvas = document.getElementById("interviewTrendChart");

    if (!canvas || !trendData || trendData.length === 0) {
        return;
    }

    const labels = trendData.map(item => item.label);
    const scores = trendData.map(item => item.score);

    new Chart(canvas, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Interview Score",
                    data: scores,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}


let interviewTrendChart = null;

function renderInterviewTrendChart(trendData) {

    const canvas =
        document.getElementById(
            "interviewTrendChart"
        );

    if (
        !canvas ||
        !trendData ||
        trendData.length === 0
    ) {
        return;
    }

    if (interviewTrendChart) {
        interviewTrendChart.destroy();
    }

    const labels =
        trendData.map(
            item => item.label
        );

    const scores =
        trendData.map(
            item => item.score
        );

    interviewTrendChart = new Chart(canvas, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {
                    label: "Interview Score",
                    data: scores,
                    tension: 0.3,
                    fill: false
                }

            ]
        },

        options: {

            responsive: true,

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100

                }
            }
        }
    });
}