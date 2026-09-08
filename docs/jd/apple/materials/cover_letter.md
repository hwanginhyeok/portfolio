# Cover Letter — Inhyeok Hwang
# Apple Korea · Reliability Engineer, Core Technology Operations (Job ID 200656459-3631)

> Version: 2026-09-07 v5 (rebuilt on the updated foundation: tenure 3 → 3.5 years; new paragraph on the RS500 simulation stack as usage-model-driven testing — the "field product usage model" responsibility now has a hands-on example, not only the Solar Energy damage-summation paper. v4 decisions kept: SVM attribution split, machine-learning paragraph, no LLM tooling in the letter, optics gap stated plainly.)
> Word count: ~520 words (body)

---

Dear Apple Core Technology Operations Team,

My graduate research at Konkuk University's **Reliability-Based Design Optimization (RBDO) Lab** was not a side topic — it was the focus of my master's program. Over two years I worked on accelerated life testing, prognostics, and failure-mode characterization of electric drivetrains, contributing through my thesis on IPMSM fault-diagnosis simulation and a government-funded PHM SoC project. I received the 2022 Best Paper Award from the Korean Society for Reliability and contributed as co-author to three peer-reviewed publications (IEEE Transactions on Instrumentation and Measurement · Journal of Power Electronics · Solar Energy, all 2024).

What distinguishes my profile is the bridge between that academic foundation and production reality. Over three and a half years at GINT Corp. I led GT-SS500 — a 48 V autonomous agricultural sprayer — through APQP Phase 2–3, authoring DFMEA Step 1–7 and applying ISO 25119 AgPL risk assessment (over-charge protection rated AgPL d). I closed four root-cause analyses on real field issues — MCB electrolytic carbonization, a state-machine safety bug, a pump O-ring freeze in low-temperature operation, and ground-bounce noise on the control bus — and tracked 27 NCRs through closure in a closed-loop corrective action process with Cpk-based IQC criteria. I also built four custom test rigs in-house: dynamometer torque control (nonlinearity 0.008%), fan bench (+57% airflow), pump bench, and bumper safety rig. This is what "production-stage execution" means to me — not running existing procedures, but building the infrastructure and closing the loop when things go wrong.

On the semiconductor side, I co-authored (third author) a programmable online bond-wire fault detection and location method for IGBT modules using inverter output parameters, published in IEEE Transactions on Instrumentation and Measurement (2024, DOI 10.1109/TIM.2024.3472910). My collaboration on identifying failure modes in IPMSM under accelerated life testing through a dual-sensor architecture appeared in the Journal of Power Electronics (2024, sixth author, DOI 10.1007/s43236-024-00810-8). Both projects relied on the same core practice — instrumenting multi-sensor signals to locate degradation modes before they manifest as failures — which is the practice I would bring to component-reliability work at Apple.

A connected strength: I have direct experience contributing to a machine learning pipeline for reliability problems. My thesis and the associated government-funded PHM SoC project (MOTIE, 2021–2022) combined physics-based simulation — a co-simulated digital twin of a 120 kW IPMSM using Ansys Maxwell FEM and MATLAB/Simulink — with an SVM-based fault classifier on phase-current signatures to diagnose demagnetization and winding-fault modes. The team built the SVM classifier; my contribution was the co-simulation that generated the labeled training data and the underlying motor and fault models. The approach is physics-informed ML: use the physical model to understand failure modes, then train a classifier to track deviation from it in real sensor streams.

I keep practicing that habit outside work. This year I built an open-source physics simulation of the same vehicle class (github.com/hwanginhyeok/physical_AI_rs500) so that usage scenarios could be exercised before hardware time: motor-driver protection logic modeled as failure modes, a scenario runner sweeping three mission profiles across five terrain types, a parameter-sensitivity report for each physical block, and 497 automated tests under continuous integration. It is the same reasoning as a field product usage model feeding an accelerated test plan — decide which stress factors matter by sweeping them, then spend hardware time only where the model says it counts.

The optics domain is the real gap in my background, and I want to be direct about it. I have not worked on cameras, VCMs, or lens assemblies; what I bring is graduate research in reliability, three and a half years of production-stage execution on different components, and the working assumption that the same methodology — DFMEA, root-cause analysis, ALT, multi-sensor signal processing, NCR close-out — is what carries between domains. Apple's Core Technology Operations team works at a scale and rigor of failure-analysis feedback loops that is unlike anything in my current industry. That is exactly where I want to work, and I would welcome the chance to discuss how my background fits.

Sincerely,
**In-hyeok Hwang**
dlsgur5560@gmail.com
hwanginhyeok.github.io/portfolio
