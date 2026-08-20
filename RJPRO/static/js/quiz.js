let currentQuestionIndex = 0;
let userAnswers = [];
let quizQuestions = [];
let currentLevel = null;
let timer = null;
let timeLeft = 30;

// Sample questions for each level
const questionsByLevel = {
    easy: [
        {
            question: "Which of the following is a strong password?",
            options: ["12345", "Password1", "admin123", "X7#9!PqT"],
            correctAnswer: 3
        },
        {
            question: "What does a firewall do?",
            options: ["Cleans your computer", "Prevents unauthorized access", "Boosts internet speed", "Stores data"],
            correctAnswer: 1
        },
        {
            question: "What is phishing?",
            options: ["A computer virus", "A fraudulent attempt to get sensitive information", "A network protocol", "A backup method"],
            correctAnswer: 1
        },
        {
            question: "What is two-factor authentication?",
            options: ["Using two different passwords", "Using two devices to login", "Using two security methods to verify identity", "Having two email accounts"],
            correctAnswer: 2
        },
        {
            question: "Which of these is NOT a common cybersecurity threat?",
            options: ["Malware", "Phishing", "Overclocking", "Ransomware"],
            correctAnswer: 2
        },
        {
            question: "What is a VPN used for?",
            options: ["Virus scanning", "Secure and private internet connection", "Password storage", "File sharing"],
            correctAnswer: 1
        },
        {
            question: "What is malware?",
            options: ["Malicious software", "Hardware failure", "Network protocol", "Security tool"],
            correctAnswer: 0
        },
        {
            question: "What should you do if you receive a suspicious email?",
            options: ["Open all attachments", "Click on links to verify", "Delete it immediately", "Report it as spam and don't open attachments"],
            correctAnswer: 3
        },
        {
            question: "How often should you update your passwords?",
            options: ["Never", "Every few years", "Every 3-6 months", "Only when compromised"],
            correctAnswer: 2
        },
        {
            question: "What is encryption used for?",
            options: ["Speed up computer", "Protect data privacy", "Improve internet speed", "Clean hard drive"],
            correctAnswer: 1
        }
    ],
    medium: [
        {
            scenario: "You receive an email from your bank stating that your account will be locked unless you verify your credentials via a provided link.",
            description: "What should you do in this situation?",
            options: [
                "Click the link and enter your details immediately",
                "Ignore the email, as banks never send such requests",
                "Call the bank's official number to verify the email",
                "Forward the email to your friends for awareness"
            ],
            correctAnswer: 2
        },
        {
            scenario: "You find a USB drive in the office parking lot.",
            description: "What is the most secure action to take?",
            options: [
                "Plug it into your computer to find its owner",
                "Hand it to IT security team without plugging it in",
                "Share it with colleagues to check contents",
                "Format it and use it for yourself"
            ],
            correctAnswer: 1
        },
        {
            scenario: "Your colleague asks for your login credentials to access a system while you're on vacation.",
            description: "What's the appropriate response?",
            options: [
                "Share credentials since they're a trusted colleague",
                "Refuse and suggest they request proper access",
                "Share but ask them to change password after",
                "Give them only the username"
            ],
            correctAnswer: 1
        },
        {
            scenario: "You notice unusual network traffic from a company server at 3 AM.",
            description: "What should be your first action?",
            options: [
                "Shut down the server immediately",
                "Wait and check during business hours",
                "Alert the security team immediately",
                "Ignore as it might be routine maintenance"
            ],
            correctAnswer: 2
        },
        {
            scenario: "A coworker shares sensitive company data on their personal social media.",
            description: "What's the best course of action?",
            options: [
                "Comment on their post to remove it",
                "Report to HR and information security",
                "Message them privately about it",
                "Ignore as it's their personal account"
            ],
            correctAnswer: 1
        },
        {
            scenario: "Your system starts encrypting files automatically with a message demanding payment.",
            description: "What should you do first?",
            options: [
                "Pay the ransom immediately",
                "Disconnect from network and report to IT",
                "Try to decrypt files yourself",
                "Ignore and continue working"
            ],
            correctAnswer: 1
        },
        {
            scenario: "You receive a call from 'Microsoft Support' about your computer having issues.",
            description: "How should you handle this?",
            options: [
                "Follow their instructions to fix issues",
                "Provide them remote access",
                "Hang up and report the number",
                "Ask them for your computer details"
            ],
            correctAnswer: 2
        },
        {
            scenario: "A website asks to install a 'required' browser extension.",
            description: "What's the safest action?",
            options: [
                "Install it to access the site",
                "Research the extension first",
                "Decline and find alternative site",
                "Ask colleagues if they use it"
            ],
            correctAnswer: 2
        },
        {
            scenario: "You notice a colleague writing passwords on sticky notes.",
            description: "What should you do?",
            options: [
                "Remove the sticky notes",
                "Ignore it as it's not your concern",
                "Educate them about password managers",
                "Report them to management"
            ],
            correctAnswer: 2
        },
        {
            scenario: "Your phone receives a text about suspicious bank activity with a link.",
            description: "What's the best action?",
            options: [
                "Click the link to check",
                "Call your bank's official number",
                "Reply to the text for details",
                "Forward to friends as warning"
            ],
            correctAnswer: 1
        }
    ],
    hard: [
        {
            question: "Arrange the steps to secure a Wi-Fi network in the correct order:",
            options: [
                "Change the default admin password",
                "Enable WPA3 encryption",
                "Disable WPS (Wi-Fi Protected Setup)",
                "Hide the SSID (Wi-Fi Network Name)"
            ],
            correctAnswer: [0, 1, 2, 3]
        },
        {
            question: "Order the steps to respond to a data breach:",
            options: [
                "Identify the breach scope and impact",
                "Contain and stop the breach",
                "Notify affected parties",
                "Document the incident and update security"
            ],
            correctAnswer: [1, 0, 2, 3]
        },
        {
            question: "Arrange the steps for implementing two-factor authentication:",
            options: [
                "Enable 2FA in security settings",
                "Choose authentication method",
                "Back up recovery codes",
                "Test the new authentication"
            ],
            correctAnswer: [0, 1, 2, 3]
        },
        {
            question: "Order the steps for secure software installation:",
            options: [
                "Verify software source",
                "Check digital signatures",
                "Scan for malware",
                "Install in isolated environment"
            ],
            correctAnswer: [0, 1, 2, 3]
        },
        {
            question: "Arrange the incident response steps:",
            options: [
                "Detect and analyze",
                "Contain and eradicate",
                "Recover systems",
                "Post-incident review"
            ],
            correctAnswer: [0, 1, 2, 3]
        },
        {
            question: "Order the steps for secure password recovery:",
            options: [
                "Verify user identity",
                "Generate temporary access",
                "Force password change",
                "Log the recovery attempt"
            ],
            correctAnswer: [0, 1, 2, 3]
        },
        {
            question: "Arrange the steps for securing a new computer:",
            options: [
                "Install antivirus software",
                "Update operating system",
                "Configure firewall",
                "Set up user accounts"
            ],
            correctAnswer: [1, 0, 2, 3]
        },
        {
            question: "Order the steps for handling a malware infection:",
            options: [
                "Disconnect from network",
                "Boot in safe mode",
                "Run malware scan",
                "Clean or reinstall system"
            ],
            correctAnswer: [0, 1, 2, 3]
        },
        {
            question: "Arrange the steps for secure cloud migration:",
            options: [
                "Data classification",
                "Security assessment",
                "Encryption setup",
                "Access control configuration"
            ],
            correctAnswer: [0, 1, 2, 3]
        },
        {
            question: "Order the steps for secure device disposal:",
            options: [
                "Back up required data",
                "Encrypt entire device",
                "Perform secure erase",
                "Physically destroy if needed"
            ],
            correctAnswer: [0, 1, 2, 3]
        }
    ],
    extreme: [
        {
            question: "What does HTTPS stand for?",
            options: ["HyperText Transfer Protocol Secure", "High Transfer Protocol System", "HyperText Transfer Protection Service", "High Text Protocol Secure"],
            correctAnswer: 0
        },
        {
            question: "Which port is commonly used for HTTPS?",
            options: ["443", "80", "8080", "21"],
            correctAnswer: 0
        },
        {
            question: "What is a zero-day exploit?",
            options: ["New vulnerability with no patch", "Exploit that takes no time", "Free hacking tool", "Daily security scan"],
            correctAnswer: 0
        },
        {
            question: "What is SQL Injection?",
            options: ["Database backup", "Code insertion attack", "SQL server tool", "Data encryption"],
            correctAnswer: 1
        },
        {
            question: "What is AES?",
            options: ["Advanced Encryption Standard", "Automated Entry System", "Active Email Service", "Advanced Email Security"],
            correctAnswer: 0
        },
        {
            question: "What is a DMZ in networking?",
            options: ["Demilitarized Zone", "Direct Memory Zone", "Data Management Zone", "Dynamic Memory Zone"],
            correctAnswer: 0
        },
        {
            question: "What is CSRF?",
            options: ["Cross-Site Request Forgery", "Client Server Request Form", "Cascading Style Request Form", "Cross-Site Response Filter"],
            correctAnswer: 0
        },
        {
            question: "What protocol does SSH use?",
            options: ["TCP port 22", "UDP port 53", "TCP port 80", "UDP port 443"],
            correctAnswer: 0
        },
        {
            question: "What is a Honeypot?",
            options: ["Security trap", "Sweet data", "Encryption key", "Network tool"],
            correctAnswer: 0
        },
        {
            question: "What is the purpose of DNSSEC?",
            options: ["DNS Security Extensions", "Domain Name System", "DNS Server", "DNS Service"],
            correctAnswer: 0
        },
        {
            question: "What is MAC spoofing?",
            options: ["Faking hardware address", "Making new MAC", "MAC encryption", "MAC filtering"],
            correctAnswer: 0
        },
        {
            question: "What is a Buffer Overflow?",
            options: ["Memory boundary breach", "Full buffer", "Data overflow", "Stack memory"],
            correctAnswer: 0
        },
        {
            question: "What is MITM?",
            options: ["Man in the Middle", "Multiple Internet Transmission Mode", "Managed IT Management", "Mobile IT Management"],
            correctAnswer: 0
        },
        {
            question: "What is Kerberos?",
            options: ["Authentication protocol", "Antivirus software", "Encryption standard", "Firewall type"],
            correctAnswer: 0
        },
        {
            question: "What does CIA stand for in security?",
            options: ["Confidentiality, Integrity, Availability", "Central Intelligence Agency", "Computer Internet Access", "Cyber Intelligence Alliance"],
            correctAnswer: 0
        }
    ]
};

