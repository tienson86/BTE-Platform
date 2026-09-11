/**
 * Number Energy API client. HTTP only. No engine imports.
 */

import { SERVER_FALLBACK, VALIDATION_FALLBACK } from "./labels";
import type { NumberEnergyEnvelope, PurposeContext } from "./types";

export const DEFAULT_NUMBER_ENERGY_API = "/backend/api/v1/number-energy/analyze";
export const FETCH_TIMEOUT_MS = 30_000;

export function numberEnergyApiUrl(): string {
  const fromWindow =
    typeof window !== "undefined"
      ? (window as Window & { __BTE_NUMBER_ENERGY_API__?: string }).__BTE_NUMBER_ENERGY_API__
      : undefined;
  return fromWindow || DEFAULT_NUMBER_ENERGY_API;
}

export async function analyzeNumberEnergy(
  number: string,
  purposeContext: PurposeContext,
): Promise<{ ok: boolean; status: number; envelope: NumberEnergyEnvelope; errorMessage: string }> {
  const url = resolvedUrl(numberEnergyApiUrl());
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        number,
        purpose_context: purposeContext,
      }),
      signal: controller.signal,
    });
    const text = await response.text();
    let envelope: NumberEnergyEnvelope = {};
    try {
      envelope = text ? (JSON.parse(text) as NumberEnergyEnvelope) : {};
    } catch {
      envelope = {};
    }
    if (!response.ok || envelope.success === false) {
      return {
        ok: false,
        status: response.status,
        envelope,
        errorMessage: customerErrorFromEnvelope(response.status, envelope),
      };
    }
    if (!envelope.data) {
      return {
        ok: false,
        status: response.status,
        envelope,
        errorMessage: SERVER_FALLBACK,
      };
    }
    return { ok: true, status: response.status, envelope, errorMessage: "" };
  } catch {
    return {
      ok: false,
      status: 0,
      envelope: {},
      errorMessage: SERVER_FALLBACK,
    };
  } finally {
    clearTimeout(timer);
  }
}

function resolvedUrl(url: string): string {
  if (url.startsWith("http://") || url.startsWith("https://")) {
    return url;
  }
  if (typeof window !== "undefined" && window.location?.origin) {
    return `${window.location.origin}${url}`;
  }
  return url;
}

export function customerErrorFromEnvelope(
  status: number,
  envelope: NumberEnergyEnvelope,
): string {
  if (status === 422) {
    return VALIDATION_FALLBACK;
  }
  if (status >= 500 || status === 0) {
    return SERVER_FALLBACK;
  }
  if (typeof envelope.message === "string" && envelope.message.trim()) {
    return envelope.message;
  }
  const detail = envelope.detail;
  if (Array.isArray(detail) && detail.length) {
    const first = detail[0] as { msg?: string };
    if (typeof first?.msg === "string" && first.msg.trim()) {
      return first.msg.replace(/^Value error,\s*/i, "");
    }
  }
  if (typeof detail === "string" && detail.trim()) {
    return detail;
  }
  return SERVER_FALLBACK;
}
