console.log("Dashboard JS loaded");

document.addEventListener("DOMContentLoaded", () => {
    loadRecommendations();
    loadRecommendationAnalytics();
    loadApplications();
    loadInterviewHistory();
    loadInterviewAnalytics();
    loadSavedOpportunities();
    loadDashboardOverview();
    loadMarketSkills();
    loadCareerReadiness();
    loadDashboardCareerReadiness();

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

            if (!container) {
                return;
            }

            if (!data.success || data.recommendations.length === 0) {
                container.innerHTML =
                    "<p>No recommendations found.</p>";
                return;
            }

            container.innerHTML = "";

            const isDashboard =
                window.location.pathname === "/dashboard/";

            const recommendationsToShow =
                isDashboard
                    ? data.recommendations.slice(0, 3)
                    : data.recommendations;

            recommendationsToShow.forEach(item => {

                const card =
                    document.createElement("div");

                card.classList.add("card");

                const matchedSkills =
                    item.matched_skills || [];

                const missingSkills =
                    item.missing_skills || [];

                const matchedSkillsHtml =
                    matchedSkills.length
                        ? matchedSkills.map(skill =>
                            `<span class="skill-badge matched">${skill}</span>`
                        ).join("")
                        : "No matched skills";

                const missingSkillsHtml =
                    missingSkills.length
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

                let matchLabel =
                    "Low Match";

                let matchClass =
                    "match-low";

                if (item.match_score >= 70) {
                    matchLabel =
                        "Strong Match";

                    matchClass =
                        "match-high";
                }
                else if (item.match_score >= 40) {
                    matchLabel =
                        "Moderate Match";

                    matchClass =
                        "match-medium";
                }

                card.innerHTML = `
                    <div class="match-row">

                        <span class="match-tag ${matchClass.replace("match-", "")}">
                            <span class="match-dot"></span>
                            ${matchLabel}
                        </span>

                        <span class="match-score ${matchClass}">
                            ${item.match_score}%
                        </span>

                    </div>

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
                        <strong>Why:</strong>
                        ${item.reasons}
                    </p>

                    
                    ${!isDashboard ? `

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

                            <div class="learning-list">
                                ${learningResourcesHtml}
                            </div>
                        </div>

                    ` : ""}

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

            const container =
                document.getElementById("recommendationsList");

            if (container) {
                container.innerHTML =
                    "<p>Error loading recommendations.</p>";
            }

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

            if (!container) {
                return;
            }

            if (!data.success || data.applications.length === 0) {
                container.innerHTML =
                    "<p>No applications yet.</p>";
                return;
            }

            container.innerHTML = "";

            data.applications.forEach(app => {

                const card =
                    document.createElement("div");

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
                        <strong>Applied:</strong>
                        ${app.applied_at}
                    </p>

                    <div class="application-status-block">

                        <label>
                            Status
                        </label>

                        <select
                            id="status-${app.id}"
                            class="application-status-select"
                        >
                            <option value="Applied" ${app.status === "Applied" ? "selected" : ""}>Applied</option>
                            <option value="Interviewing" ${app.status === "Interviewing" ? "selected" : ""}>Interviewing</option>
                            <option value="Rejected" ${app.status === "Rejected" ? "selected" : ""}>Rejected</option>
                            <option value="Offer" ${app.status === "Offer" ? "selected" : ""}>Offer</option>
                            <option value="Accepted" ${app.status === "Accepted" ? "selected" : ""}>Accepted</option>
                        </select>

                    </div>

                    <div class="application-notes-block">

                        <label>
                            Notes
                        </label>

                        <textarea
                            id="notes-${app.id}"
                            class="application-notes"
                            placeholder="Add notes about this application..."
                        >${app.notes || ""}</textarea>

                    </div>

                    <button onclick="updateApplicationStatus(${app.id})">
                        Update Application
                    </button>

                    <a
                        href="${app.application_url}"
                        target="_blank"
                    >
                        View Job
                    </a>
                `;

                container.appendChild(card);

            });

        })
        .catch(error => {

            console.error(error);

            const container =
                document.getElementById("applicationsList");

            if (container) {
                container.innerHTML =
                    "<p>Error loading applications.</p>";
            }

        });
}