document.addEventListener('DOMContentLoaded', () => {
    setupLevelSelection();
});

function setupLevelSelection() {
    const levelCards = document.querySelectorAll('.level-card');
    levelCards.forEach(card => {
        card.addEventListener('click', () => {
            const level = card.dataset.level;
            currentLevel = level;
            loadQuizByLevel(level);
        });
    });
}

function loadQuizByLevel(level) {
    try {
        // Since we don't have a backend yet, we'll use our sample questions
        quizQuestions = questionsByLevel[level];
        userAnswers = new Array(quizQuestions.length).fill(null);
        document.getElementById('levelSelection').style.display = 'none';
        document.getElementById('quizContainer').style.display = 'block';
        
        if (level === 'extreme') {
            document.getElementById('timerContainer').style.display = 'block';
            startTimer();
        }
        
        displayQuestion(0);
        setupEventListeners();
    } catch (error) {
        console.error('Error loading quiz:', error);
    }
}

function displayQuestion(index) {
    const question = quizQuestions[index];
    const questionContainer = document.getElementById('questionContainer');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');

    document.getElementById('currentQuestion').textContent = index + 1;
    document.getElementById('totalQuestions').textContent = quizQuestions.length;

    prevBtn.disabled = index === 0;
    nextBtn.style.display = index === quizQuestions.length - 1 ? 'none' : 'flex';
    submitBtn.style.display = index === quizQuestions.length - 1 ? 'flex' : 'none';

    let questionHTML = '';
    
    switch(currentLevel) {
        case 'easy':
            questionHTML = createMCQQuestion(question, index);
            break;
        case 'medium':
            questionHTML = createScenarioQuestion(question, index);
            break;
        case 'hard':
            questionHTML = createDragDropQuestion(question, index);
            break;
        case 'extreme':
            questionHTML = createRapidFireQuestion(question, index);
            break;
    }

    questionContainer.innerHTML = questionHTML;
    setupQuestionInteractions(currentLevel, index);
}

