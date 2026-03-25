> **English:** [README_EN.md](README_EN.md)

# MemoryPhase_Kernel (MPK)

**Memory Phase Kernel** — 엣지 AI·로컬 에이전트에 맞춘 **기억·공명 기반 접근·해석 커널** 독립 패키지다.  
데이터를 기본 **liquid**(비해석)로 두고, 신뢰·채널 일치에 따라 **semi_frozen → frozen**으로 **의미 정렬(해석 윈도)** 을 허용한다.

쉽게 말하면:

- 데이터는 기본적으로 **물처럼 흘러가며** 바로 개인 의미를 드러내지 않는다.
- 로컬 AI 에이전트가 **“지금 들어온 사람이 내가 기억한 그 사용자와 얼마나 같은가”** 를 판단한다.
- 충분히 일치할 때만 데이터가 **얼음처럼 정렬**되어, 그 사용자에게만 의미 있게 읽힌다.
- 사용자가 떠나거나 신뢰가 내려가면 다시 **재용해(re-melt)** 되어 해석 창이 닫힌다.

- **버전**: `VERSION` / `pyproject.toml`  
- **의존성**: 코어 **stdlib only** (배포·엣지 친화)  
- **설계 정본**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)  
- **기초 레이어 맵**: [docs/FOUNDATION_LAYERS.md](docs/FOUNDATION_LAYERS.md)
- **보안 모델 설명**: [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md)
- **무결성 / 서명**: [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md), [PHAM_BLOCKCHAIN_LOG.md](PHAM_BLOCKCHAIN_LOG.md), `SIGNATURE.sha256`
- **철학·총망라 (레포 메타)**: [design_workspace/MEMORY_ACCESS_KERNEL_DESIGN.md](../design_workspace/MEMORY_ACCESS_KERNEL_DESIGN.md)

## 이 패키지가 하는 일 / 아직 안 하는 일

이 패키지는 **완성형 기억 기반 보안 제품**이 아니다.  
대신 그 보안 구조의 **기초 커널**을 제공한다.

현재 하는 일:

- 장기 프로필과 현재 신호를 비교한다.
- 공명(`resonance_index`)과 동일성 점수를 계산한다.
- `대칭 -> 진동 -> 감쇠 -> 공명 -> 붕괴` 수학 레이어의 최소 동역학을 계산한다.
- `liquid / semi_frozen / frozen` 위상을 결정한다.
- 어떤 민감도 티어까지 해석 가능한지 결정한다.
- 침입·유휴·드리프트 시 다시 `liquid`로 강등할 수 있다.
- 기초 `RawStateVault` / `IdentityMemoryStore` 스캐폴딩을 제공한다.

아직 안 하는 일:

- 실제 암복호화 구현
- 얼굴/음성/홍채/지문 자체의 추론 모델 내장
- 장기 누적 사용자 기억 학습 엔진
- 전체 운영 로그 저장소 자체
- Atom/Athena/Pharaoh 결과물의 실제 복호·마스킹 구현

즉 MPK는 **“누가 읽을 수 있는가”와 “어느 정도까지 의미가 열리는가”를 결정하는 커널**이다.

## 왜 생소한 개념인가

이 패키지는 일반적인 로그인 패키지처럼 보이지 않는다.  
그 이유는 목표가 단순한 “문 열기”가 아니기 때문이다.

일반 로그인:

- 비밀번호/토큰/패스키를 확인
- 맞으면 입장
- 틀리면 거부

MPK가 보는 접근:

- 사용자를 기억하는 장기 프로필이 있다
- 현재 사용자 신호가 들어온다
- 두 상태가 시간에 따라 맞물리며 수렴한다
- 충분히 수렴하면 정보가 **해석 가능한 상태**로 정렬된다
- 수렴이 깨지면 다시 해석 불가능 상태로 돌아간다

즉 이 패키지는 **접근 통과 여부**보다 **정보가 누구에게 의미 있게 열리는가**를 더 중요하게 본다.

## 왜 이 개념이 필요한가

보통 로그인은 비밀번호를 맞추는 구조다.  
MPK가 지향하는 것은 그보다 아래에 있는 **기억 기반 접근 커널**이다.

- 비밀번호를 외우는 보안이 아니라, **AI가 사용자를 기억하는 보안**
- 한 번 열고 끝나는 인증이 아니라, **세션 동안 계속 확인하는 연속 인증**
- 데이터를 그냥 열고 닫는 것이 아니라, **정보를 해석 가능한 상태로 정렬하는 위상 제어**

