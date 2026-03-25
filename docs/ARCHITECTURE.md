> **English:** [ARCHITECTURE_EN.md](ARCHITECTURE_EN.md)

# Memory Phase Kernel (MPK) — 아키텍처·설계 정본

**패키지 루트**: `_staging/MemoryPhase_Kernel/`  
**Python 모듈**: `memory_phase_kernel` (import 이름)  
**버전**: `VERSION` 파일 및 `pyproject.toml` 과 동기

**관련 개념 문서 (00_BRAIN 메타)**: [design_workspace/MEMORY_ACCESS_KERNEL_DESIGN.md](../design_workspace/MEMORY_ACCESS_KERNEL_DESIGN.md) — 물·얼음·공명·MAK 레이어 철학 총망라. **본 문서는 상용 독립 모듈의 구현 경계와 확장 계약**에 초점을 둔다.
**기초 레이어 문서**: [FOUNDATION_LAYERS.md](FOUNDATION_LAYERS.md) — MPK가 전체 기억 기반 보안 중 어디까지 구현하는지 설명.

---

## 1. 목적과 비목표

### 1.1 목적

- **엣지 AI 친화적** 접근·해석 커널: 로컬에서 관측된 신호를 **장기 프로파일**과 결합해, 데이터를 **liquid / semi_frozen / frozen** 위상으로 다룬다.
- **운영 시스템과 분리**: Atom·Athena·Pharaoh·FirstOrder 등은 **산출물 생산**만 담당하고, MPK는 **누가 어떤 민감도 티어를 어떤 위상에서 읽는지**만 결정한다(산출물 불변).
- **확장 가능**: 코어는 **stdlib only**; 카메라·음성·키스트로크 등은 `extensions/` 및 외부 패키지에서 `LiveSignalFrame`만 채운다.

### 1.2 비목표 (v0.1)

- 실제 암호 구현(AES/GCM, HSM) 내장 — **TrustAnchorProtocol** 뒤에 둔다.
- 딥러닝 추론 엔진 내장 — **채널별 match_score**만 주입.
- 단일 제품으로 “비밀번호 완전 폐기” 주장 — **Trust Anchor 슬롯**을 문서·API에 유지한다.

---

## 2. 핵심 개념 매핑

| 개념 (서사) | MPK 타입 / 모듈 |
|-------------|-----------------|
| 물 (비해석) | `DataPhase.LIQUID` |
| 얼음 (해석 윈도) | `DataPhase.FROZEN` (+ `SEMI_FROZEN` 중간대) |
| 공명 (채널 일치) | `resonance.compute_resonance_index` → `IdentityScoreBundle.resonance_index` |
| 기억 (가중치) | `IdentityProfile.channel_weights` |
| Trust 뿌리 | `TrustAnchorProtocol` / `NullTrustAnchor` |
| 재용해 | `ReMeltEvent` + 정책 `should_re_melt` |

---

## 2.5 현재 구현 범위

MPK는 전체 기억 기반 보안 시스템 전체를 혼자 구현하지 않는다.

- 현재 강하게 구현된 층: 장기 기억 슬롯, 공명 점수, 접근 동역학, 위상 전이, 허용 티어 결정
- 현재 약하게 구현된 층: re-melt 훅, trust anchor 슬롯, `RawStateVault`/`IdentityMemoryStore` 스캐폴딩
- 아직 외부 책임인 층: 실제 Raw Vault 저장소, 실제 복호/마스킹, 장기 학습형 기억 엔진, 감사 체인

즉 MPK는 **판단 커널**이지, 완전한 저장소나 생체 추론 패키지는 아니다.

---

## 3. 모듈 구조

```
memory_phase_kernel/
  __init__.py          # 공개 API
  contracts.py         # Phase, 티어, 프레임, 정책 임계, 감사 표면
  resonance.py         # Ω_res (가중 일치)
  profile.py           # IdentityProfile, score_frame
  phase_control.py     # phase/tier 결정, re-melt 규칙
  trust.py             # TrustAnchorProtocol
  kernel.py            # MemoryPhaseKernel 파사드
  extensions/          # 어댑터 네임스페이스 (빈 슬롯)
```

**의존성 방향**: `kernel` → `profile` → `resonance` / `contracts` ; `trust` 는 프로토콜만.

---

## 4. 데이터 흐름 (런타임)

