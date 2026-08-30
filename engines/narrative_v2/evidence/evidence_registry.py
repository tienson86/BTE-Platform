"""Evidence field catalog and allowed domains.

Maps Narrative V2 requested facts onto the audited CanonicalAnalysis schema.
Does not invent source paths. Does not calculate astrology.
"""

from __future__ import annotations

from dataclasses import dataclass

ALLOWED_DOMAINS: tuple[str, ...] = (
    "identity",
    "calendar",
    "bazi",
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "five_elements",
    "ten_gods",
    "shensha",
    "luck",
)

FORBIDDEN_SOURCE_PREFIXES: tuple[str, ...] = (
    "interpretation",
    "narrative",
    "narrative_result",
    "integrated_narrative",
    "report",
    "commercial_consulting",
    "customer",
)

FORBIDDEN_KEY_TOKENS: tuple[str, ...] = (
    "headline",
    "summary",
    "insight",
    "customer_meaning",
    "customer_reason",
    "action",
    "warning",
    "decision",
    "recommendation",
    "reasoning",
)


@dataclass(frozen=True, slots=True)
class EvidenceFieldSpec:
    """One extractable published field."""

    evidence_id: str
    domain: str
    key: str
    label: str
    source_path: str
    requested: bool = True


def _pillar_specs() -> tuple[EvidenceFieldSpec, ...]:
    specs: list[EvidenceFieldSpec] = []
    for pillar in ("year", "month", "day", "hour"):
        prefix = f"bazi.{pillar}_pillar"
        specs.extend(
            (
                EvidenceFieldSpec(
                    evidence_id=f"evidence.bazi.{pillar}_pillar.stem",
                    domain="bazi",
                    key=f"{pillar}_pillar.stem",
                    label=f"{pillar} stem",
                    source_path=f"{prefix}.stem",
                ),
                EvidenceFieldSpec(
                    evidence_id=f"evidence.bazi.{pillar}_pillar.branch",
                    domain="bazi",
                    key=f"{pillar}_pillar.branch",
                    label=f"{pillar} branch",
                    source_path=f"{prefix}.branch",
                ),
                EvidenceFieldSpec(
                    evidence_id=f"evidence.bazi.{pillar}_pillar.nap_am",
                    domain="bazi",
                    key=f"{pillar}_pillar.nap_am",
                    label=f"{pillar} nạp âm",
                    source_path=f"{prefix}.nap_am",
                ),
                EvidenceFieldSpec(
                    evidence_id=f"evidence.bazi.{pillar}_pillar.truong_sinh",
                    domain="bazi",
                    key=f"{pillar}_pillar.truong_sinh",
                    label=f"{pillar} trường sinh",
                    source_path=f"{prefix}.truong_sinh",
                ),
                EvidenceFieldSpec(
                    evidence_id=f"evidence.bazi.{pillar}_pillar.hidden_stems",
                    domain="bazi",
                    key=f"{pillar}_pillar.hidden_stems",
                    label=f"{pillar} tàng can",
                    source_path=f"{prefix}.hidden_stems",
                ),
                EvidenceFieldSpec(
                    evidence_id=f"evidence.bazi.{pillar}_pillar.ten_god",
                    domain="bazi",
                    key=f"{pillar}_pillar.ten_god",
                    label=f"{pillar} thập thần",
                    source_path=f"{prefix}.ten_god",
                ),
            )
        )
    return tuple(specs)


def _five_element_specs() -> tuple[EvidenceFieldSpec, ...]:
    specs: list[EvidenceFieldSpec] = []
    for key, label in (
        ("wood", "Mộc"),
        ("fire", "Hỏa"),
        ("earth", "Thổ"),
        ("metal", "Kim"),
        ("water", "Thủy"),
    ):
        specs.append(
            EvidenceFieldSpec(
                evidence_id=f"evidence.five_elements.{key}.count",
                domain="five_elements",
                key=f"{key}.count",
                label=f"{label} count",
                source_path=f"five_elements.{key}.count",
            )
        )
    specs.append(
        EvidenceFieldSpec(
            evidence_id="evidence.five_elements.dominant",
            domain="five_elements",
            key="dominant",
            label="published dominant element",
            source_path="five_elements.dominant",
        )
    )
    return tuple(specs)


