// Package Builder Configurator — Dynamic Pricing by Car Type & Goal Presets
document.addEventListener('DOMContentLoaded', () => {
    const configContainer = document.getElementById('package-builder-container');
    if (!configContainer) return;

    // ── Price table: prices[carType][serviceKey] ──────────────────────────────
    const PRICES = {
        hatchback: { coating: 8000,   ppf: 60000,  glass: 8000,  detailing: 6000  },
        sedan:     { coating: 12000,  ppf: 100000, glass: 12000, detailing: 8000  },
        crossover: { coating: 15000,  ppf: 130000, glass: 15000, detailing: 10000 },
        suv:       { coating: 20000,  ppf: 150000, glass: 20000, detailing: 13000 },
    };

    const CAR_LABELS = {
        hatchback: 'Hatchback',
        sedan:     'Sedan',
        crossover: 'Crossover',
        suv:       'Full-Size SUV',
    };

    // ── DOM refs ──────────────────────────────────────────────────────────────
    const carRadios     = configContainer.querySelectorAll('input[name="cfg_car"]');
    const paintOptions  = configContainer.querySelectorAll('input[name="cfg_paint"]');
    const glassCheck    = configContainer.querySelector('input[name="cfg_glass"]');
    const interiorCheck = configContainer.querySelector('input[name="cfg_interior"]');
    const goalCards     = configContainer.querySelectorAll('.cfg-goal-card');
    const listEl        = document.getElementById('cfg-summary-list');
    const priceEl       = document.getElementById('cfg-total-price');
    const waBtn         = document.getElementById('cfg-wa-btn');
    const carBadge      = document.getElementById('cfg-selected-car-badge');

    let activeGoal = 'gloss_suite';

    function getSelectedCar() {
        for (const r of carRadios) { if (r.checked) return r.value; }
        return 'hatchback';
    }

    function fmt(n) { return 'PKR ' + n.toLocaleString(); }

    // ── Update goal preset prices on car change ───────────────────────────────
    function updateGoalPrices(carType) {
        const p = PRICES[carType];
        goalCards.forEach(card => {
            const goal = card.getAttribute('data-goal');
            const priceSpan = card.querySelector('.cfg-goal-price');
            if (!priceSpan) return;

            let price = 0;
            if (goal === 'gloss_suite')    price = p.coating + p.glass + p.detailing;
            else if (goal === 'armor_ppf') price = p.ppf + p.glass + p.detailing;
            else if (goal === 'graphene_suite') price = p.coating + p.glass + p.detailing;
            else if (goal === 'paint_only') price = p.coating;
            else if (goal === 'detail_glass') price = p.glass + p.detailing;

            if (price > 0) {
                priceSpan.textContent = fmt(price);
            }
        });
    }

    // ── Update all visible individual module price labels ──────────────────────
    function updatePriceLabels(carType) {
        const p = PRICES[carType];
        configContainer.querySelectorAll('.cfg-price-label').forEach(span => {
            const key = span.getAttribute('data-for');
            if (!key || !p[key]) return;
            const isAddon = (key === 'glass' || key === 'detailing');
            span.textContent = isAddon ? '+ ' + fmt(p[key]) : fmt(p[key]);
        });
    }

    // ── Update car-type button highlight ──────────────────────────────────────
    function updateCarButtons(carType) {
        ['hatchback', 'sedan', 'crossover', 'suv'].forEach(ct => {
            const lbl = document.getElementById('car-label-' + ct);
            if (!lbl) return;
            const icon = lbl.querySelector('i');
            if (ct === carType) {
                lbl.style.background = 'rgba(255,30,39,0.14)';
                lbl.style.border     = '2px solid var(--red-z)';
                if (icon) icon.style.color = 'var(--red-z)';
            } else {
                lbl.style.background = 'rgba(10,11,14,0.6)';
                lbl.style.border     = '1px solid var(--border-color)';
                if (icon) icon.style.color = 'var(--text-muted)';
            }
        });

        if (carBadge) {
            carBadge.textContent = CAR_LABELS[carType].toUpperCase();
        }
    }

    // ── Highlight active goal preset card ─────────────────────────────────────
    function updateGoalCardStyles() {
        goalCards.forEach(card => {
            const g = card.getAttribute('data-goal');
            if (g === activeGoal) {
                card.style.background = 'rgba(255,30,39,0.12)';
                card.style.borderColor = 'var(--red-z)';
            } else {
                card.style.background = 'rgba(10,11,14,0.6)';
                card.style.borderColor = 'var(--border-color)';
            }
        });
    }

    // ── Apply Goal Preset selection to module checkboxes ───────────────────────
    function applyGoalPreset(goal) {
        activeGoal = goal;
        updateGoalCardStyles();

        if (goal === 'gloss_suite') {
            setPaintSelection('coating');
            if (glassCheck) glassCheck.checked = true;
            if (interiorCheck) interiorCheck.checked = true;
        } else if (goal === 'armor_ppf') {
            setPaintSelection('ppf');
            if (glassCheck) glassCheck.checked = true;
            if (interiorCheck) interiorCheck.checked = true;
        } else if (goal === 'graphene_suite') {
            setPaintSelection('graphene');
            if (glassCheck) glassCheck.checked = true;
            if (interiorCheck) interiorCheck.checked = true;
        } else if (goal === 'paint_only') {
            setPaintSelection('coating');
            if (glassCheck) glassCheck.checked = false;
            if (interiorCheck) interiorCheck.checked = false;
        } else if (goal === 'detail_glass') {
            setPaintSelection('none');
            if (glassCheck) glassCheck.checked = true;
            if (interiorCheck) interiorCheck.checked = true;
        }

        updateConfigurator();
    }

    function setPaintSelection(val) {
        paintOptions.forEach(opt => {
            opt.checked = (opt.value === val);
        });
    }

    // ── Recalculate bundle total & items ──────────────────────────────────────
    function updateConfigurator() {
        const carType = getSelectedCar();
        const p = PRICES[carType];
        let total = 0;
        const items = [];

        paintOptions.forEach(opt => {
            if (opt.checked) {
                const key = opt.getAttribute('data-key');
                if (key !== 'none' && p[key]) {
                    total += p[key];
                    items.push(opt.getAttribute('data-name'));
                }
            }
        });

        if (glassCheck && glassCheck.checked) {
            total += p['glass'] || 0;
            items.push(glassCheck.getAttribute('data-name'));
        }

        if (interiorCheck && interiorCheck.checked) {
            total += p['detailing'] || 0;
            items.push(interiorCheck.getAttribute('data-name'));
        }

        if (items.length === 0) {
            items.push('No modules selected (Custom)');
        }

        if (listEl) {
            listEl.innerHTML = items.map(i =>
                `<li style="padding:4px 0; color:#fff; display:flex; align-items:center; gap:8px;">
                    <i class="fa-solid fa-check" style="color:var(--red-z); font-size:0.8rem;"></i>
                    <span>${i}</span>
                </li>`
            ).join('');
        }

        if (priceEl) priceEl.textContent = fmt(total);

        if (waBtn) {
            const carLabel = CAR_LABELS[carType];
            const pkgStr   = items.join(' + ');
            waBtn.href = `https://wa.me/923024577493?text=Hi%20AutozCraveStudio!%20I%20built%20a%20package%20for%20my%20${encodeURIComponent(carLabel)}:%20${encodeURIComponent(pkgStr)}%20-%20Starting%20from%20${encodeURIComponent(fmt(total))}.%20Can%20I%20get%20an%20exact%20quote%20and%20schedule%20an%20inspection?`;
        }
    }

    // ── On car type change ───────────────────────────────────────────────────
    function onCarChange() {
        const carType = getSelectedCar();
        updateCarButtons(carType);
        updateGoalPrices(carType);
        updatePriceLabels(carType);
        updateConfigurator();
    }

    // Attach listeners
    carRadios.forEach(r => r.addEventListener('change', onCarChange));

    goalCards.forEach(card => {
        card.addEventListener('click', () => {
            const goal = card.getAttribute('data-goal');
            applyGoalPreset(goal);
        });
    });

    configContainer.querySelectorAll('input[name="cfg_paint"], input[name="cfg_glass"], input[name="cfg_interior"]')
        .forEach(inp => inp.addEventListener('change', () => {
            activeGoal = 'custom';
            updateGoalCardStyles();
            updateConfigurator();
        }));

    // ── Initial render ────────────────────────────────────────────────────────
    onCarChange();
    applyGoalPreset('gloss_suite');
});

