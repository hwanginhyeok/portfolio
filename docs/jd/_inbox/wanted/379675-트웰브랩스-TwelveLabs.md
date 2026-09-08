---
wanted_id: 379675
company: "트웰브랩스(TwelveLabs)"
position: "Senior ML Research Scientist, Jockey Core"
url: "https://www.wanted.co.kr/wd/379675"
location: "서울시 용산구 이태원로 27길 39-11"
skill_tags: ["GitHub", "MongoDB", "PyTorch", "Redis", "Python", "AWS", "Go", "Docker", "ElasticSearch", "RabbitMQ", "Golang", "Kubernetes"]
track: "ai-native"
search_lane: "ai-native"
search_lanes: ["ai-native"]
due_time: null
first_seen: "2026-08-31"
matched_keywords: ["로보틱스"]
---

## 소개

* Who we are
Video is 90% of the world's data. Most of it is invisible to machines.
TwelveLabs builds the intelligence layer to change that. Our multimodal AI models understand video the way humans do — across sight, sound, and motion — and power production-scale AI workloads across media, entertainment, sports, security, and government.

We have raised more than $210 million from NEA, Radical Ventures, Amazon, NVIDIA, Snowflake, Databricks, Index Ventures, NAVER Ventures, Korea Investment Partners, Quadrille Capital, Red Bull Ventures, and AI pioneers including Fei-Fei Li, Silvio Savarese, and Alexandr Wang.

We are a global company, headquartered in San Francisco with offices in Seoul, New York, and London, and employees around the world. We believe the differences in our cultural, educational, and life experiences make our products stronger. Building technology that understands the world in all its complexity requires people who see it from every angle. We are looking for individuals who are driven by hard problems and want their work to matter. Come build it with us!

* About Jockey
Jockey is TwelveLabs' unified agentic system that reasons across your videos and images. It combines a reasoning model with a memory layer that builds a knowledge store from your corpus.

No context window holds a video archive. We work at a million hours of video. A single model forward pass can tell you about one file; it can't reason across a corpus, and no context window closes that gap. Jockey decomposes a query, retrieves, segments, and reasons across thousands of videos and images. Point it at an archive, ask for a highlight reel or the best viral moments, and it returns timestamped cuts you can use. Corpus-level understanding you can act on is the whole product.

Built for agents, not just people. As AI agents increasingly become the primary consumers of video, we're building production-grade infrastructure that scales to millions of hours while delivering reliable, high-quality results for both human users and autonomous agents.

We build on models we own. Marengo, our embedding model, resolves a query like "the moment we almost missed the flight" into real retrieval. Pegasus, our video-language model, returns structured, timestamped moments on a schema you define. We ship and improve both continuously, so Jockey's quality compounds with every release — no re-integration for customers. Few teams get to build an agent on a stack they control end to end.

Deep expertise, one system, open culture. Foundation models, knowledge construction, search, and the agent harness all live in one org. Each team owns its domain and is expected to have deep expertise in it — but like a Formula 1 team, we optimize for the global system, not local parts. A model gain that doesn't expand what the agent can do isn't a gain. We trace a single algorithm change through to end-system behavior, and share work in progress weekly, not just finished results. Anyone can pull the context they need from any team.

* About the team
The Cognition Models team owns the models that turn video into structured understanding and reasoning: Pegasus, our video-language model, and Jockey Core, the reasoning LLM behind Jockey. In the model stack we sit between Perception Models (embeddings and retrieval) and the agent system — taking what's retrieved and producing structured understanding and the reasoning to act on it.

We focus on multimodal systems with high instruction-following capability and complex, hierarchically structured outputs. Our work spans training infrastructure from pre-training to RL, temporal segmentation and structured metadata extraction, large-scale inference and serving systems, data-curation and evaluation pipelines, and building Jockey Core. We ship products with real-world value rather than doing research in isolation, working as a goal-oriented, cross-functional team of ML researchers and engineers — using the most advanced compute in the world, including NVIDIA B300s, to accelerate the research-to-production cycle.

* About Jockey Core
Jockey Core is the reasoning LLM at the center of Jockey — the model that decomposes a query, decides what to retrieve and segment, and reasons over the results into an answer you can act on. It sits in the critical path of every agent step, so its quality, latency, and cost directly shape what Jockey can do. Jockey Core is a model we own and serve end to end, and we improve it continuously so Jockey's quality compounds with every release.

## 주요업무

• This role leads model-efficiency and post-training research for Jockey Core — making a high-quality reasoning model efficient enough to serve in production without losing what makes it good.
• Drive model compression and efficiency research — structured pruning, quantization (PTQ/QAT), distillation, and recovery fine-tuning — building reasoning models that keep their quality at a production-efficient size.
• Design rigorous evals on the agent's real reasoning and tool-calling behavior, replaying real traffic rather than generic benchmarks.
• Explore post-training (SFT/RL) to preserve or improve agentic tool-use, and train draft models for speculative decoding where it helps.
• Work closely with serving engineers so efficiency gains become real cost and latency wins, and use your findings to set research direction.

## 자격요건

• Strong LLM research experience — post-training (SFT/RL), model compression, distillation, or efficient inference.
• A track record of independently driving research from ideation to execution, with strong experimental judgment (eval design, rigorous ablations, clear empirical conclusions).
• Strong proficiency in Python and PyTorch.
• The ability to communicate and collaborate closely with both researchers and engineers.

## 우대사항

• Hands-on experience pruning, quantizing, or distilling large models, and an understanding of how compression affects reasoning/agentic behavior.
• Experience with large-scale distributed training in high-performance GPU environments.
• Experience translating research advances into production ML systems.
• A Master's/PhD in Machine Learning, Computer Science, or a related technical field.

## 혜택

• 글로벌 고객과 함께 성장하는 글로벌 팀
• 자율성과 협업을 모두 갖춘 하이브리드 근무
• 전 직원에게 맥북 및 70만원 상당 재택근무 장비 지원, 3년 주기로 최신 장비 교체
• 식사·교통비 등 자유롭게 사용할 수 있는 월 60만 원 한도 법인카드 제공
• 사무실 내 스낵바(간식, 커피, 신선식품 제공)
• 연말 2주간 겨울 방학 운영
• 연 1회 건강검진 지원
• 영어 교육 프로그램 지원