function createMCQQuestion(question, index) {
    return `
        <div class="question">
            <div class="question-text">${index + 1}. ${question.question}</div>
            <div class="options">
                ${question.options.map((option, optionIndex) => `
                    <div class="option ${userAnswers[index] === optionIndex ? 'selected' : ''}" 
                         data-index="${optionIndex}">
                        ${option}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function createScenarioQuestion(question, index) {
    return `
        <div class="question">
            <div class="question-text">${index + 1}. ${question.scenario}</div>
            <div class="scenario-description">${question.description}</div>
            <div class="options">
                ${question.options.map((option, optionIndex) => `
                    <div class="option ${userAnswers[index] === optionIndex ? 'selected' : ''}" 
                         data-index="${optionIndex}">
                        ${option}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function createDragDropQuestion(question, index) {
    return `
        <div class="question">
            <div class="question-text">${index + 1}. ${question.question}</div>
            <div class="drag-drop-container" data-index="${index}">
                ${question.options.map((option, optionIndex) => `
                    <div class="drag-item" draggable="true" data-index="${optionIndex}">
                        ${option}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function createRapidFireQuestion(question, index) {
    return `
        <div class="question">
            <div class="question-text">${index + 1}. ${question.question}</div>
            <div class="options">
                ${question.options.map((option, optionIndex) => `
                    <div class="option ${userAnswers[index] === optionIndex ? 'selected' : ''}" 
                         data-index="${optionIndex}">
                        ${option}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function setupQuestionInteractions(level, index) {
    switch(level) {
        case 'easy':
        case 'medium':
        case 'extreme':
            setupMCQInteractions();
            break;
        case 'hard':
            setupDragDropInteractions(index);
            break;
    }
}

function setupMCQInteractions() {
    const options = document.querySelectorAll('.option');
    options.forEach(option => {
        option.addEventListener('click', () => {
            const optionIndex = parseInt(option.dataset.index);
            selectOption(optionIndex);
        });
    });
}

function setupDragDropInteractions(index) {
    const draggables = document.querySelectorAll('.drag-item');
    const container = document.querySelector('.drag-drop-container');

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', () => {
            draggable.classList.add('dragging');
        });

        draggable.addEventListener('dragend', () => {
            draggable.classList.remove('dragging');
            const newOrder = [...container.querySelectorAll('.drag-item')].map(item => 
                parseInt(item.dataset.index)
            );
            userAnswers[index] = newOrder;
        });
    });

    container.addEventListener('dragover', e => {
        e.preventDefault();
        const afterElement = getDragAfterElement(container, e.clientY);
        const draggable = document.querySelector('.dragging');
        if (afterElement) {
            container.insertBefore(draggable, afterElement);
        } else {
            container.appendChild(draggable);
        }
    });
}

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.drag-item:not(.dragging)')];
    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

