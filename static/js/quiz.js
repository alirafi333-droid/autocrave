// "Find Your Protection" Enhanced Interactive Quiz Logic
document.addEventListener('DOMContentLoaded', () => {
    const quizContainer = document.getElementById('protection-quiz-container');
    if (!quizContainer) return;

    let currentStep = 1;
    const totalSteps = 4;
    const answers = {};

    const stepElements = quizContainer.querySelectorAll('.quiz-step');
    const prevBtn = document.getElementById('quiz-prev-btn');
    const nextBtn = document.getElementById('quiz-next-btn');
    const navControls = document.getElementById('quiz-nav-controls');
    const resultBox = document.getElementById('quiz-result-box');
    const stepIndicator = document.getElementById('quiz-step-indicator');
    const progressBar = document.getElementById('quiz-progress-bar');
    const restartBtn = document.getElementById('quiz-restart-btn');

    function updateStepView() {
        stepElements.forEach((el, index) => {
            if (index + 1 === currentStep) {
                el.style.display = 'block';
            } else {
                el.style.display = 'none';
            }
        });

        if (stepIndicator) {
            stepIndicator.innerText = `Question ${currentStep} of ${totalSteps}`;
        }

        const progressPercent = (currentStep / totalSteps) * 100;
        if (progressBar) progressBar.style.width = `${progressPercent}%`;

        if (prevBtn) prevBtn.style.display = currentStep > 1 ? 'inline-flex' : 'none';
        if (nextBtn) {
            nextBtn.innerHTML = currentStep === totalSteps ? 
                'See Recommendation <i class="fa-solid fa-wand-magic-sparkles"></i>' : 
                'Next Question <i class="fa-solid fa-arrow-right"></i>';
        }

        if (navControls) navControls.style.display = 'flex';
        if (resultBox) resultBox.style.display = 'none';
    }

    // Option selection + auto-advance
    quizContainer.querySelectorAll('.quiz-option').forEach(option => {
        option.addEventListener('click', () => {
            const stepEl = option.closest('.quiz-step');
            const stepNum = parseInt(stepEl.getAttribute('data-step'), 10);
            const value = option.getAttribute('data-value');

            stepEl.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
            option.classList.add('selected');

            answers[`step_${stepNum}`] = value;

            // Smooth auto-advance after 220ms
            setTimeout(() => {
                if (currentStep < totalSteps) {
                    currentStep++;
                    updateStepView();
                } else {
                    calculateRecommendation();
                }
            }, 220);
        });
    });

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            if (!answers[`step_${currentStep}`]) {
                alert('Please select an option to proceed to the next step.');
                return;
            }

            if (currentStep < totalSteps) {
                currentStep++;
                updateStepView();
            } else {
                calculateRecommendation();
            }
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentStep > 1) {
                currentStep--;
                updateStepView();
            }
        });
    }

    if (restartBtn) {
        restartBtn.addEventListener('click', () => {
            currentStep = 1;
            quizContainer.querySelectorAll('.quiz-option').forEach(o => o.classList.remove('selected'));
            for (let k in answers) delete answers[k];
            updateStepView();
        });
    }

    function calculateRecommendation() {
        stepElements.forEach(el => el.style.display = 'none');
        if (navControls) navControls.style.display = 'none';
        if (progressBar) progressBar.style.width = '100%';
        if (stepIndicator) stepIndicator.innerText = 'Custom Recommendation Ready';

        const vehicle = answers.step_1 || 'sedan';
        const usage   = answers.step_2;
        const parking = answers.step_3;
        const concern = answers.step_4;

        let recTitle = "Ceramic / Graphene / Glass Coating";
        let recDesc  = "A perfect balance of deep mirror gloss, hydrophobic water-sheeting, and UV defense tailored for Lahore weather conditions.";
        let estPrice = "PKR 12,000";

        if (vehicle === 'hatchback') {
            if (concern === 'chips' || usage === 'track') {
                recTitle = "Self-Healing PPF Protection (Hatchback)";
                recDesc  = "Your hatchback faces high highway gravel and road debris exposure. Self-healing TPU film provides unmatched physical armor against stone chips and scratches.";
                estPrice = "Starting from PKR 60,000";
            } else {
                recTitle = "Ceramic / Graphene / Glass Coating (Hatchback)";
                recDesc  = "Delivers stunning liquid gloss, hydrophobic dirt repellency, and UV protection — the ideal premium coating for a hatchback.";
                estPrice = "Starting from PKR 8,000";
            }
        } else if (vehicle === 'sedan' || vehicle === 'coupe') {
            if (concern === 'chips' || usage === 'track') {
                recTitle = "Self-Healing PPF Protection (Sedan / Coupe)";
                recDesc  = "High-grade TPU paint protection film protects your front bumper, bonnet, fenders, and side panels from stone chips, scratches, and swirl marks.";
                estPrice = "Starting from PKR 100,000";
            } else {
                recTitle = "Ceramic / Graphene / Glass Coating (Sedan / Coupe)";
                recDesc  = "Full multi-stage paint correction followed by 9H/10H ceramic coating for mirror reflection, hydrophobic water-beading, and UV defense.";
                estPrice = "Starting from PKR 12,000";
            }
        } else if (vehicle === 'crossover') {
            if (concern === 'chips' || usage === 'track') {
                recTitle = "Self-Healing PPF Protection (Crossover)";
                recDesc  = "Heavy-duty TPU protection film shielding your crossover against scratches, highway stone chips, and daily road abrasion.";
                estPrice = "Starting from PKR 130,000";
            } else {
                recTitle = "Ceramic / Graphene / Glass Coating (Crossover)";
                recDesc  = "Full exterior coating providing intense candy gloss, easy wash maintenance, and protection against chemical contaminants.";
                estPrice = "Starting from PKR 15,000";
            }
        } else if (vehicle === 'suv') {
            if (concern === 'chips' || usage === 'track') {
                recTitle = "Self-Healing PPF Armor (Full-Size SUV)";
                recDesc  = "Maximum physical armor shielding full SUV body panels from heavy stone chips, bush scratches, and daily environmental wear.";
                estPrice = "Starting from PKR 150,000";
            } else {
                recTitle = "Ceramic / Graphene / Glass Coating (Full-Size SUV)";
                recDesc  = "Large-surface multi-layer ceramic/graphene coating armor with hydrophobic windshield treatment and deep paint enhancement.";
                estPrice = "Starting from PKR 20,000";
            }
        } else if (vehicle === 'supercar') {
            recTitle = "Full-Body PPF Armor + 10H Graphene Coating";
            recDesc  = "Exotics and high-value performance cars require zero compromise. Self-healing TPU PPF shields every inch, topped with 10H Graphene for maximum thermal resistance and gloss.";
            estPrice = "Starting from PKR 150,000+";
        }

        const titleEl = document.getElementById('rec-title');
        const descEl  = document.getElementById('rec-desc');
        const priceEl = document.getElementById('rec-price');
        const waLink  = document.getElementById('rec-wa-link');

        if (titleEl) titleEl.innerText = recTitle;
        if (descEl)  descEl.innerText  = recDesc;
        if (priceEl) priceEl.innerText = estPrice;
        if (waLink) {
            waLink.href = `https://wa.me/923024577493?text=Hi%20AutozCraveStudio!%20I%20completed%20your%20Protection%20Quiz%20and%20got%20recommended:%20${encodeURIComponent(recTitle)}.%20Price:%20${encodeURIComponent(estPrice)}.`;
        }

        if (resultBox) resultBox.style.display = 'block';
    }

    updateStepView();
});
