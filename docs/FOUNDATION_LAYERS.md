> **English:** [FOUNDATION_LAYERS_EN.md](FOUNDATION_LAYERS_EN.md)

# MPK 기초 레이어 맵

이 문서는 `MemoryPhase_Kernel`을 **완성형 보안 제품**으로 설명하지 않고,  
앞으로 확장 가능한 **기초 공사 레이어**로 설명하기 위한 문서다.

핵심 개념은 단순하다.

- 데이터는 기본적으로 **물(liquid)** 이다.
- 사용자가 맞다고 충분히 판단되면 데이터는 **얼음(frozen)** 처럼 정렬된다.
- 사용자가 떠나거나 신뢰가 무너지면 다시 **물**로 돌아간다.

즉 MPK는 파일을 그냥 “열고 닫는” 것이 아니라,  
**정보가 의미 있게 읽히는 상태를 제어하는 커널**이다.

## 레이어 개요

### Layer 0 — Raw State Vault

역할:

- 개인 정보, 운영 로그, 판단 결과를 기본적으로 `liquid` 상태로 저장
- raw 데이터와 해석 가능한 데이터 표현을 분리
- 사용자 없이도 데이터는 존재하지만, 바로 개인 의미를 드러내지 않음

현재 상태:

- 실제 저장소/복호 계층은 여전히 외부 책임
- 하지만 패키지 안에 `raw_vault.py` 최소 스캐폴딩이 추가됨
- materialize 시 `collapse_score` 임계도 함께 볼 수 있음

### Layer 1 — Identity Memory Engine

역할:

- 사용자를 “기억”하는 장기 프로필
- 채널별 중요도, 장기 경향, 신뢰 이력 보관

예시 채널:

- typing
- voice
- face
- language
- gaze
- device

현재 상태:

- `IdentityProfile`이 최소 구조를 제공
- `memory_store.py`가 누적 저장소 스캐폴딩을 제공
- 현재는 **가중치 슬롯 중심**
- 진짜 장기 학습/적응형 기억 엔진은 아직 아님
- `forgetting` / `drift penalty`의 최소 규칙은 포함됨

### Layer 2 — Continuous Identity Scoring

역할:

- 현재 입력과 장기 기억을 비교
- “지금 이 사람이 기억된 사용자와 얼마나 같은가” 계산

현재 상태:

- `compute_resonance_index()`
- `score_frame()`

산출:

- `resonance_index`
- `identity_score`
- quality / drift / intrusion 힌트

### Layer 3 — Access Dynamics Layer

역할:

- 저장된 기억과 현재 입력이 시간에 따라 어떻게 수렴하는지 계산
- `대칭 -> 진동 -> 감쇠 -> 공명 -> 붕괴` 흐름을 수학 레이어로 표현
- 단일 점수 판정보다 더 안정적인 연속 인증 흐름 제공

현재 상태:

- `dynamics.py`
- `compute_symmetry_score()`
- `compute_oscillation_score()`
- `compute_damping_score()`
- `compute_resonance_gain()`
- `compute_collapse_score()`
- `evolve_phase_dynamics()`

핵심 해석:

- 대칭: 기억과 현재 사용자의 구조적 정렬
- 진동: 최근 틱에서의 흔들림
- 감쇠: 노이즈가 줄어드는 정도
- 공명: 안정적인 사용자 일치가 형성되는 정도
- 붕괴: 최종적으로 접근 결정을 내릴 수 있을 정도로 상태가 수렴하는 정도

### Layer 4 — Phase Transition Controller

역할:

- 점수와 정책에 따라 `liquid / semi_frozen / frozen` 위상 전이
- 침입, 유휴, 드리프트 시 강등

현재 상태:

- `phase_from_identity_score()`
- `build_access_decision()`
- `should_re_melt()`

이 레이어가 실제로 하는 일은:

- “보여줄까?”보다
- **“의미 있게 정렬할까?”** 를 결정하는 것

### Layer 5 — Access Kernel

역할:

- 위상에 따라 민감도 티어를 결정
- 어떤 정보층까지 읽을 수 있는지 정책화

현재 상태:

- `AccessDecision.phase`
- `AccessDecision.allowed_tiers`

예상 연결 대상:

- Atom 상태 요약
- Athena 분석 결과
- Pharaoh 보고서
- 운영 로그
- 개인 메모리

### Layer 6 — Audit / Forgetting / Re-melt

역할:

- 세션 종료, 사용자 이탈, 침입, 유휴 시 재용해
- 해석 창 닫기
- 세션 키 폐기, 감사 기록 남기기

현재 상태:

- `ReMeltEvent`
- `should_re_melt()`

아직 없는 것:

- 완전한 감사 체인
- 키 폐기 정책
- 장기 망각/재학습 정책

## 현재 MPK가 실제로 덮는 범위

현재 `MemoryPhase_Kernel`은 주로 아래를 담당한다.

- Layer 1: 장기 기억 슬롯의 최소 형태
- Layer 1.5: 최소 누적 저장소 스캐폴딩 (`IdentityMemoryStore`)
- Layer 2: 동일성/공명 점수
- Layer 3: 접근 동역학 (`대칭 -> 진동 -> 감쇠 -> 공명 -> 붕괴`)
- Layer 4: 위상 전이
- Layer 5: 민감도 티어 허용
- Layer 5 준비용 Vault 스캐폴딩 (`RawStateVault`)
- Layer 6: 재용해 훅

즉 지금 MPK는 **기억 기반 보안 전체**가 아니라,  
그 보안의 중심 판단 코어라고 보는 것이 정확하다.

## 앞으로 확장될 때 지켜야 할 원칙

1. raw 데이터보다 feature/embedding/요약을 우선 저장
2. 위상 결정과 실제 복호/표시 계층을 분리
3. trust anchor 슬롯을 유지
4. audit와 UX를 분리
5. 사용자 기억은 누적되되, 과적응을 막는 drift 정책을 둔다
6. “비밀번호 폐기”보다 “기억 기반 연속 인증 강화”를 우선한다

## 한 줄 정의

**MPK는 “AI가 기억한 사용자에게만 정보가 얼음처럼 정렬되는가”를 결정하는 기초 접근 커널이다.**