function startTimer() {
    timeLeft = 120;
    updateTimerDisplay();
    timer = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();
        if (timeLeft <= 0) {
            clearInterval(timer);
            submitQuiz();
        }
    }, 1000);
}

function updateTimerDisplay() {
    document.getElementById('timer').textContent = timeLeft;
}

function selectOption(optionIndex) {
    userAnswers[currentQuestionIndex] = optionIndex;
    displayQuestion(currentQuestionIndex);
}

function setupEventListeners() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    const retakeBtn = document.getElementById('retakeBtn');

    prevBtn.addEventListener('click', () => {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion(currentQuestionIndex);
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentQuestionIndex < quizQuestions.length - 1) {
            currentQuestionIndex++;
            displayQuestion(currentQuestionIndex);
        }
    });

    submitBtn.addEventListener('click', () => {
        if (userAnswers.includes(null)) {
            alert('Please answer all questions before submitting.');
            highlightUnansweredQuestions();
            return;
        }
        submitQuiz();
    });

    retakeBtn.addEventListener('click', () => {
        if (timer) {
            clearInterval(timer);
        }
        document.getElementById('quizContainer').style.display = 'none';
        document.getElementById('levelSelection').style.display = 'grid';
        currentQuestionIndex = 0;
        userAnswers = [];
        quizQuestions = [];
        currentLevel = null;
    });
}

async function submitQuiz() {
    if (timer) {
        clearInterval(timer);
    }
    
    try {
        const result = calculateResults();
        displayResults(result);
    } catch (error) {
        console.error('Error submitting quiz:', error);
    }
}

