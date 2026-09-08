---
wanted_id: 372973
company: "슈퍼브에이아이(Superb AI)"
position: "Simulation Engineer"
url: "https://www.wanted.co.kr/wd/372973"
location: "서울 강남구 테헤란로 427"
skill_tags: ["Python", "AWS", "데이터 분석", "인공 지능", "컴퓨터 비전"]
track: "ai-native"
search_lane: "ai-native"
search_lanes: ["ai-native"]
due_time: null
first_seen: "2026-08-24"
matched_keywords: ["simulation engineer"]
---

## 소개

[포지션 소개]
Superb AI의 Simulation Engineer는 다양한 로봇·센서·태스크 조합에 대해 양질의 대규모 데이터를 얻을 수 있도록, GPU에서 수많은 환경을 병렬화하는 시뮬레이션 프레임워크를 구축합니다. 이 프레임워크는 RL 기반 정책 학습(locomotion, manipulation)에 활용되는 한편, 다양한 로봇 AI 모델의 배포 전 검증에도 쓰이며, 궁극적으로 Superb AI의 RFM·WFM 학습에 기여합니다.

[이 포지션의 매력]
• Founding Role로 사족로봇, 로봇팔, 휴머노이드에 적용할 수 있는 Physical AI의 시뮬레이션 프레임워크를 설계하고 구축합니다.
• FR3, Piper, G1, Go2 등 확보된 로봇 자산과 실험 공간을 제공합니다.
• 문제 정의부터 시스템 설계, 프레임워크 아키텍처, 도구 선택, 협업 방식까지 큰 자율성을 갖고 일합니다.
• 3D / 영상관제 / 데이터 역량과 결합된 새로운 Physical AI Application을 만들 수 있습니다.

## 주요업무

[시뮬레이션 프레임워크 설계]
• 로봇·센서·태스크를 모듈식으로 조합하는 환경 API(Gymnasium 등)를 설계하고, 새로운 로봇 기종·도메인에 손쉽게 대응할 수 있는 플러그인 구조를 만듭니다.
• Isaac Sim·Isaac Lab·Omniverse, MuJoCo(MJX) 등 백엔드를 추상화하여, 다양한 도메인의 시나리오로 빠르게 확장 가능한 사내 시뮬레이션 인프라를 구축합니다.

[동역학·제어·장면/에이전트 모델링]
• Manipulation, locomotion 등 contact-rich 태스크의 동역학·제어(IK, OSC, 궤적 생성 등)와 actuator 모델을 구성하고 관련 시나리오를 만듭니다.
• ego 로봇뿐 아니라 군집 로봇의 협응, 보행자·군중 거동, 동적 장애물로 채워진 대규모 장면을 구성하고, 다른 agent의 behavior·policy를 모델링해 현실적인 상호작용 시나리오를 만듭니다.
• IMU·F/T·LiDAR·proprioception 등 센서의 노이즈·신호 특성과 통신 지연을 시뮬레이터에서 재현합니다.

[GPU 병렬화 및 RL 환경 통합]
• Isaac Lab tensor API·MJX·Warp 등으로 수만 개의 환경을 병렬화하고, 병목을 규명해 throughput(steps/sec) 등 성능 지표를 최적화합니다.
• RSL-RL·TorchRL·SKRL 등 RL 프레임워크와 통합하고, 실제로 정책을 학습시켜 환경의 정합성과 reward 설계를 검증합니다.

[대규모 합성데이터 및 동역학 정렬]
• 질량·관성·마찰 등에 대한 동역학 수준의 도메인 랜덤화를 수행하고, sim-to-real dynamics gap을 정량화·개선합니다.
• ROS 2 bridge 등을 활용한 Real-to-Sim·system identification으로 실로봇 동역학을 시뮬레이터에 정렬합니다.
• cuRobo·MimicGen·scripted 방식 등으로 데모를 자동 생성하여, 수십억 env-steps 규모의 로봇 학습 데이터를 구축합니다.
• Omniverse Replicator 등으로 pixel-perfect ground-truth(segmentation, 2D/3D detection, depth 등)와 multi-camera 일관 ID(MTMC) 라벨을 자동 생성해, perception·영상관제 모델용 합성 데이터를 대규모로 만듭니다.
• 데이터 커버리지·다양성 등 품질 지표를 측정해 ML 모델 학습에 곧바로 쓸 수 있는 데이터를 제공합니다.

