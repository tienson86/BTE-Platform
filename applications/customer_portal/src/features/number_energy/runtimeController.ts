/**
 * RB08 Number Energy runtime controller / hook.
 *
 * Orchestrates validate → runtime client → adapter.
 * NumberEnergyPage may import the hook only for explicit runtimeMode.
 * Default public page stays static and must not fetch on load.
 * Freeze: NUMBER_ENERGY_STATIC_UI_V1
 */

import { useCallback, useEffect, useRef, useState } from "react";

import { adaptNumberEnergyPresentation } from "./presentationAdapter";
import {
  PURPOSE_CONTEXT_VALUES,
  type NumberEnergyAdapterResult,
  type NumberEnergyPresentationView,
  type PresentationSlotId,
  type RuntimeGap,
  type SlotRenderSource,
} from "./presentationContract";
import {
  analyzeNumberEnergyRuntime,
  type NumberEnergyRuntimeAnalyzeInput,
  type NumberEnergyRuntimeClientError,
  type NumberEnergyRuntimeResult,
} from "./runtimeClient";

export const NUMBER_ENERGY_RUNTIME_STATUS = {
  idle: "idle",
  loading: "loading",
  success: "success",
  error: "error",
} as const;

export type NumberEnergyRuntimeStatus =
  (typeof NUMBER_ENERGY_RUNTIME_STATUS)[keyof typeof NUMBER_ENERGY_RUNTIME_STATUS];

export type NumberEnergyRuntimePublicError = {
  code: string;
  message: string;
};

export type NumberEnergyRuntimeState = {
  status: NumberEnergyRuntimeStatus;
  view: NumberEnergyPresentationView | null;
  adapterResult: NumberEnergyAdapterResult | null;
  slotSource: Record<PresentationSlotId, SlotRenderSource> | null;
  gaps: readonly RuntimeGap[];
  error: NumberEnergyRuntimePublicError | null;
};

export type NumberEnergyRuntimeControllerDeps = {
  analyze?: (input: NumberEnergyRuntimeAnalyzeInput) => Promise<NumberEnergyRuntimeResult>;
  adapt?: typeof adaptNumberEnergyPresentation;
};

export type NumberEnergyRuntimeController = {
  getState: () => NumberEnergyRuntimeState;
  subscribe: (listener: (state: NumberEnergyRuntimeState) => void) => () => void;
  submit: (input: NumberEnergyRuntimeAnalyzeInput) => Promise<NumberEnergyRuntimeState>;
  reset: () => void;
};

const SAFE_INPUT_MESSAGE = "Dữ liệu phân tích chưa hợp lệ.";
const SAFE_CONTEXT_MESSAGE = "Ngữ cảnh sử dụng chưa hợp lệ.";
const SAFE_ADAPTER_MESSAGE = "Không thể hoàn tất phân tích lúc này.";
const INPUT_SEPARATORS = /[.\s-]/g;
const VEHICLE_CONTEXTS = new Set(["car_plate", "motorcycle_plate", "motorbike_plate"]);
const IDENTITY_CONTEXTS = new Set(["id_number"]);

/**
 * Create a standalone runtime controller. No fetch until submit().
 */
export function createNumberEnergyRuntimeController(
  deps: NumberEnergyRuntimeControllerDeps = {},
): NumberEnergyRuntimeController {
  const analyze = deps.analyze ?? analyzeNumberEnergyRuntime;
  const adapt = deps.adapt ?? adaptNumberEnergyPresentation;
  let state = idleState();
  let generation = 0;
  const listeners = new Set<(next: NumberEnergyRuntimeState) => void>();

  function setState(next: NumberEnergyRuntimeState): NumberEnergyRuntimeState {
    state = next;
    for (const listener of listeners) {
      listener(state);
    }
    return state;
  }

  return {
    getState: () => state,
    subscribe(listener) {
      listeners.add(listener);
      return () => {
        listeners.delete(listener);
      };
    },
    reset() {
      generation += 1;
      setState(idleState());
    },
    async submit(input) {
      const normalized = normalizeRuntimeSubmit(input);
      if (!normalized.ok) {
        generation += 1;
        return setState(errorState(normalized.error));
      }
      const token = (generation += 1);
      setState(loadingState());
      let clientResult: NumberEnergyRuntimeResult;
      try {
        clientResult = await analyze(normalized.value);
      } catch {
        if (token !== generation) {
          return state;
        }
        return setState(errorState({ code: "NETWORK_ERROR", message: SAFE_ADAPTER_MESSAGE }));
      }
      if (token !== generation) {
        return state;
      }
      if (!clientResult.ok) {
        return setState(errorState(toPublicError(clientResult.error)));
      }
      try {
        const adapterResult = adapt(clientResult.data);
        if (token !== generation) {
          return state;
        }
        return setState(successState(adapterResult));
      } catch {
        if (token !== generation) {
          return state;
        }
        return setState(errorState({ code: "ADAPTER_ERROR", message: SAFE_ADAPTER_MESSAGE }));
      }
    },
  };
}