function calculateResults() {
    let score = 0;
    let questionResults = [];
    
    quizQuestions.forEach((question, index) => {
        const userAnswer = userAnswers[index];
        let isCorrect = false;
        
        if (currentLevel === 'hard') {
            // For drag and drop, compare arrays
            isCorrect = JSON.stringify(userAnswer) === JSON.stringify(question.correctAnswer);
        } else {
            // For other question types
            isCorrect = userAnswer === question.correctAnswer;
        }
        
        if (isCorrect) {
            score++;
        }
        
        questionResults.push({
            question: question.question || question.scenario,
            userAnswer: userAnswer,
            correctAnswer: question.correctAnswer,
            isCorrect: isCorrect
        });
    });
    
    return {
        score: score,
        total: quizQuestions.length,
        timeTaken: currentLevel === 'extreme' ? 30 - timeLeft : undefined,
        questionResults: questionResults
    };
}

function displayResults(result) {
    const quizContainer = document.getElementById('quizContainer');
    const resultContainer = document.getElementById('resultContainer');
    
    quizContainer.querySelector('.quiz-content').style.display = 'none';
    resultContainer.style.display = 'block';
    
    const percentage = (result.score / result.total) * 100;
    
    let feedbackMessage = '';
    if (percentage >= 90) {
        feedbackMessage = 'Excellent! You\'re a cybersecurity expert!';
    } else if (percentage >= 70) {
        feedbackMessage = 'Great job! You have a solid understanding of cybersecurity.';
    } else if (percentage >= 50) {
        feedbackMessage = 'Good effort! Keep learning about cybersecurity.';
    } else {
        feedbackMessage = 'Keep studying! Review the topics you missed to strengthen your understanding.';
    }

    let questionReviewHTML = result.questionResults.map((qResult, index) => {
        let answerDisplay = '';
        if (currentLevel === 'hard') {
            // For drag and drop questions, show the order
            answerDisplay = `
                <div class="user-answer">Your order: ${qResult.userAnswer.map(i => qResult.question.options[i]).join(' → ')}</div>
                <div class="correct-answer">Correct order: ${qResult.correctAnswer.map(i => qResult.question.options[i]).join(' → ')}</div>
            `;
        } else {
            // For other question types
            const userAnswerText = qResult.userAnswer !== null ? 
                quizQuestions[index].options[qResult.userAnswer] : 
                'Not answered';
            const correctAnswerText = quizQuestions[index].options[qResult.correctAnswer];
            
            answerDisplay = `
                <div class="user-answer">Your answer: ${userAnswerText}</div>
                ${!qResult.isCorrect ? `<div class="correct-answer">Correct answer: ${correctAnswerText}</div>` : ''}
            `;
        }

        return `
            <div class="review-item ${qResult.isCorrect ? 'correct' : 'incorrect'}">
                <div class="question-number">Question ${index + 1}</div>
                <div class="question-text">${qResult.question}</div>
                <div class="answer-details">
                    ${answerDisplay}
                    <div class="result-icon">
                        <i class="fas ${qResult.isCorrect ? 'fa-check-circle' : 'fa-times-circle'}"></i>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    resultContainer.innerHTML = `
        <h2>Quiz Results</h2>
        <div class="score-container">
            <div class="score-circle">
                <span class="score-text">${percentage.toFixed(1)}%</span>
            </div>
            <div class="score-details">
                <p class="feedback">${feedbackMessage}</p>
                <p>Level: ${currentLevel.charAt(0).toUpperCase() + currentLevel.slice(1)}</p>
                <p>Correct Answers: ${result.score} out of ${result.total}</p>
            </div>
        </div>
        
        <div class="questions-review">
            <h3>Detailed Review</h3>
            ${questionReviewHTML}
        </div>
        
        <button id="retakeBtn" class="retry-btn">
            Try Another Level <i class="fas fa-redo"></i>
        </button>
    `;
    
    if (percentage >= 70) {
        createConfetti(100);
    }
    
    // Re-attach event listener to the new retake button
    document.getElementById('retakeBtn').addEventListener('click', () => {
        if (timer) {
            clearInterval(timer);
        }
        document.getElementById('quizContainer').style.display = 'none';
        document.getElementById('levelSelection').style.display = 'grid';
        currentQuestionIndex = 0;
        userAnswers = [];
        quizQuestions = [];
        currentLevel = null;
    });
}