function updateApplicationStatus(applicationId) {

    const statusInput =
        document.getElementById(`status-${applicationId}`);

    const notesInput =
        document.getElementById(`notes-${applicationId}`);

    if (!statusInput || !notesInput) {
        return;
    }

    fetch("/api/applications/update-status/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            application_id: applicationId,
            status: statusInput.value,
            notes: notesInput.value
        })
    })
        .then(response => response.json())
        .then(data => {

            if (data.success) {
                alert("Application updated");
                loadApplications();
            }
            else {
                alert(data.error || "Could not update application");
            }

        })
        .catch(error => {

            console.error(error);
            alert("Error updating application");

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

function loadSavedOpportunities() {

    const container =
        document.getElementById("savedOpportunitiesList");

    if (!container) {
        return;
    }

    fetch("/api/bookmarks/")
        .then(response => response.json())
        .then(data => {

            if (
                !data.success ||
                data.saved_opportunities.length === 0
            ) {
                container.innerHTML =
                    "<p>No saved opportunities yet.</p>";
                return;
            }

            container.innerHTML = "";

            data.saved_opportunities.forEach(item => {

                const card =
                    document.createElement("div");

                card.classList.add("card");

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

                    <p>
                        <strong>Saved:</strong>
                        ${item.saved_at}
                    </p>

                    <button onclick="toggleBookmark(${item.id})">
                        Remove Bookmark
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

            container.innerHTML =
                "<p>Error loading saved opportunities.</p>";

        });
}

function loadDashboardOverview() {

    const recommendations =
        document.getElementById("overviewRecommendations");

    const saved =
        document.getElementById("overviewSaved");

    const applications =
        document.getElementById("overviewApplications");

    const profile =
        document.getElementById("overviewProfile");

    if (!recommendations || !saved || !applications || !profile) {
        return;
    }

    fetch("/api/recommendations/analytics/")
        .then(response => response.json())
        .then(data => {
            recommendations.textContent =
                data.success
                    ? data.analytics.total_recommendations
                    : "0";
        });

    fetch("/api/bookmarks/")
        .then(response => response.json())
        .then(data => {

            const count =
                data.success
                    ? data.saved_opportunities.length
                    : 0;

            saved.textContent = count;

            const snapshotSaved =
                document.getElementById("snapshotSaved");

            if (snapshotSaved) {
                snapshotSaved.textContent = count;
            }

        });

    fetch("/api/applications/")
        .then(response => response.json())
        .then(data => {
            applications.textContent =
                data.success
                    ? data.applications.length
                    : "0";
        });
    fetch("/api/profile/summary/")
        .then(response => response.json())
        .then(data => {

            if (!data.success) {
                profile.textContent = "0%";
                return;
            }

            profile.textContent =
                `${data.completion}%`;

            const snapshotCompletion =
                document.getElementById("snapshotCompletion");

            const snapshotNextStep =
                document.getElementById("snapshotNextStep");

            if (snapshotCompletion) {
                snapshotCompletion.textContent =
                    `${data.completion}%`;
            }

            if (snapshotNextStep) {

                if (data.completion < 70) {

                    snapshotNextStep.textContent =
                        "Complete your profile";

                } else {

                    snapshotNextStep.textContent =
                        "Explore opportunities";

                }

            }

        });

    const snapshotCompletion =
    document.getElementById("snapshotCompletion");

    const snapshotSaved =
        document.getElementById("snapshotSaved");

    const snapshotStrongMatches =
        document.getElementById("snapshotStrongMatches");

    const snapshotNextStep =
        document.getElementById("snapshotNextStep");
}

function loadMarketSkills() {

    const container =
        document.getElementById("marketSkillsList");

    if (!container) {
        return;
    }

    fetch("/api/market-skills/")
        .then(response => response.json())
        .then(data => {

            if (!data.success || data.skills.length === 0) {
                container.innerHTML =
                    "<p>No market skills data available yet.</p>";
                return;
            }

            container.innerHTML = `
                <h3>Most requested skills</h3>

                <p>
                    These skills appear most often across imported opportunities.
                </p>

                <div class="market-skills-list">
                    ${data.skills.map((skill, index) => `
                        <div class="market-skill-item">
                            <span class="market-skill-rank">
                                ${index + 1}
                            </span>

                            <div>
                                <strong>
                                    ${skill.name}
                                </strong>

                                <p>
                                    ${skill.category} · ${skill.demand_count} opportunities
                                </p>
                            </div>
                        </div>
                    `).join("")}
                </div>
            `;

        })
        .catch(error => {

            console.error(error);

            container.innerHTML =
                "<p>Error loading market skills.</p>";

        });
}

function loadCareerReadiness() {

    const container =
        document.getElementById("careerReadinessCard");

    if (!container) {
        return;
    }

    fetch("/api/career-readiness/")
        .then(response => response.json())
        .then(data => {

            if (!data.success) {
                container.innerHTML =
                    "<p>Career readiness data is not available.</p>";
                return;
            }

            const skillsYouHaveHtml =
                data.skills_you_have.length
                    ? data.skills_you_have.map(skill => `
                        <span class="skill-badge matched">
                            ${skill.name}
                        </span>
                    `).join("")
                    : "No top market skills matched yet.";

            const missingSkillsHtml =
                data.missing_high_impact_skills.length
                    ? data.missing_high_impact_skills.slice(0, 5).map(skill => `
                        <span class="skill-badge missing">
                            ${skill.name}
                        </span>
                    `).join("")
                    : "No major missing market skills.";

            const nextSkill =
                data.recommended_next_skill;

            container.innerHTML = `
                <h3>
                    ${data.readiness_score}% Career Readiness
                </h3>

                <p>
                    Career direction:
                    <strong>${data.career_direction}</strong>
                </p>

                <div class="career-readiness-grid">

                    <div>
                        <strong>Skills You Already Have</strong>

                        <div class="skill-badges">
                            ${skillsYouHaveHtml}
                        </div>
                    </div>

                    <div>
                        <strong>Missing Top Market Skills</strong>

                        <div class="skill-badges">
                            ${missingSkillsHtml}
                        </div>
                    </div>

                </div>

                <div class="readiness-next-step">

                    <strong>Recommended Next Skill</strong>

                    <p>
                        ${
                            nextSkill
                                ? `${nextSkill.name} appears in ${nextSkill.market_count} imported opportunities.`
                                : "You currently cover the top market skills."
                        }
                    </p>

                    <a href="/dashboard/resources/#market-skills">
                        View Market Skills
                    </a>

                </div>
            `;

        })
        .catch(error => {

            console.error(error);

            container.innerHTML =
                "<p>Error loading career readiness intelligence.</p>";

        });
}


function loadDashboardCareerReadiness() {

    const container =
        document.getElementById(
            "dashboardCareerReadiness"
        );

    if (!container) {
        return;
    }

    fetch("/api/career-readiness/")
        .then(response => response.json())
        .then(data => {

            if (!data.success) {

                container.innerHTML =
                    "<p>Career readiness unavailable.</p>";

                return;
            }

            let readinessLevel =
                "Early Stage";

            if (data.readiness_score >= 90) {

                readinessLevel =
                    "Highly Competitive";

            }
            else if (data.readiness_score >= 70) {

                readinessLevel =
                    "Market Ready";

            }
            else if (data.readiness_score >= 40) {

                readinessLevel =
                    "Intermediate Stage";

            }

            const skillsYouHave =
                data.skills_you_have
                    .slice(0, 3)
                    .map(skill => `
                        <span class="skill-badge matched">
                            ✓ ${skill.name}
                        </span>
                    `)
                    .join("");

            const missingSkills =
                data.missing_high_impact_skills
                    .slice(0, 3)
                    .map(skill => `
                        <span class="skill-badge missing">
                            ✗ ${skill.name}
                        </span>
                    `)
                    .join("");

            container.innerHTML = `

                <div class="readiness-header">

                    <div>

                        <div class="readiness-score">
                            ${data.readiness_score}%
                        </div>

                        <div class="readiness-level">
                            ${readinessLevel}
                        </div>

                    </div>

                </div>

                <div class="readiness-content">

                    <div>

                        <h4>
                            Skills You Have
                        </h4>

                        <div class="skill-badges">
                            ${skillsYouHave}
                        </div>

                    </div>

                    <div>

                        <h4>
                            Missing High-Impact Skills
                        </h4>

                        <div class="skill-badges">
                            ${missingSkills}
                        </div>

                    </div>

                </div>

                <div class="readiness-next">

                    <strong>
                        Recommended Next Skill
                    </strong>

                    <p>
                        ${
                            data.recommended_next_skill
                                ? data.recommended_next_skill.name
                                : "You're covering the major market skills."
                        }
                    </p>

                    <a
                        href="/dashboard/resources/#career-readiness"
                        class="readiness-link"
                    >
                        View Full Analysis
                    </a>

                </div>

            `;

        })
        .catch(error => {

            console.error(error);

            container.innerHTML =
                "<p>Error loading readiness data.</p>";

        });

}