이 개념은 운영 시스템 위에서 특히 중요하다.

- Atom / Athena / Pharaoh 는 판단과 상태 수렴 결과를 만든다.
- MPK는 **누가 그 결과를 자기 정보로 해석할 수 있는지**를 결정한다.

## 빠른 시작

```bash
cd _staging/MemoryPhase_Kernel
python3 -m pytest tests/ -q
```

```python
from memory_phase_kernel import (
    IdentityProfile,
    LiveSignalFrame,
    MemoryPhaseKernel,
    readings_from_simple_map,
)

k = MemoryPhaseKernel()
profile = IdentityProfile("user-1", {"typing": 0.6, "voice": 0.4})
frame = LiveSignalFrame(
    readings=readings_from_simple_map({"typing": 0.9, "voice": 0.85}),
)
decision = k.evaluate(profile, frame)
print(decision.phase, decision.allowed_tiers, decision.score_bundle.resonance_index)
```

## 공개 API 요약

| 구성요소 | 역할 |
|----------|------|
| `MemoryPhaseKernel` | Trust Anchor(선택) + 프레임 → `AccessDecision` |
| `IdentityProfile` | 채널별 가중치(장기 기억 슬롯) |
| `LiveSignalFrame` | 엣지 관측 한 틱 |
| `compute_resonance_index` | Ω_res |
| `evolve_phase_dynamics` | 대칭→진동→감쇠→공명→붕괴 흐름 계산 |
| `TrustAnchorProtocol` | 패스키·Secure Enclave 등 앵커 주입 |

## 기초 레이어 맵

확장 가능한 구조를 위해, MPK는 아래 레이어를 기준으로 자라야 한다.

1. `Raw State Vault`
데이터를 기본 `liquid` 상태로 유지하는 저장층. 실제 저장/복호는 여전히 외부 책임이지만, 패키지 안에 `RawStateVault` 스캐폴딩이 들어 있다.

2. `Identity Memory Engine`
사용자 장기 기억 슬롯. 현재 `IdentityProfile`이 가장 작은 형태로 담당하고, `IdentityMemoryStore`가 누적 저장소의 시작점을 제공한다.

3. `Continuous Identity Scoring`
현재 신호와 장기 기억 비교. 현재 `score_frame()`과 `compute_resonance_index()`가 담당한다.

4. `Access Dynamics Layer`
대칭 -> 진동 -> 감쇠 -> 공명 -> 붕괴 흐름을 계산하는 수학 레이어. 현재 `dynamics.py`가 최소 스캐폴딩을 제공한다.

5. `Phase Transition Controller`
`liquid / semi_frozen / frozen` 전이. 현재 `phase_control.py`가 담당한다.

6. `Access Kernel`
민감도 티어별 해석 허용. 현재 `AccessDecision`과 `allowed_tiers`가 담당한다.

7. `Audit / Forgetting / Re-melt`
세션 종료, 침입, 유휴 시 재용해. 현재 `ReMeltEvent`와 `should_re_melt()`가 시작점이다.

중요한 점:

- **현재 구현된 것은 주로 2~6층**이다.
- 1층의 실제 데이터 저장/복호 계층은 아직 외부 책임이다.
- 7층도 기초 훅은 있지만, 완전한 감사·망각 시스템은 아직 아니다.

## 현재 구현 범위

현재 MPK는 다음 질문에 답하는 커널이다.

- “지금 이 사람은 내가 기억한 사용자와 얼마나 비슷한가?”
- “이 세션은 어느 위상까지 올라가도 되는가?”
- “지금 어떤 민감도 티어까지 해석을 허용할 것인가?”

즉 지금은 **판단 커널** 단계다.  
앞으로 이 위에 다중모달 기억 학습, Raw Vault, 실제 해석 복원 계층을 쌓을 수 있다.

현재 패키지 안에는 이 확장을 위한 최소 스캐폴딩도 포함된다.

- `RawStateVault` / `VaultRecord`
- `IdentityMemoryStore` / `SubjectMemoryState`
- `PhaseDynamicsState` / `evolve_phase_dynamics()`

그리고 이제 기초 보안성도 한 단계 올라갔다.

