/**
 * Approved ShenSha customer knowledge lookup.
 * Reads frozen interpretation-domain entities. Does not invent meanings.
 */

import duongNhan from "../../../../knowledge/interpretation/domains/shensha/duong_nhan.json";
import hoaCai from "../../../../knowledge/interpretation/domains/shensha/hoa_cai.json";
import hongLoan from "../../../../knowledge/interpretation/domains/shensha/hong_loan.json";
import locThan from "../../../../knowledge/interpretation/domains/shensha/loc_than.json";
import nguyetDuc from "../../../../knowledge/interpretation/domains/shensha/nguyet_duc.json";
import nguyetDucQuyNhan from "../../../../knowledge/interpretation/domains/shensha/nguyet_duc_quy_nhan.json";
import thienAt from "../../../../knowledge/interpretation/domains/shensha/thien_at.json";
import thienAtQuyNhan from "../../../../knowledge/interpretation/domains/shensha/thien_at_quy_nhan.json";
import thienDuc from "../../../../knowledge/interpretation/domains/shensha/thien_duc.json";
import thienDucQuyNhan from "../../../../knowledge/interpretation/domains/shensha/thien_duc_quy_nhan.json";
import thienHy from "../../../../knowledge/interpretation/domains/shensha/thien_hy.json";
import vanXuong from "../../../../knowledge/interpretation/domains/shensha/van_xuong.json";

type RelatedEntity = {
  readonly key?: string;
};

type ApprovedShenShaEntity = {
  readonly key?: string;
  readonly positive_meaning?: string;
  readonly manifestation?: string;
  readonly meaning?: string;
  readonly related_entities?: readonly RelatedEntity[];
  readonly metadata?: {
    readonly status?: string;
  };
};

const TECHNICAL =
  /TIAN_|YUE_|HONG_|HUA_|WEN_|append|detector|engine|service\.py|stem_list|branch_list|token tháng|nhãn đủ|cùng hit|cùng khối|production list|stems hit|tra cứu alias/i;
const FEAR = /tai họa|cô độc chắc chắn|hôn nhân xấu|đại hung|nguy hiểm|ly hôn|khắc chồng/i;
const ALIAS_WEAK = /nhãn đủ|cùng hit|cùng kênh|alias|cùng detector|tra cứu quý/i;

const ENTITIES: readonly ApprovedShenShaEntity[] = [
  duongNhan,
  hoaCai,
  hongLoan,
  locThan,
  nguyetDuc,
  nguyetDucQuyNhan,
  thienAt,
  thienAtQuyNhan,
  thienDuc,
  thienDucQuyNhan,
  thienHy,
  vanXuong,
];

const BY_KEY = new Map<string, ApprovedShenShaEntity>(
  ENTITIES.filter((entity) => entity.key).map((entity) => [String(entity.key), entity]),
);

function firstSentence(value: string): string {
  const trimmed = value.trim();
  if (!trimmed) return "";
  const match = trimmed.match(/^(.+?[.。])(?:\s|$)/);
  return (match ? match[1] : trimmed).trim();
}

function customerSafeLine(value: unknown): string {
  if (typeof value !== "string") return "";
  const line = firstSentence(value);
  if (!line || TECHNICAL.test(line) || FEAR.test(line)) return "";
  return line;
}

function approvedLine(entity: ApprovedShenShaEntity | undefined): string {
  if (!entity || (entity.metadata?.status && entity.metadata.status !== "approved")) return "";
  const positive = customerSafeLine(entity.positive_meaning);
  if (positive && !ALIAS_WEAK.test(entity.positive_meaning || "")) return positive;
  const manifestation = customerSafeLine(entity.manifestation);
  if (manifestation) return manifestation;
  if (positive) return positive;
  return "";
}

function isAliasWeak(entity: ApprovedShenShaEntity | undefined): boolean {
  if (!entity) return false;
  return ALIAS_WEAK.test(entity.positive_meaning || "") || ALIAS_WEAK.test(entity.meaning || "");
}

/**
 * Concise customer meaning from approved domain knowledge, keyed by canonical name.
 */
export function approvedShenShaMeaning(canonicalName: string): string {
  const key = canonicalName.trim();
  if (!key) return "";
  const entity = BY_KEY.get(key);
  if (!isAliasWeak(entity)) {
    const own = approvedLine(entity);
    if (own) return own;
  }
  const relatedKey = entity?.related_entities?.[0]?.key;
  if (!relatedKey || relatedKey === key) return approvedLine(entity);
  return approvedLine(BY_KEY.get(relatedKey)) || approvedLine(entity);
}

export function hasApprovedShenShaMeaning(canonicalName: string): boolean {
  return Boolean(approvedShenShaMeaning(canonicalName));
}