1. **엣지 어댑터**가 관측을 `ChannelReading` 리스트로 묶어 `LiveSignalFrame` 생성.  
2. **IdentityProfile**이 채널 가중치를 제공.  
3. `score_frame()`이 `resonance_index` 및 `identity_score`(기본 동일, override 가능) 산출.  
4. `evolve_phase_dynamics()`가 `대칭 -> 진동 -> 감쇠 -> 공명 -> 붕괴` 상태를 계산.  
5. `build_access_decision()`이 `identity_score + collapse_score`를 함께 사용해 phase·허용 티어 결정; 침입·유휴 시 liquid 강등.  
6. **앱 레이어**가 `AccessDecision`에 따라 조건부 복호·UI 마스킹을 수행(MPK 외부).

---

## 5. 상용·확장 가이드

### 5.1 설정 가능 항목

- `PolicyThresholds`: frozen/semi 임계, 침입·유휴 re-melt.  
- `MemoryPhaseKernelConfig.require_trust_anchor`: 상용에서 True 권장.  
- 프로파일 `version`: 재학습 시 마이그레이션 훅.

### 5.2 확장 포인트

| 확장 | 방법 |
|------|------|
| 새 센서 채널 | `ChannelReading` + 프로파일 가중치 추가 |
| 엣지 어댑터 | `extensions.ChannelAdapter` 구현 → `capture()` 로 `LiveSignalFrame` 공급 (예: `KeystrokeRhythmStubAdapter`) |
| 앵커 | `TrustAnchorProtocol` 구현체 주입 |
| 정책 성숙도 | 임계값을 시간·채널 수에 따라 외부 정책 엔진에서 갱신해 주입 |
| 감사 | `AuditSurface` 참조해 앱이 로그 저장 (MPK는 이벤트 타입만 정의) |
| FirstOrder 연동 | `integrations.parse_mak_access_bridge(evidence)` — 호스트가 `AccessDecision.allowed_tiers` 와 `mak_sensitivity_tier` 교차 검증 |

기초 스캐폴딩 추가:

- `RawStateVault`는 `phase + collapse_score` 기반 materialize 경로를 제공
- `IdentityMemoryStore`는 `apply_forgetting()` / `apply_drift_penalty()`를 제공
- `integrations.governance_vaults`는 Atom/Athena/Pharaoh 결과를 `VaultRecord`로 바꾸는 브리지를 제공
- `MemoryPhaseSessionLoop`는 `입장 -> materialize -> re-melt`의 최소 observer 루프를 제공

### 5.3 배포

- `pip install -e .` 또는 wheel 빌드 후 내부 레지스트리 업로드.  
- 코어에 네이티브 의존성 없음 → **엣지 디바이스**에 적합.

---

## 6. 운영 스택 연동 계약 (선택 필드)

**FirstOrder (v0.1.2+)** 는 `run_force_assessment` 결과 `evidence`에 아래 형태의 블록을 넣는다 (`memory_phase_kernel` 미설치여도 동작).

```json
"mak_access_bridge": {
  "mak_sensitivity_tier": "operational",
  "mak_evidence_ref": "<blackbox head hash>",
  "operational_posture_stage": "neutral"
}
```

MPK 측 파서: `parse_mak_access_bridge(evidence)`.

| 필드 | 설명 |
|------|------|
| `mak_sensitivity_tier` | 호스트가 제안하는 데이터 민감도 티어 |
| `mak_evidence_ref` | 감사 체인 포인터(예: BlackBox head) |
| `operational_posture_stage` | 티어 자동 매핑의 근거가 된 운영 자세 |

MPK 코어 **결정기**는 이 필드를 사용하지 않는다. **앱 브리지**에서 `AccessDecision.allowed_tiers` 와 교차 검증한다.

---

## 7. 보안 주의

- `NullTrustAnchor`는 **개발 전용**.  
- `match_score` 스푸핑 방지는 **채널별 quality** 및 **앵커**로 상쇄.  
- 감사: “공명으로 frozen 진입”은 **내부적으로 기록**하는 것을 권장(UX 흔적 최소와 분리).

---

## 8. 로드맵 (패키지)

- v0.2: `ChannelAdapter` 프로토콜 초안, 샘플 keystroke 어댑터(선택)  
- v0.3: 정책 YAML 로더(선택 의존성)  
- v1.0: 안정 API凍結, 보안 검토 체크리스트

---

*v0.1 — 변경 시 `ARCHITECTURE_EN.md`·`README`·`CHANGELOG` 동기화.*