/**
 * React hook over the runtime controller. Not wired into NumberEnergyPage.
 */
export function useNumberEnergyRuntime(
  deps: NumberEnergyRuntimeControllerDeps = {},
): NumberEnergyRuntimeState & {
  submit: NumberEnergyRuntimeController["submit"];
  reset: NumberEnergyRuntimeController["reset"];
} {
  const controllerRef = useRef<NumberEnergyRuntimeController | null>(null);
  if (controllerRef.current === null) {
    controllerRef.current = createNumberEnergyRuntimeController(deps);
  }
  const controller = controllerRef.current;
  const [state, setState] = useState<NumberEnergyRuntimeState>(controller.getState());

  useEffect(() => controller.subscribe(setState), [controller]);

  const submit = useCallback(
    (input: NumberEnergyRuntimeAnalyzeInput) => controller.submit(input),
    [controller],
  );
  const reset = useCallback(() => {
    controller.reset();
  }, [controller]);

  return { ...state, submit, reset };
}

function normalizeRuntimeSubmit(
  input: NumberEnergyRuntimeAnalyzeInput,
):
  | { ok: true; value: NumberEnergyRuntimeAnalyzeInput }
  | { ok: false; error: NumberEnergyRuntimePublicError } {
  const purpose = input.purpose_context.trim();
  if (!isRuntimePurpose(purpose)) {
    return { ok: false, error: { code: "INVALID_INPUT", message: SAFE_CONTEXT_MESSAGE } };
  }
  const compact = input.input.trim().replace(INPUT_SEPARATORS, "");
  if (!compact) {
    return { ok: false, error: { code: "INVALID_INPUT", message: SAFE_INPUT_MESSAGE } };
  }
  if (purpose === "phone_number" && !/^[0-9]+$/.test(compact)) {
    return { ok: false, error: { code: "INVALID_INPUT", message: SAFE_INPUT_MESSAGE } };
  }
  if (VEHICLE_CONTEXTS.has(purpose)) {
    if (!/^[0-9A-Za-z]+$/.test(compact)) {
      return { ok: false, error: { code: "INVALID_INPUT", message: SAFE_INPUT_MESSAGE } };
    }
    return {
      ok: true,
      value: {
        purpose_context: purpose,
        input: input.input.trim(),
        apiUrl: input.apiUrl,
      },
    };
  }
  if (IDENTITY_CONTEXTS.has(purpose)) {
    if (!/^[0-9A-Za-z]+$/.test(compact)) {
      return { ok: false, error: { code: "INVALID_INPUT", message: SAFE_INPUT_MESSAGE } };
    }
    return {
      ok: true,
      value: {
        purpose_context: purpose,
        input: input.input.trim(),
        apiUrl: input.apiUrl,
      },
    };
  }
  if (!/^[0-9]+$/.test(compact)) {
    return { ok: false, error: { code: "INVALID_INPUT", message: SAFE_INPUT_MESSAGE } };
  }
  return {
    ok: true,
    value: {
      purpose_context: purpose,
      input: compact,
      apiUrl: input.apiUrl,
    },
  };
}

function isRuntimePurpose(value: string): boolean {
  return (PURPOSE_CONTEXT_VALUES as readonly string[]).includes(value);
}

function idleState(): NumberEnergyRuntimeState {
  return {
    status: NUMBER_ENERGY_RUNTIME_STATUS.idle,
    view: null,
    adapterResult: null,
    slotSource: null,
    gaps: [],
    error: null,
  };
}

function loadingState(): NumberEnergyRuntimeState {
  return {
    status: NUMBER_ENERGY_RUNTIME_STATUS.loading,
    view: null,
    adapterResult: null,
    slotSource: null,
    gaps: [],
    error: null,
  };
}

function successState(adapterResult: NumberEnergyAdapterResult): NumberEnergyRuntimeState {
  return {
    status: NUMBER_ENERGY_RUNTIME_STATUS.success,
    view: adapterResult.view,
    adapterResult,
    slotSource: adapterResult.slotSource,
    gaps: adapterResult.gaps,
    error: null,
  };
}

function errorState(error: NumberEnergyRuntimePublicError): NumberEnergyRuntimeState {
  return {
    status: NUMBER_ENERGY_RUNTIME_STATUS.error,
    view: null,
    adapterResult: null,
    slotSource: null,
    gaps: [],
    error,
  };
}

function toPublicError(error: NumberEnergyRuntimeClientError): NumberEnergyRuntimePublicError {
  return { code: error.code, message: error.message };
}