## 자격요건

AI·Computer Science·Robotics 등 유관 분야 학위가 있거나 그에 상응하는 경험이 있는 분
• Robotics·Simulation 관련 3년 이상 실무 경험이 있는 분
• Isaac Sim·Isaac Lab·MuJoCo 등 로봇 시뮬레이터 기반 개발 및 통합 경험이 있는 분
• GPU 병렬 RL 환경 또는 대규모 병렬 시뮬레이션 구축 경험이 있는 분 (Isaac Lab·MJX·Warp 등)
• 제어 실무(IK·OSC 등)와 궤적 생성·충돌 회피 경험이 있는 분
• Dynamics gap 분석·디버깅과 domain randomization 실무 경험이 있는 분
• Linux 개발 환경(Docker, Git 등) 및 ROS 2 기반 시스템 개발 경험이 있는 분

## 우대사항

오픈소스 로봇 시뮬레이션 프레임워크·RL 환경을 직접 설계·구축하거나 기여한 경험이 있는 분 (Isaac Lab, ManiSkill, RoboSuite 등)
JAX·NVIDIA Warp·CUDA 등으로 물리 시뮬레이션을 가속하거나 물리엔진 내부(MuJoCo·PhysX 등)를 확장한 경험이 있는 분
• 대규모 장면(군집 로봇, 군중·동적 장애물 등) 또는 멀티에이전트 RL 환경(PettingZoo 등) 구축한 경험이 있는 분
• 사족로봇·휴머노이드 locomotion·navigation RL 시뮬레이션 경험 또는 AMR·차량 동역학 모델링 경험이 있는 분
• 보행자·군중 시뮬레이션 및 agent behavior 모델링 경험이 있는 분 (social-force, ORCA 등)
• 물리 기반 시뮬레이션 연구 경험이 있는 분 (whole-body control, MPC, system identification 등)
• VLA 또는 RFM/WFM 모델(GR00T, Cosmos 등)을 시뮬레이터에 통합한 경험이 있는 분
• Omniverse Replicator 등으로 perception 모델 학습용 synthetic data를 ground-truth와 함께 구축한 경험이 있는 분

## 혜택

[업무 효율을 극대화하는 유연한 근무 제도]
• 코어타임(10:00~17:00) 기반의 자율 근무제
• 재택 근무와 사무실 근무를 병행하는 하이브리드 근무제

[구성원의 성장을 돕는 성장 지원 프로그램]
• 도서 구입, 강의 수강, 운동, 전자기기 구매에 필요한 자기계발비 지원 (월 10만원)
• 노하우 공유 혹은 지식 습득을 위한 사내 점심 스터디 모임 지원
• 성장을 위한 내부 컨퍼런스 및 교육 프로그램 수시 진행

[회사와 함께 성장하는 평가 및 보상 제도]
• 기존 경력 및 연차가 아닌 성과와 역량에 따른 보상 및 승진 제도 운영
• 연간 성과에 따른 스톡옵션 부여
• 분기별 성장 리뷰를 통한 정기적 피드백 및 1:1 진행

[구성원의 건강과 휴식, 생활을 지원해 드립니다!]
• 눈치 보지 않고 리더 승인 없이 자유로운 휴가 사용
• 근로기준법을 준수한 각종 법정 휴가 지원
• 법으로 지정되지 않는 신정, 근로자의 날, 현충일이 공휴일인 경우 특별 휴가 지원
• 부득이하게 휴일에 근무하는 경우 보상휴가 제공
• 야간 근무 시 저녁 식대 및 심야 시간 귀가를 위한 택시 비용 지급
• 근속 매 3년 마다 10일의 리프레시(Refresh) 휴가 및 휴가비 지원
• 매년 본인 및 가족 1인 종합 건강 검진 지원
• 근무일과 본인 휴가일에도 사용 가능한 점심 식대 지급
• 경조휴가 및 경조비 지원
• 명절(설/추석) 선물 지급
• 중소기업 청년 소득세 감면 혜택 적용 가능
• 청년내일채움공제 가입 가능

+ 더 자세한 회사 및 팀 소개, 복리후생은 슈퍼브에이아이 채용 페이지를 확인해주시기 바랍니다.