SCALAR_SPECS: tuple[EvidenceFieldSpec, ...] = (
    EvidenceFieldSpec(
        evidence_id="evidence.identity.name",
        domain="identity",
        key="name",
        label="name",
        source_path="identity.person.full_name",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.identity.gender",
        domain="identity",
        key="gender",
        label="gender",
        source_path="identity.person.gender",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.identity.solar_birth",
        domain="identity",
        key="solar_birth",
        label="solar birth",
        source_path="identity.person.solar_birth",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.identity.birth_time",
        domain="identity",
        key="birth_time",
        label="birth time",
        source_path="identity.person.birth_time",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.identity.timezone",
        domain="identity",
        key="timezone",
        label="timezone",
        source_path="identity.person.timezone",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.identity.birth_place",
        domain="identity",
        key="birth_place",
        label="birth place",
        source_path="identity.person.birth_place",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.identity.analysis_id",
        domain="identity",
        key="analysis_id",
        label="analysis id",
        source_path="analysis_id",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.calendar.solar_date",
        domain="calendar",
        key="solar_date",
        label="solar date",
        source_path="calendar.solar_date",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.calendar.lunar_date",
        domain="calendar",
        key="lunar_date",
        label="lunar date",
        source_path="calendar.lunar_date",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.calendar.solar_term",
        domain="calendar",
        key="solar_term",
        label="solar term",
        source_path="calendar.solar_term.name",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.calendar.timezone",
        domain="calendar",
        key="timezone",
        label="timezone",
        source_path="calendar.timezone",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.bazi.day_master",
        domain="bazi",
        key="day_master",
        label="day master",
        source_path="bazi.day_master",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.bazi.day_master_element",
        domain="bazi",
        key="day_master_element",
        label="day master element",
        source_path="bazi.day_master_element",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.bazi.day_master_yin_yang",
        domain="bazi",
        key="day_master_yin_yang",
        label="day master yin yang",
        source_path="bazi.day_master_yin_yang",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.strength.level",
        domain="strength",
        key="strength_level",
        label="strength class",
        source_path="strength.strength_level",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.strength.score",
        domain="strength",
        key="strength_score",
        label="strength score",
        source_path="strength.strength_score",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.temperature.climate_state",
        domain="temperature",
        key="climate_state",
        label="temperature state",
        source_path="temperature.climate_state",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.temperature.balancing_need",
        domain="temperature",
        key="balancing_need",
        label="balancing need",
        source_path="temperature.balancing_need",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.pattern.primary",
        domain="pattern",
        key="pattern",
        label="pattern",
        source_path="pattern.pattern",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.pattern.cach_cuc",
        domain="pattern",
        key="cach_cuc",
        label="cách cục",
        source_path="pattern.cach_cuc",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.pattern.than_vuong_nhuoc",
        domain="pattern",
        key="than_vuong_nhuoc",
        label="thân vượng nhược",
        source_path="pattern.than_vuong_nhuoc",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.useful_god.primary",
        domain="useful_god",
        key="useful_god",
        label="useful god",
        source_path="useful_god.useful_god",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.useful_god.element",
        domain="useful_god",
        key="useful_element",
        label="useful god element",
        source_path="useful_god.useful_element",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.useful_god.stem",
        domain="useful_god",
        key="useful_stem",
        label="useful god stem",
        source_path="useful_god.useful_stem",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.useful_god.ten_god",
        domain="useful_god",
        key="useful_ten_god",
        label="useful god ten god",
        source_path="useful_god.useful_ten_god",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.useful_god.favorable",
        domain="useful_god",
        key="favorable_gods",
        label="favorable gods",
        source_path="useful_god.favorable_gods",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.useful_god.unfavorable",
        domain="useful_god",
        key="unfavorable_gods",
        label="unfavorable gods",
        source_path="useful_god.unfavorable_gods",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.luck.direction",
        domain="luck",
        key="direction",
        label="luck direction",
        source_path="luck.direction",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.luck.start_age",
        domain="luck",
        key="start_age",
        label="luck starting age",
        source_path="luck.start_age",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.luck.current_cycle",
        domain="luck",
        key="current_cycle",
        label="current luck cycle",
        source_path="luck.current_cycle.gan_zhi",
    ),
    EvidenceFieldSpec(
        evidence_id="evidence.luck.available",
        domain="luck",
        key="available",
        label="luck available",
        source_path="luck.available",
    ),
) + _pillar_specs() + _five_element_specs()


class EvidenceRegistry:
    """Published-field registry. No builder implementation of astrology."""

    def specs(self) -> tuple[EvidenceFieldSpec, ...]:
        """Return the audited extraction catalog."""
        return SCALAR_SPECS

    def allowed_domains(self) -> tuple[str, ...]:
        """Return allowed evidence domains."""
        return ALLOWED_DOMAINS
