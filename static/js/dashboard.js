console.log("Dashboard JS loaded");

document.addEventListener("DOMContentLoaded", () => {
    loadRecommendations();
    loadRecommendationAnalytics();
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
                document.getElementById("recommendationsList");

            if (!data.success || data.recommendations.length === 0) {
                container.innerHTML =
                    "<p>No recommendations found.</p>";
                return;
            }

            container.innerHTML = "";

            data.recommendations.forEach(item => {

                const card = document.createElement("div");
                card.classList.add("card");

                const matchedSkills = item.matched_skills || [];
                const missingSkills = item.missing_skills || [];


                const matchedSkillsHtml = matchedSkills.length
                    ? matchedSkills.map(skill =>
                        `<span class="skill-badge matched">${skill}</span>`
                    ).join("")
                    : "No matched skills";

                const missingSkillsHtml = missingSkills.length
                    ? missingSkills.map(skill =>
                        `<span class="skill-badge missing">${skill}</span>`
                    ).join("")
                    : "No skill gaps identified";


                const learningResources =
                    item.learning_resources || [];


                const learningResourcesHtml =
                    learningResources.length
                        ? learningResources.map(resource => `
                            <a
                                class="learning-link"
                                href="${resource.url}"
                                target="_blank"
                            >
                                ${resource.title}
                            </a>
                        `).join("")
                        : "No learning recommendations";

                

                let matchLabel = "Development Opportunity";
                let matchClass = "match-low";

                if (item.match_score >= 80) {
                    matchLabel = "Excellent Match";
                    matchClass = "match-high";
                }
                else if (item.match_score >= 60) {
                    matchLabel = "Strong Match";
                    matchClass = "match-medium";
                }
                else if (item.match_score >= 40) {
                    matchLabel = "Moderate Match";
                    matchClass = "match-average";
                }


                card.innerHTML = `
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

                    <div class="match-score-card ${matchClass}">
                        <div class="match-label">
                            ${matchLabel}
                        </div>
                        <span class="match-score ${matchClass}">
                            ${item.match_score}%
                        </span>
                    </div>

                    <p>
                        <strong>Why:</strong>
                        ${item.reasons}
                    </p>

                    <div class="skill-section">
                        <strong>Matched Skills</strong>
                        <div class="skill-badges">
                            ${matchedSkillsHtml}
                        </div>
                    </div>

                    <div class="skill-section">
                        <strong>Skill Gaps</strong>
                        <div class="skill-badges">
                            ${missingSkillsHtml}
                        </div>
                    </div>

                    <div class="learning-resources">
                        <strong>Learning Resources</strong>

                        <div class="learning-buttons">
                            ${learningResourcesHtml}
                        </div>
                    </div>

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

            document.getElementById("recommendationsList").innerHTML =
                "<p>Error loading recommendations.</p>";
        });
}


function loadOpportunities() {

    const search =
        document.getElementById("searchInput").value;

    const type =
        document.getElementById("typeFilter").value;

    fetch(`/api/opportunities/?search=${search}&type=${type}`)
        .then(response => response.json())
        .then(data => {

            const container =
                document.getElementById("opportunityResults");

            if (!data.success || data.opportunities.length === 0) {
                container.innerHTML =
                    "<p>No opportunities found.</p>";
                return;
            }

            container.innerHTML = "";

            data.opportunities.forEach(job => {

                const card = document.createElement("div");
                card.classList.add("card");

                card.innerHTML = `
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

            document.getElementById("opportunityResults").innerHTML =
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
            alert(data.message || "Bookmark updated");
        })
        .catch(error => {
            console.error(error);
            alert("Error saving opportunity");
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
            alert(data.message || "Application updated");
            loadApplications();
        })
        .catch(error => {
            console.error(error);
            alert("Error applying");
        });
}


function loadApplications() {

    fetch("/api/applications/")
        .then(response => response.json())
        .then(data => {

            const container =
                document.getElementById("applicationsList");

            if (!data.success || data.applications.length === 0) {
                container.innerHTML =
                    "<p>No applications yet.</p>";
                return;
            }

            container.innerHTML = "";

            data.applications.forEach(app => {

                const card = document.createElement("div");
                card.classList.add("card");

                card.innerHTML = `
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

            document.getElementById("applicationsList").innerHTML =
                "<p>Error loading applications.</p>";
        });
}


function loadInterviewHistory() {

    fetch("/api/interviews/history/")
        .then(response => response.json())
        .then(data => {

            const container =
                document.getElementById("interviewHistoryList");

            if (!data.success || data.history.length === 0) {
                container.innerHTML =
                    "<p>No interviews completed yet.</p>";
                return;
            }

            container.innerHTML = "";

            data.history.forEach(session => {

                const card = document.createElement("div");
                card.classList.add("card");

                card.innerHTML = `
                    <h3>${session.role}</h3>

                    <p>
                        <strong>Started:</strong>
                        ${session.started_at}
                    </p>

                    <p>
                        <strong>Completed:</strong>
                        ${session.completed_at || "Not completed"}
                    </p>

                    <p>
                        <strong>Questions Answered:</strong>
                        ${session.responses_count}
                    </p>

                    <p>
                        <strong>Overall Score:</strong>
                        ${session.overall_score ?? "Pending"}%
                    </p>

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
                document.getElementById("interviewAnalytics");

            if (!data.success || data.analytics.total_interviews === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        No completed interviews yet.
                    </div>
                `;
                return;
            }

            const analytics = data.analytics;

            container.innerHTML = `
                <div class="card">
                    <h3>Total Interviews</h3>
                    <p>${analytics.total_interviews}</p>
                </div>

                <div class="card">
                    <h3>Average Score</h3>
                    <p>${analytics.average_score}%</p>
                </div>

                <div class="card">
                    <h3>Highest Score</h3>
                    <p>${analytics.highest_score}%</p>
                </div>

                <div class="card">
                    <h3>Lowest Score</h3>
                    <p>${analytics.lowest_score}%</p>
                </div>

                <div class="card">
                    <h3>Strongest Role</h3>
                    <p>${analytics.strongest_role}</p>
                </div>

                <div class="card">
                    <h3>Weakest Role</h3>
                    <p>${analytics.weakest_role}</p>
                </div>
            `;

            renderInterviewTrendChart(analytics.trend);
        })
        .catch(error => {
            console.error(error);

            document.getElementById("interviewAnalytics").innerHTML =
                "<p>Error loading analytics.</p>";
        });
}


let interviewTrendChart = null;

function renderInterviewTrendChart(trendData) {

    const canvas =
        document.getElementById("interviewTrendChart");

    if (!canvas || !trendData || trendData.length === 0) {
        return;
    }

    if (interviewTrendChart) {
        interviewTrendChart.destroy();
    }

    const labels =
        trendData.map(item => item.label);

    const scores =
        trendData.map(item => item.score);

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


function loadRecommendationAnalytics() {

    fetch("/api/recommendations/analytics/")
        .then(response => response.json())
        .then(data => {

            const container =
                document.getElementById("recommendationAnalytics");

            if (!data.success || data.analytics.total_recommendations === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        No recommendation analytics available.
                    </div>
                `;
                return;
            }

            const analytics = data.analytics;

            container.innerHTML = `
                <div class="card">
                    <h3>Total Recommendations</h3>
                    <p>${analytics.total_recommendations}</p>
                </div>

                <div class="card">
                    <h3>Average Match Score</h3>
                    <p>${analytics.average_match_score}%</p>
                </div>

                <div class="card">
                    <h3>Highest Match Score</h3>
                    <p>${analytics.highest_match_score}%</p>
                </div>

                <div class="card">
                    <h3>Top Opportunity Type</h3>
                    <p>${analytics.top_opportunity_type}</p>
                </div>

                <div class="card">
                    <h3>Top Location</h3>
                    <p>${analytics.top_location}</p>
                </div>
            `;

            renderRecommendationScoreChart(
                analytics.score_distribution
            );
        })
        .catch(error => {
            console.error(error);

            document.getElementById("recommendationAnalytics").innerHTML = `
                <div class="empty-state">
                    Error loading recommendation analytics.
                </div>
            `;
        });
}


let recommendationScoreChart = null;

function renderRecommendationScoreChart(distribution) {

    const canvas =
        document.getElementById("recommendationScoreChart");

    if (!canvas || !distribution) {
        return;
    }

    if (recommendationScoreChart) {
        recommendationScoreChart.destroy();
    }

    const labels =
        Object.keys(distribution);

    const values =
        Object.values(distribution);

    recommendationScoreChart = new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Number of Recommendations",
                    data: values
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}