- `RawStateVault`는 `phase`뿐 아니라 `collapse_score`까지 보고 실제 materialize 여부를 결정할 수 있다.
- `IdentityMemoryStore`는 누적만 하지 않고 `forgetting`과 `drift penalty`를 받을 수 있다.

운영 시스템 연결도 시작됐다.

- `atom_result_to_vault_record()`
- `athena_result_to_vault_record()`
- `pharaoh_result_to_vault_record()`
- `MemoryPhaseSessionLoop`

즉 이제 MPK는 운영 결과를 Vault로 바꾸고, 세션 동안 `입장 -> materialize -> re-melt` 흐름을 관찰하는 최소 루프를 가진다.

중요:

- 이제 동역학 레이어는 단순 관측용이 아니다.
- `collapse_score`가 실제 `phase/access decision` 계산에 반영된다.
- 즉 `붕괴 -> 입장` 흐름이 실제 판정 경로에 연결되기 시작했다.

## 활용성

이 패키지는 지금 당장 완제품 로그인 시스템을 대체하려는 것이 아니다.  
대신 아래 같은 기초/연구/로컬 에이전트 환경에서 특히 유용하다.

- 개인 AI 에이전트의 로컬 접근 커널
- 운영 시스템 결과를 사용자별로 다른 민감도 티어로 열어야 하는 환경
- 연속 인증과 세션 중 재잠금이 중요한 환경
- 비전문가도 레이어를 이해하면서 확장할 수 있는 보안 워크벤치
- Atom / Athena / Pharaoh 같은 운영 판단 결과를 해석 권한과 분리하고 싶은 환경

## 다른 보안 방식과의 관계

MPK는 기존 보안을 부정하지 않는다.  
오히려 아래 방식을 **대체**하기보다 **결합**하는 것이 현실적이다.

1. 비밀번호 / 패스키 / Secure Enclave
- 소유와 루트 신뢰를 확인하는 층

2. 생체 인증
- 얼굴/지문/홍채처럼 강한 특정 채널

3. 행동 기반 연속 인증
- 타이핑, 말투, 사용 습관, 시간대, 장치 흐름

4. MPK
- 위 채널들을 장기 기억과 비교해서
- `물 -> 얼음`
- `대칭 -> 진동 -> 감쇠 -> 공명 -> 붕괴`
- `입장 -> 재용해`
  흐름으로 조직하는 커널

즉 MPK는 “또 하나의 인증 수단”이라기보다,  
**여러 인증/행동 신호를 기억 기반 접근 구조로 조직하는 상위 커널**에 가깝다.

## 레이어를 어떻게 쌓아가야 하나

가장 안전한 확장 순서는 아래와 같다.

1. `TrustAnchorProtocol` 현실화
- 패스키, Secure Enclave, TPM 등

2. `LiveSignalFrame` 채널 확장
- typing
- voice
- language
- gaze
- device

3. `IdentityMemoryStore` 고도화
- forgetting
- drift
- 장기 적응
- 정상 변동 범위

4. `RawStateVault` 고도화
- 실제 저장소
- 세션 키
- remask
- 키 폐기

5. 운영 브리지 확장
- Atom
- Athena
- Pharaoh
- FirstOrder

6. observer loop 확장
- 세션 수명주기
- 재용해 트리거
- 감사 체인

## 현재 상태 표

| 항목 | 상태 |
|------|------|
| 기억 기반 점수 | 구현됨 |
| 공명/동역학 | 구현됨 |
| 붕괴 기반 입장 판정 | 구현됨 |
| Vault materialize | 기초 구현 |
| forgetting / drift | 기초 구현 |
| 운영 결과 브리지 | 기초 구현 |
| 세션 observer loop | 기초 구현 |
| 실제 암복호/키 관리 | 아직 외부 책임 |
| 완전한 감사 체인 | 아직 미구현 |

## 확장

- `memory_phase_kernel.extensions` — `ChannelAdapter` 프로토콜 + `KeystrokeRhythmStubAdapter` 샘플.
- `memory_phase_kernel.integrations.parse_mak_access_bridge` — FirstOrder `evidence["mak_access_bridge"]` 파싱.
- 운영 스택은 **MPK 패키지 없이도** 브리지 필드만 넣을 수 있다(FirstOrder v0.1.2+).

## 라이선스

`pyproject.toml` 기준 MIT (필요 시 조직 정책에 맞게 변경).
